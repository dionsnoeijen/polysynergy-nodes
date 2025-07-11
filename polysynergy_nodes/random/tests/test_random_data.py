import unittest
from faker import Faker
from polysynergy_nodes.random.random_data import RandomData

faker = Faker()

class TestRandomDataNode(unittest.TestCase):

    def setUp(self):
        self.node = RandomData()
        self.node.true_path = False
        self.node.type = "name"
        self.node.min = 0
        self.node.max = 100

    def test_name_type(self):
        self.node.type = "name"
        self.node.execute()
        self.assertTrue(isinstance(self.node.true_path, str))  # Expect a string for name
        self.assertTrue(len(self.node.true_path.split()) >= 2)  # Name should consist of at least two words

    def test_email_type(self):
        self.node.type = "email"
        self.node.execute()
        self.assertTrue(isinstance(self.node.true_path, str))  # Expect a string for email
        self.assertTrue("@" in self.node.true_path)

    def test_uuid_type(self):
        self.node.type = "uuid"
        self.node.execute()
        self.assertTrue(isinstance(self.node.true_path, str))  # Expect a string for UUID
        self.assertTrue(len(self.node.true_path) == 36)  # UUID length should be 36

    def test_text_type(self):
        self.node.type = "text"
        self.node.execute()
        self.assertTrue(isinstance(self.node.true_path, str))  # Expect a string for text
        self.assertTrue(len(self.node.true_path) > 0)  # Text should have content

    def test_int_type(self):
        self.node.type = "int"
        self.node.execute()
        self.assertTrue(isinstance(self.node.true_path, int))  # Expect an integer for int type
        self.assertTrue(self.node.true_path >= self.node.min and self.node.true_path <= self.node.max)  # Integer should be within min and max

    def test_float_type(self):
        self.node.type = "float"
        self.node.execute()
        self.assertTrue(isinstance(self.node.true_path, float))  # Expect a float for float type
        self.assertTrue(self.node.true_path >= self.node.min and self.node.true_path <= self.node.max)  # Float should be within min and max

    def test_date_type(self):
        self.node.type = "date"
        self.node.execute()
        self.assertTrue(isinstance(self.node.true_path, str))  # Expect a string for date
        self.assertTrue("T" in self.node.true_path)  # Date format should have a "T" for ISO format

    def test_company_type(self):
        self.node.type = "company"
        self.node.execute()
        self.assertTrue(isinstance(self.node.true_path, str))  # Expect a string for company
        self.assertTrue(len(self.node.true_path) > 0)  # Company name should have content

    def test_unsupported_type(self):
        self.node.type = "unsupported_type"
        self.node.execute()
        self.assertEqual(self.node.true_path, "Unsupported type: unsupported_type")

if __name__ == "__main__":
    unittest.main()