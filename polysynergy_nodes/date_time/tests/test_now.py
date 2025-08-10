import unittest
from datetime import datetime, timedelta, timezone
from polysynergy_nodes.date_time.now import Now


class TestNowNode(unittest.TestCase):

    def setUp(self):
        self.node = Now()
        self.node.false_path = False
        self.node.true_path = False
        self.node.timestamp_output = None

    def test_default_now_format(self):
        self.node.format = "%Y-%m-%d %H:%M:%S"
        self.node.offset = ""
        self.node.execute()

        result_time = datetime.strptime(self.node.true_path, "%Y-%m-%d %H:%M:%S")
        now = datetime.now(timezone.utc)
        delta = abs((now - result_time.replace(tzinfo=timezone.utc)).total_seconds())
        self.assertLessEqual(delta, 2)

        self.assertIsInstance(self.node.timestamp_output, int)

    def test_iso_format(self):
        self.node.format = "iso8601"
        self.node.offset = ""
        self.node.execute()

        self.assertRegex(self.node.true_path, r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z")
        self.assertIsInstance(self.node.timestamp_output, int)

    def test_offset_minus_seconds(self):
        self.node.format = "%s"
        self.node.offset = "-5s"
        self.node.execute()

        expected = int((datetime.now(timezone.utc) - timedelta(seconds=5)).timestamp())
        delta = abs(self.node.timestamp_output - expected)
        self.assertLessEqual(delta, 2)

    def test_offset_plus_minutes(self):
        self.node.format = "iso8601"
        self.node.offset = "+2m"
        self.node.execute()

        self.assertIn("T", self.node.true_path)
        self.assertIsInstance(self.node.timestamp_output, int)

    def test_invalid_offset(self):
        self.node.offset = "5weeks"
        self.node.execute()
        self.assertIn("error", self.node.false_path)
        self.assertIsNone(self.node.timestamp_output)

    def test_offset_days(self):
        self.node.offset = "-3d"
        self.node.format = "%Y-%m-%d"
        self.node.execute()

        expected_date = (datetime.now(timezone.utc) - timedelta(days=3)).strftime("%Y-%m-%d")
        self.assertEqual(self.node.true_path, expected_date)

if __name__ == '__main__':
    unittest.main()