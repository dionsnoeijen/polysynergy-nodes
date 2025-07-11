import unittest
from unittest.mock import patch
from polysynergy_nodes.log.log_info import LogInfo

class TestLogInfoNode(unittest.TestCase):
    def setUp(self):
        self.node = LogInfo()
        self.node.message = "This is an info message"

    @patch("polysynergy_nodes.log.log_info.logger")
    def test_info_logging(self, mock_logger):
        self.node.execute()
        mock_logger.info.assert_called_once_with("This is an info message")

if __name__ == "__main__":
    unittest.main()