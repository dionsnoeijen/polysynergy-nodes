import logging
import unittest
from polysynergy_nodes.date_time.fixed_window import FixedWindow

class TestFixedWindowNode(unittest.TestCase):

    def setUp(self):
        logging.disable(logging.ERROR)
        self.node = FixedWindow()
        self.node.false_path = False

    def test_iso_format_minutes_interval(self):
        self.node.reference_time = "2025-04-21T15:43:00Z"
        self.node.unit = "minutes"
        self.node.interval = 20
        self.node.format = "iso8601"
        self.node.execute()
        self.assertEqual(self.node.window_end, "2025-04-21T15:40:00Z")
        self.assertEqual(self.node.window_start, "2025-04-21T15:20:00Z")

    def test_iso_format_hours_interval(self):
        self.node.reference_time = "2025-04-21T17:43:00Z"
        self.node.unit = "hours"
        self.node.interval = 2
        self.node.format = "iso8601"
        self.node.execute()
        self.assertEqual(self.node.window_end, "2025-04-21T16:00:00Z")
        self.assertEqual(self.node.window_start, "2025-04-21T14:00:00Z")

    def test_iso_format_seconds_interval(self):
        self.node.reference_time = "2025-04-21T12:00:43Z"
        self.node.unit = "seconds"
        self.node.interval = 15
        self.node.format = "iso8601"
        self.node.execute()
        self.assertEqual(self.node.window_end, "2025-04-21T12:00:30Z")
        self.assertEqual(self.node.window_start, "2025-04-21T12:00:15Z")

    def test_invalid_unit(self):
        self.node.reference_time = "2025-04-21T12:00:00Z"
        self.node.unit = "days"
        self.node.interval = 1
        self.node.execute()
        self.assertIn("error", self.node.false_path)

    def test_invalid_reference_time_format(self):
        self.node.reference_time = "21-04-2025"
        self.node.unit = "minutes"
        self.node.interval = 5
        self.node.execute()
        self.assertIn("error", self.node.false_path)

if __name__ == "__main__":
    unittest.main()