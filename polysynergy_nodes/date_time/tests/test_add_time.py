import unittest
from datetime import datetime, timedelta
from polysynergy_nodes.date_time.add_time import AddTime


class TestAddTime(unittest.TestCase):

    def setUp(self):
        self.node = AddTime()
        self.node.false_path = False
        self.node.true_path = False
        self.node.result_datetime = None
        self.node.timestamp_output = None

    def test_add_seconds(self):
        self.node.datetime_input = "2024-01-15T12:00:00"
        self.node.duration = "30s"
        self.node.format_output = "iso8601"
        
        self.node.execute()
        
        self.assertIsNotNone(self.node.result_datetime)
        self.assertTrue("12:00:30" in self.node.result_datetime)
        self.assertIsInstance(self.node.timestamp_output, int)
        self.assertEqual(self.node.true_path, self.node.result_datetime)
        self.assertFalse(self.node.false_path)

    def test_add_minutes(self):
        self.node.datetime_input = "2024-01-15T12:00:00"
        self.node.duration = "45m"
        self.node.format_output = "iso8601"
        
        self.node.execute()
        
        self.assertIsNotNone(self.node.result_datetime)
        self.assertTrue("12:45:00" in self.node.result_datetime)
        self.assertFalse(self.node.false_path)

    def test_add_hours(self):
        self.node.datetime_input = "2024-01-15T12:00:00"
        self.node.duration = "3h"
        self.node.format_output = "iso8601"
        
        self.node.execute()
        
        self.assertIsNotNone(self.node.result_datetime)
        self.assertTrue("15:00:00" in self.node.result_datetime)
        self.assertFalse(self.node.false_path)

    def test_add_days(self):
        self.node.datetime_input = "2024-01-15T12:00:00"
        self.node.duration = "7d"
        self.node.format_output = "iso8601"
        
        self.node.execute()
        
        self.assertIsNotNone(self.node.result_datetime)
        self.assertTrue("2024-01-22" in self.node.result_datetime)
        self.assertFalse(self.node.false_path)

    def test_add_weeks(self):
        self.node.datetime_input = "2024-01-15T12:00:00"
        self.node.duration = "2w"
        self.node.format_output = "iso8601"
        
        self.node.execute()
        
        self.assertIsNotNone(self.node.result_datetime)
        self.assertTrue("2024-01-29" in self.node.result_datetime)
        self.assertFalse(self.node.false_path)

    def test_add_compound_duration(self):
        # Test multiple units like "1h30m"
        self.node.datetime_input = "2024-01-15T12:00:00"
        self.node.duration = "1h30m"
        self.node.format_output = "iso8601"
        
        self.node.execute()
        
        self.assertIsNotNone(self.node.result_datetime)
        self.assertTrue("13:30:00" in self.node.result_datetime)
        self.assertFalse(self.node.false_path)

    def test_add_complex_compound_duration(self):
        # Test complex duration like "2d5h30m15s"
        self.node.datetime_input = "2024-01-15T12:00:00"
        self.node.duration = "2d5h30m15s"
        self.node.format_output = "iso8601"
        
        self.node.execute()
        
        self.assertIsNotNone(self.node.result_datetime)
        self.assertTrue("2024-01-17" in self.node.result_datetime)
        self.assertTrue("17:30:15" in self.node.result_datetime)
        self.assertFalse(self.node.false_path)

    def test_custom_format_output(self):
        self.node.datetime_input = "2024-01-15T12:00:00"
        self.node.duration = "1h"
        self.node.format_output = "%Y-%m-%d %H:%M:%S"
        
        self.node.execute()
        
        self.assertIsNotNone(self.node.result_datetime)
        self.assertRegex(self.node.result_datetime, r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")
        self.assertTrue("13:00:00" in self.node.result_datetime)

    def test_iso_input_with_z_suffix(self):
        self.node.datetime_input = "2024-01-15T12:00:00Z"
        self.node.duration = "30m"
        self.node.format_output = "iso8601"
        
        self.node.execute()
        
        self.assertIsNotNone(self.node.result_datetime)
        self.assertTrue("12:30:00" in self.node.result_datetime)
        self.assertFalse(self.node.false_path)

    def test_common_datetime_input_formats(self):
        test_formats = [
            "2024-01-15 12:00:00",
            "2024-01-15T12:00:00.123456",
            "2024-01-15",
        ]
        
        for dt_format in test_formats:
            with self.subTest(format=dt_format):
                self.node.datetime_input = dt_format
                self.node.duration = "1h"
                self.node.format_output = "iso8601"
                
                # Reset state
                self.node.false_path = False
                self.node.result_datetime = None
                
                self.node.execute()
                
                self.assertIsNotNone(self.node.result_datetime)
                self.assertFalse(self.node.false_path)

    def test_invalid_duration_format(self):
        self.node.datetime_input = "2024-01-15T12:00:00"
        self.node.duration = "invalid_duration"
        
        self.node.execute()
        
        self.assertIn("error", self.node.false_path)
        self.assertIsNone(self.node.result_datetime)
        self.assertIsNone(self.node.timestamp_output)

    def test_invalid_datetime_input(self):
        self.node.datetime_input = "not a datetime"
        self.node.duration = "1h"
        
        self.node.execute()
        
        self.assertIn("error", self.node.false_path)
        self.assertIsNone(self.node.result_datetime)
        self.assertIsNone(self.node.timestamp_output)

    def test_empty_duration(self):
        self.node.datetime_input = "2024-01-15T12:00:00"
        self.node.duration = ""
        self.node.format_output = "iso8601"
        
        self.node.execute()
        
        self.assertIsNotNone(self.node.result_datetime)
        # Should return the same datetime when duration is empty
        self.assertTrue("12:00:00" in self.node.result_datetime)
        self.assertFalse(self.node.false_path)

    def test_unsupported_duration_unit(self):
        self.node.datetime_input = "2024-01-15T12:00:00"
        self.node.duration = "5y"  # Years not supported
        
        self.node.execute()
        
        self.assertIn("error", self.node.false_path)
        self.assertIsNone(self.node.result_datetime)

    def test_parse_duration_method(self):
        # Test the helper method directly
        duration = self.node.parse_duration("1h30m")
        expected = timedelta(hours=1, minutes=30)
        self.assertEqual(duration, expected)
        
        # Test complex duration
        duration = self.node.parse_duration("2d5h30m15s")
        expected = timedelta(days=2, hours=5, minutes=30, seconds=15)
        self.assertEqual(duration, expected)
        
        # Test empty duration
        duration = self.node.parse_duration("")
        self.assertEqual(duration, timedelta(0))

    def test_parse_datetime_input_method(self):
        # Test the helper method directly
        dt = self.node.parse_datetime_input("2024-01-15T12:00:00")
        self.assertIsInstance(dt, datetime)
        self.assertEqual(dt.year, 2024)
        self.assertEqual(dt.hour, 12)

    def test_format_datetime_method(self):
        # Test the helper method directly
        self.node.format_output = "iso8601"
        dt = datetime(2024, 1, 15, 12, 0, 0)
        formatted = self.node.format_datetime(dt)
        self.assertIn("2024-01-15", formatted)
        self.assertIn("12:00:00", formatted)

    def test_large_duration_addition(self):
        # Test adding a large duration
        self.node.datetime_input = "2024-01-15T12:00:00"
        self.node.duration = "365d"  # One year
        self.node.format_output = "iso8601"
        
        self.node.execute()
        
        self.assertIsNotNone(self.node.result_datetime)
        # Should be around January 15, 2025
        self.assertTrue("2025-01" in self.node.result_datetime)
        self.assertFalse(self.node.false_path)

    def test_microseconds_handling(self):
        self.node.datetime_input = "2024-01-15T12:00:00.123456"
        self.node.duration = "1s"
        self.node.format_output = "iso8601"
        
        self.node.execute()
        
        self.assertIsNotNone(self.node.result_datetime)
        self.assertTrue("12:00:01" in self.node.result_datetime)
        self.assertFalse(self.node.false_path)


if __name__ == "__main__":
    unittest.main()