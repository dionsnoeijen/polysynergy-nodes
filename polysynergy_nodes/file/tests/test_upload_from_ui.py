import unittest
from polysynergy_nodes.file.upload_from_ui import UploadFromUI

class TestUploadFromUINode(unittest.TestCase):

    def setUp(self):
        self.node = UploadFromUI()
        self.node.true_path = False
        self.node.false_path = False

    def test_files_present(self):
        self.node.files = [
            {"name": "example.txt", "url": "https://example.com/example.txt"},
            {"name": "image.png", "url": "https://example.com/image.png"}
        ]
        self.node.execute()
        self.assertEqual(self.node.true_path, self.node.files)
        self.assertFalse(self.node.false_path)

    def test_no_files(self):
        self.node.files = []
        self.node.execute()
        self.assertIn("error", self.node.false_path)
        self.assertFalse(self.node.true_path)

    def test_files_none(self):
        self.node.files = None
        self.node.execute()
        self.assertIn("error", self.node.false_path)
        self.assertFalse(self.node.true_path)

if __name__ == "__main__":
    unittest.main()