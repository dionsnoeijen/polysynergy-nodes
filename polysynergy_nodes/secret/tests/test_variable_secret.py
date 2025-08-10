import asyncio
import unittest
from polysynergy_nodes.secret.variable_secret import VariableSecret


class TestVariableSecretNode(unittest.TestCase):

    def setUp(self):
        self.node = VariableSecret()
        self.node.true_path = None

    def test_node_creation(self):
        """Test that the node can be created successfully."""
        self.assertIsInstance(self.node, VariableSecret)
        self.assertIsNone(self.node.true_path)

    def test_execute_method_exists(self):
        """Test that the execute method exists and is callable."""
        self.assertTrue(hasattr(self.node, 'execute'))
        self.assertTrue(callable(getattr(self.node, 'execute')))

    def test_execute_does_not_modify_state(self):
        """Test that execute doesn't change the node's state."""
        initial_true_path = self.node.true_path
        asyncio.run(self.node.execute())
        self.assertEqual(self.node.true_path, initial_true_path)

    def test_execute_with_preset_true_path(self):
        """Test that execute doesn't modify a preset true_path value."""
        self.node.true_path = "test_secret_key"
        asyncio.run(self.node.execute())
        self.assertEqual(self.node.true_path, "test_secret_key")

    def test_execute_with_boolean_true_path(self):
        """Test that execute works with boolean true_path values."""
        self.node.true_path = True
        asyncio.run(self.node.execute())
        self.assertTrue(self.node.true_path)

        self.node.true_path = False
        asyncio.run(self.node.execute())
        self.assertFalse(self.node.true_path)

    def test_execute_is_async(self):
        """Test that execute is properly async."""
        result = self.node.execute()
        self.assertTrue(asyncio.iscoroutine(result))
        # Clean up the coroutine to avoid warnings
        asyncio.run(result)

    def test_multiple_execute_calls(self):
        """Test that multiple execute calls work consistently."""
        self.node.true_path = "persistent_value"
        
        # Execute multiple times
        for _ in range(3):
            asyncio.run(self.node.execute())
            self.assertEqual(self.node.true_path, "persistent_value")

    def test_node_attributes(self):
        """Test that the node has the expected attributes."""
        # Check that true_path is defined
        self.assertTrue(hasattr(self.node, 'true_path'))
        
        # The node should be very minimal - just true_path and execute
        expected_methods = ['execute']
        for method in expected_methods:
            self.assertTrue(hasattr(self.node, method))


if __name__ == "__main__":
    unittest.main()