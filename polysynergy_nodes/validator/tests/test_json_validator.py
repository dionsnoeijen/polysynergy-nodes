import unittest
from polysynergy_nodes.validator.json import Json

class TestJsonValidatorNode(unittest.TestCase):

    def setUp(self):
        self.node = Json()
        self.node.true_path = False
        self.node.false_path = False

    def test_valid_json(self):
        schema = """
        {
            "fields": {
                "name": {"type": "str", "required": true},
                "age": {"type": "int", "required": true}
            }
        }
        """
        input_json = '{"name": "John", "age": 30}'
        self.node.schema = schema
        self.node.input_json = input_json
        self.node.execute()
        self.assertTrue(self.node.true_path)  # The JSON should be valid
        self.assertEqual(self.node.validation_result, "Valid JSON")

    def test_invalid_json(self):
        schema = """
        {
            "fields": {
                "name": {"type": "str", "required": true},
                "age": {"type": "int", "required": true}
            }
        }
        """
        input_json = '{"name": "John", "age": "not_a_number"}'  # Invalid value for age
        self.node.schema = schema
        self.node.input_json = input_json
        self.node.execute()
        self.assertFalse(self.node.true_path)  # The JSON should be invalid
        self.assertIn("Validation Error", self.node.validation_result)

    def test_empty_input(self):
        schema = """
        {
            "fields": {
                "name": {"type": "str", "required": true},
                "age": {"type": "int", "required": true}
            }
        }
        """
        input_json = ""  # Empty input
        self.node.schema = schema
        self.node.input_json = input_json
        self.node.execute()
        self.assertFalse(self.node.true_path)  # The input should be considered empty and invalid
        self.assertIn("Input is empty", self.node.validation_result)

    def test_invalid_schema(self):
        schema = """{
            "fields": {
                "name": {"type": "str"}
            }
        """  # Invalid schema (missing closing bracket)
        input_json = '{"name": "John"}'
        self.node.schema = schema
        self.node.input_json = input_json
        self.node.execute()
        self.assertFalse(self.node.true_path)  # The schema is invalid
        self.assertIn("Schema is invalid JSON", self.node.validation_result)

    def test_invalid_json_structure(self):
        schema = """
        {
            "fields": {
                "name": {"type": "str", "required": true}
            }
        }
        """
        input_json = '{"age": 30}'  # Missing required 'name' field
        self.node.schema = schema
        self.node.input_json = input_json
        self.node.execute()
        self.assertFalse(self.node.true_path)  # The JSON structure is invalid (missing required field)
        self.assertIn("Validation Error", self.node.validation_result)

if __name__ == "__main__":
    unittest.main()