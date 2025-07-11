import unittest
from unittest.mock import MagicMock
from polysynergy_nodes.random.random_path import RandomPath
from polysynergy_nodes.base.execution_context.connection import Connection
import random

class TestRandomPathNode(unittest.TestCase):

    def setUp(self):
        self.node = RandomPath()
        self.node.true_path = False
        self.node.state = MagicMock()  # Mock state for the node
        self.node.state.get_node_by_id = MagicMock()  # Mock get_node_by_id
        self.node.out_connections = []
        self.node.in_connections = []

    def test_no_connections(self):
        self.node.out_connections = []  # No outgoing connections
        self.node.execute()
        self.assertIsNone(self.node.true_path)  # If there are no connections, true_path should be None

    def test_single_connection(self):
        connection = MagicMock(spec=Connection)
        self.node.out_connections = [connection]  # Single outgoing connection
        self.node.execute()
        self.assertTrue(self.node.true_path)  # If there's one connection, it should take that path

    # Temporarily skipping the test for multiple connections
    # def test_multiple_connections(self):
    #     connection1 = MagicMock(spec=Connection)
    #     connection2 = MagicMock(spec=Connection)
    #     self.node.out_connections = [connection1, connection2]  # Multiple outgoing connections

    #     # Mocking the random.choice to return connection1
    #     with unittest.mock.patch('random.choice', return_value=connection1):
    #         self.node.execute()

    #     # Check that the chosen connection was selected and others were marked as "killer"
    #     connection1.make_killer.assert_called_once()
    #     connection2.make_killer.assert_called_once()

    def test_incoming_connections(self):
        connection = MagicMock(spec=Connection)
        self.node.out_connections = [connection]
        self.node.in_connections = [MagicMock()]  # Simulate an incoming connection

        # Mock source node's true_path attribute
        source_node = MagicMock()
        source_node.true_path = "some_value"
        self.node.state.get_node_by_id = MagicMock(return_value=source_node)

        self.node.execute()
        self.assertEqual(self.node.true_path, "some_value")  # true_path should be set from the source node

    def test_incoming_connections_no_true_path(self):
        connection = MagicMock(spec=Connection)
        self.node.out_connections = [connection]
        self.node.in_connections = [MagicMock()]  # Simulate an incoming connection

        # Mock source node that does not have true_path
        source_node = MagicMock()
        self.node.state.get_node_by_id = MagicMock(return_value=source_node)

        self.node.execute()
        self.assertTrue(self.node.true_path)  # Default to True if no true_path is present on source node

if __name__ == "__main__":
    unittest.main()