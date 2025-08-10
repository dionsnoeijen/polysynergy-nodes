import unittest
from unittest.mock import Mock, patch, MagicMock
from botocore.exceptions import ClientError
from polysynergy_nodes.secret.services.secrets_manager import SecretsManager


class TestSecretsManager(unittest.TestCase):

    @patch('polysynergy_nodes.secret.services.secrets_manager.boto3.client')
    @patch.dict('os.environ', {
        'AWS_REGION': 'us-west-2',
        'AWS_ACCESS_KEY_ID': 'test_key',
        'AWS_SECRET_ACCESS_KEY': 'test_secret'
    })
    def test_init_with_explicit_credentials(self, mock_boto_client):
        """Test initialization with explicit AWS credentials."""
        mock_client = Mock()
        mock_boto_client.return_value = mock_client
        
        manager = SecretsManager()
        
        mock_boto_client.assert_called_once_with(
            "secretsmanager",
            region_name="us-west-2",
            aws_access_key_id="test_key",
            aws_secret_access_key="test_secret",
            aws_session_token=None
        )
        self.assertEqual(manager.client, mock_client)

    @patch('polysynergy_nodes.secret.services.secrets_manager.boto3.client')
    @patch.dict('os.environ', {'AWS_REGION': 'eu-central-1'}, clear=True)
    def test_init_without_explicit_credentials(self, mock_boto_client):
        """Test initialization without explicit AWS credentials."""
        mock_client = Mock()
        mock_boto_client.return_value = mock_client
        
        manager = SecretsManager()
        
        mock_boto_client.assert_called_once_with(
            "secretsmanager",
            region_name="eu-central-1"
        )

    @patch('polysynergy_nodes.secret.services.secrets_manager.boto3.client')
    @patch.dict('os.environ', {
        'AWS_EXECUTION_ENV': 'AWS_Lambda_python3.9'
    }, clear=True)
    def test_init_in_lambda_environment(self, mock_boto_client):
        """Test initialization in Lambda environment."""
        mock_client = Mock()
        mock_boto_client.return_value = mock_client
        
        manager = SecretsManager()
        
        # Should use default credentials in Lambda
        mock_boto_client.assert_called_once_with(
            "secretsmanager", 
            region_name="eu-central-1"
        )

    def test_prefix_name_with_stage(self):
        """Test name prefixing with stage."""
        with patch('polysynergy_nodes.secret.services.secrets_manager.boto3.client'):
            manager = SecretsManager()
            result = manager._prefix_name("my_secret", "project_123", "dev")
            self.assertEqual(result, "project_123@dev@my_secret")

    def test_prefix_name_without_stage(self):
        """Test name prefixing without stage."""
        with patch('polysynergy_nodes.secret.services.secrets_manager.boto3.client'):
            manager = SecretsManager()
            result = manager._prefix_name("my_secret", "project_123")
            self.assertEqual(result, "project_123@my_secret")

    @patch('polysynergy_nodes.secret.services.secrets_manager.boto3.client')
    def test_create_secret_success(self, mock_boto_client):
        """Test successful secret creation."""
        mock_client = Mock()
        mock_boto_client.return_value = mock_client
        mock_client.create_secret.return_value = {"ARN": "test_arn"}
        
        manager = SecretsManager()
        result = manager.create_secret("my_secret", "secret_value", "project_123", "dev")
        
        mock_client.create_secret.assert_called_once_with(
            Name="project_123@dev@my_secret",
            SecretString="secret_value",
            Tags=[
                {"Key": "project", "Value": "project_123"},
                {"Key": "stage", "Value": "dev"}
            ]
        )
        self.assertEqual(result, {"ARN": "test_arn"})

    @patch('polysynergy_nodes.secret.services.secrets_manager.boto3.client')
    def test_create_secret_client_error(self, mock_boto_client):
        """Test secret creation with ClientError."""
        mock_client = Mock()
        mock_boto_client.return_value = mock_client
        client_error = ClientError(
            {"Error": {"Code": "ResourceExistsException"}},
            "CreateSecret"
        )
        mock_client.create_secret.side_effect = client_error
        
        manager = SecretsManager()
        
        with self.assertRaises(ClientError):
            manager.create_secret("my_secret", "secret_value", "project_123", "dev")

    @patch('polysynergy_nodes.secret.services.secrets_manager.boto3.client')
    def test_get_secret_success(self, mock_boto_client):
        """Test successful secret retrieval."""
        mock_client = Mock()
        mock_boto_client.return_value = mock_client
        mock_client.get_secret_value.return_value = {
            "Name": "project_123@dev@my_secret",
            "SecretString": "secret_value"
        }
        
        manager = SecretsManager()
        result = manager.get_secret("project_123@dev@my_secret")
        
        mock_client.get_secret_value.assert_called_once_with(
            SecretId="project_123@dev@my_secret"
        )
        self.assertEqual(result, {
            "key": "dev@my_secret", 
            "value": "secret_value"
        })

    @patch('polysynergy_nodes.secret.services.secrets_manager.boto3.client')
    def test_get_secret_by_key(self, mock_boto_client):
        """Test get secret by key."""
        mock_client = Mock()
        mock_boto_client.return_value = mock_client
        mock_client.get_secret_value.return_value = {
            "Name": "project_123@dev@my_secret",
            "SecretString": "secret_value"
        }
        
        manager = SecretsManager()
        result = manager.get_secret_by_key("my_secret", "project_123", "dev")
        
        mock_client.get_secret_value.assert_called_once_with(
            SecretId="project_123@dev@my_secret"
        )
        self.assertEqual(result, {
            "key": "dev@my_secret",
            "value": "secret_value"
        })

    @patch('polysynergy_nodes.secret.services.secrets_manager.boto3.client')
    def test_update_secret_success(self, mock_boto_client):
        """Test successful secret update."""
        mock_client = Mock()
        mock_boto_client.return_value = mock_client
        mock_client.update_secret.return_value = {"ARN": "test_arn"}
        
        manager = SecretsManager()
        result = manager.update_secret("secret_id", "new_value")
        
        mock_client.update_secret.assert_called_once_with(
            SecretId="secret_id",
            SecretString="new_value"
        )
        self.assertEqual(result, {"ARN": "test_arn"})

    @patch('polysynergy_nodes.secret.services.secrets_manager.boto3.client')
    def test_delete_secret_success(self, mock_boto_client):
        """Test successful secret deletion."""
        mock_client = Mock()
        mock_boto_client.return_value = mock_client
        mock_client.delete_secret.return_value = {"ARN": "test_arn"}
        
        manager = SecretsManager()
        result = manager.delete_secret("secret_id")
        
        mock_client.delete_secret.assert_called_once_with(
            SecretId="secret_id",
            ForceDeleteWithoutRecovery=True
        )
        self.assertEqual(result, {"ARN": "test_arn"})

    @patch('polysynergy_nodes.secret.services.secrets_manager.boto3.client')
    def test_list_secrets_success(self, mock_boto_client):
        """Test successful secrets listing."""
        mock_client = Mock()
        mock_boto_client.return_value = mock_client
        mock_client.list_secrets.return_value = {
            "SecretList": [{"Name": "secret1"}, {"Name": "secret2"}]
        }
        
        manager = SecretsManager()
        result = manager.list_secrets("project_123")
        
        mock_client.list_secrets.assert_called_once_with(
            Filters=[
                {
                    'Key': 'tag-key',
                    'Values': ['project']
                },
                {
                    'Key': 'tag-value',
                    'Values': ['project_123']
                }
            ]
        )
        self.assertEqual(result, [{"Name": "secret1"}, {"Name": "secret2"}])


if __name__ == "__main__":
    unittest.main()