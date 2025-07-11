import unittest
from unittest.mock import patch, MagicMock
from polysynergy_nodes.dynamodb.set import KeyValueStoreSet

class TestKeyValueStoreSetNode(unittest.TestCase):

    def setUp(self):
        self.node = KeyValueStoreSet()
        self.node.true_path = False
        self.node.false_path = False
        self.node.table_name = "KeyValueStore"
        self.node.key = "myKey"
        self.node.value = "myValue"

    @patch("polysynergy_nodes.dynamodb.set.DynamoDBClient")
    def test_successful_store(self, mock_dynamo_client_class):
        mock_table = MagicMock()
        mock_table.put_item.return_value = {}

        mock_dynamo_client = MagicMock()
        mock_dynamo_client.get_table.return_value = mock_table
        mock_dynamo_client_class.return_value = mock_dynamo_client

        self.node.execute()

        self.assertEqual(self.node.true_path, "myValue")
        self.assertFalse(self.node.false_path)

    @patch("polysynergy_nodes.dynamodb.set.DynamoDBClient")
    def test_dynamodb_exception(self, mock_dynamo_client_class):
        mock_table = MagicMock()
        mock_table.put_item.side_effect = Exception("DynamoDB write failed")

        mock_dynamo_client = MagicMock()
        mock_dynamo_client.get_table.return_value = mock_table
        mock_dynamo_client_class.return_value = mock_dynamo_client

        self.node.execute()

        self.assertFalse(self.node.true_path)
        self.assertIn("error", self.node.false_path)
        self.assertIn("DynamoDB write failed", self.node.false_path["error"])

if __name__ == "__main__":
    unittest.main()