import unittest
from polysynergy_nodes.list.zip_inject import ZipInject

class TestZipInjectNode(unittest.TestCase):

    def setUp(self):
        self.node = ZipInject()
        self.node.true_path = False
        self.node.false_path = False

    def test_basic_zip_injection(self):
        self.node.source_list = [
            {"id": "1", "data": {}},
            {"id": "2", "data": {}}
        ]
        self.node.values_to_inject = ["A", "B"]
        self.node.target_path = "data.label"
        self.node.execute()
        self.assertEqual(
            self.node.true_path,
            [
                {"id": "1", "data": {"label": "A"}},
                {"id": "2", "data": {"label": "B"}}
            ]
        )
        self.assertFalse(self.node.false_path)

    def test_with_json_strings(self):
        self.node.source_list_as_string = '[{"id": "x"}, {"id": "y"}]'
        self.node.values_to_inject_as_string = '["foo", "bar"]'
        self.node.target_path = "result"
        self.node.execute()
        self.assertEqual(
            self.node.true_path,
            [
                {"id": "x", "result": "foo"},
                {"id": "y", "result": "bar"}
            ]
        )

    def test_length_mismatch(self):
        self.node.source_list = [{"a": 1}]
        self.node.values_to_inject = ["only", "extra"]
        self.node.target_path = "x"
        self.node.execute()
        self.assertIsInstance(self.node.false_path, dict)
        self.assertIn("error", self.node.false_path)

    def test_invalid_json(self):
        self.node.source_list_as_string = 'not valid json'
        self.node.values_to_inject = ["test"]
        self.node.target_path = "field"
        self.node.execute()
        self.assertIsInstance(self.node.false_path, dict)
        self.assertIn("error", self.node.false_path)

if __name__ == "__main__":
    unittest.main()
