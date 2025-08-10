import unittest
from unittest.mock import patch, MagicMock
from polysynergy_nodes.dynamodb.get import KeyValueStoreGet

class TestKeyValueStoreGetNode(unittest.TestCase):

    def setUp(self):
        self.node = KeyValueStoreGet()
        self.node.true_path = False
        self.node.false_path = False
        self.node.table_name = "KeyValueStore"
        self.node.key = "myKey"

    @patch("polysynergy_nodes.dynamodb.get.DynamoDBClient")
    def test_key_found(self, mock_dynamo_client_class):
        mock_table = MagicMock()
        mock_table.get_item.return_value = {"Item": {"Value": "found_value"}}

        mock_dynamo_client = MagicMock()
        mock_dynamo_client.get_table.return_value = mock_table
        mock_dynamo_client_class.return_value = mock_dynamo_client

        self.node.execute()

        self.assertEqual(self.node.true_path, "found_value")
        self.assertFalse(self.node.false_path)

    @patch("polysynergy_nodes.dynamodb.get.DynamoDBClient")
    def test_key_not_found(self, mock_dynamo_client_class):
        mock_table = MagicMock()
        mock_table.get_item.return_value = {}

        mock_dynamo_client = MagicMock()
        mock_dynamo_client.get_table.return_value = mock_table
        mock_dynamo_client_class.return_value = mock_dynamo_client

        self.node.execute()

        self.assertFalse(self.node.true_path)
        self.assertIn("error", self.node.false_path)

    @patch("polysynergy_nodes.dynamodb.get.DynamoDBClient")
    def test_dynamodb_exception(self, mock_dynamo_client_class):
        mock_table = MagicMock()
        mock_table.get_item.side_effect = Exception("Something went wrong")

        mock_dynamo_client = MagicMock()
        mock_dynamo_client.get_table.return_value = mock_table
        mock_dynamo_client_class.return_value = mock_dynamo_client

        self.node.execute()

        self.assertFalse(self.node.true_path)
        self.assertIn("error", self.node.false_path)
        self.assertIn("Something went wrong", self.node.false_path["error"])

if __name__ == "__main__":
    unittest.main()