import unittest
from unittest.mock import patch
from polysynergy_nodes.log.log_error import LogError

class TestLogErrorNode(unittest.TestCase):
    def setUp(self):
        self.node = LogError()
        self.node.message = "Test error message"

    @patch("polysynergy_nodes.log.log_error.logger")
    def test_error_logging(self, mock_logger):
        self.node.execute()
        mock_logger.error.assert_called_once_with("Test error message")

if __name__ == "__main__":
    unittest.main()