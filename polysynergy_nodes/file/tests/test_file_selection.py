import unittest
from polysynergy_nodes.file.file_selection import FileSelection


class TestFileSelection(unittest.TestCase):

    def setUp(self):
        self.node = FileSelection()
        self.node.true_path = False
        self.node.false_path = False

    def test_node_initialization(self):
        """Test that the node initializes correctly"""
        self.assertIsNotNone(self.node)
        self.assertIsInstance(self.node, FileSelection)

    def test_execute_with_selected_files(self):
        """Test execute with files selected"""
        test_files = [
            "tenant123/project456/private/documents/report.pdf",
            "tenant123/project456/private/images/chart.png",
            "tenant123/project456/private/data/dataset.csv"
        ]
        
        self.node.selected_files = test_files
        self.node.execute()
        
        # Should trigger true_path with the files
        self.assertEqual(self.node.true_path, test_files)
        self.assertEqual(self.node.file_count, 3)
        self.assertFalse(self.node.false_path)

    def test_execute_with_single_file(self):
        """Test execute with single file selected"""
        test_files = ["tenant123/project456/public/uploads/document.pdf"]
        
        self.node.selected_files = test_files
        self.node.execute()
        
        # Should trigger true_path with the single file
        self.assertEqual(self.node.true_path, test_files)
        self.assertEqual(self.node.file_count, 1)
        self.assertFalse(self.node.false_path)

    def test_execute_with_no_files_empty_list(self):
        """Test execute with empty file list"""
        self.node.selected_files = []
        self.node.execute()
        
        # Should trigger false_path
        self.assertEqual(self.node.false_path, {"error": "No files selected from file manager."})
        self.assertEqual(self.node.file_count, 0)
        self.assertFalse(self.node.true_path)

    def test_execute_with_no_files_none(self):
        """Test execute with None as selected_files"""
        self.node.selected_files = None
        self.node.execute()
        
        # Should trigger false_path
        self.assertEqual(self.node.false_path, {"error": "No files selected from file manager."})
        self.assertEqual(self.node.file_count, 0)
        self.assertFalse(self.node.true_path)

    def test_file_count_accuracy(self):
        """Test that file_count is accurate for different scenarios"""
        # Test with multiple files
        test_files_multiple = [
            "file1.pdf", "file2.jpg", "file3.txt", "file4.csv", "file5.docx"
        ]
        self.node.selected_files = test_files_multiple
        self.node.execute()
        self.assertEqual(self.node.file_count, 5)
        
        # Test with single file
        self.node.selected_files = ["single_file.pdf"]
        self.node.execute()
        self.assertEqual(self.node.file_count, 1)
        
        # Test with no files
        self.node.selected_files = []
        self.node.execute()
        self.assertEqual(self.node.file_count, 0)

    def test_selected_files_passthrough(self):
        """Test that selected_files are passed through unchanged"""
        original_files = [
            "tenant123/project456/private/docs/original_file.pdf",
            "tenant123/project456/public/images/original_image.png"
        ]
        
        self.node.selected_files = original_files
        self.node.execute()
        
        # Output should be identical to input
        self.assertEqual(self.node.true_path, original_files)
        self.assertEqual(self.node.selected_files, original_files)

    def test_file_location_formats(self):
        """Test various file location formats"""
        test_cases = [
            # Standard private files
            ["tenant123/project456/private/documents/report.pdf"],
            # Public files
            ["tenant123/project456/public/uploads/image.jpg"],
            # Files with subdirectories
            ["tenant123/project456/private/data/2024/january/stats.csv"],
            # Mixed scope files
            [
                "tenant123/project456/private/docs/private_doc.pdf",
                "tenant123/project456/public/images/public_image.png"
            ]
        ]
        
        for test_files in test_cases:
            with self.subTest(files=test_files):
                self.node.selected_files = test_files
                self.node.execute()
                
                self.assertEqual(self.node.true_path, test_files)
                self.assertEqual(self.node.file_count, len(test_files))

    def test_node_properties_exist(self):
        """Test that all expected properties exist"""
        # Check that the node has the expected attributes
        self.assertTrue(hasattr(self.node, 'selected_files'))
        self.assertTrue(hasattr(self.node, 'file_count'))
        self.assertTrue(hasattr(self.node, 'true_path'))
        self.assertTrue(hasattr(self.node, 'false_path'))

    def test_multiple_executions(self):
        """Test that the node can be executed multiple times with different inputs"""
        # First execution with files
        files1 = ["file1.pdf", "file2.jpg"]
        self.node.selected_files = files1
        self.node.execute()
        self.assertEqual(self.node.true_path, files1)
        self.assertEqual(self.node.file_count, 2)
        
        # Second execution with no files
        self.node.selected_files = []
        self.node.execute()
        self.assertEqual(self.node.false_path, {"error": "No files selected from file manager."})
        self.assertEqual(self.node.file_count, 0)
        
        # Third execution with different files
        files3 = ["file3.txt"]
        self.node.selected_files = files3
        self.node.execute()
        self.assertEqual(self.node.true_path, files3)
        self.assertEqual(self.node.file_count, 1)

    def test_error_message_format(self):
        """Test that error message has the correct format"""
        self.node.selected_files = []
        self.node.execute()
        
        error = self.node.false_path
        self.assertIsInstance(error, dict)
        self.assertIn("error", error)
        self.assertEqual(error["error"], "No files selected from file manager.")


if __name__ == "__main__":
    unittest.main()