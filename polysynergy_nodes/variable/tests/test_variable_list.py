import unittest
from polysynergy_nodes.variable.variable_list import VariableList

class TestVariableListNode(unittest.TestCase):

    def setUp(self):
        self.node = VariableList()
        self.node.true_path = False
        self.node.false_path = False

    def test_append_value(self):
        self.node.value = [1, 2, 3]
        self.node.append = 4
        self.node.execute()

        self.assertTrue(self.node.true_path)
        self.assertEqual(self.node.true_path, [1, 2, 3, 4])

    def test_append_multiple_values(self):
        self.node.value = [1, 2, 3]
        self.node.append = [4, 5]
        self.node.execute()

        self.assertTrue(self.node.true_path)
        self.assertEqual(self.node.true_path, [1, 2, 3, [4, 5]])

    def test_append_empty_value(self):
        self.node.value = [1, 2, 3]
        self.node.append = []
        self.node.execute()

        self.assertTrue(self.node.true_path)
        self.assertEqual(self.node.true_path, [1, 2, 3])

    def test_no_append(self):
        self.node.value = [1, 2, 3]
        self.node.append = None  # No value to append
        self.node.execute()

        self.assertTrue(self.node.true_path)
        self.assertEqual(self.node.true_path, [1, 2, 3])

    def test_empty_list(self):
        self.node.value = []
        self.node.append = 1
        self.node.execute()

        self.assertTrue(self.node.true_path)
        self.assertEqual(self.node.true_path, [1])

if __name__ == "__main__":
    unittest.main()