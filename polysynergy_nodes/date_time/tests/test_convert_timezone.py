import unittest
from unittest.mock import patch
from datetime import datetime
import pytz
from polysynergy_nodes.date_time.convert_timezone import ConvertTimezone


class TestConvertTimezone(unittest.TestCase):

    def setUp(self):
        self.node = ConvertTimezone()
        self.node.false_path = False
        self.node.true_path = False
        self.node.converted_datetime = None
        self.node.timestamp_output = None

    def test_utc_to_eastern_conversion(self):
        self.node.datetime_input = "2024-01-15T12:00:00"
        self.node.from_timezone = "UTC"
        self.node.to_timezone = "America/New_York"
        self.node.format_output = "iso8601"
        
        self.node.execute()
        
        self.assertIsNotNone(self.node.converted_datetime)
        self.assertIsInstance(self.node.timestamp_output, int)
        self.assertEqual(self.node.true_path, self.node.converted_datetime)
        self.assertFalse(self.node.false_path)

    def test_eastern_to_pacific_conversion(self):
        self.node.datetime_input = "2024-07-15T15:30:00"
        self.node.from_timezone = "America/New_York"
        self.node.to_timezone = "America/Los_Angeles"
        self.node.format_output = "iso8601"
        
        self.node.execute()
        
        self.assertIsNotNone(self.node.converted_datetime)
        self.assertIsInstance(self.node.timestamp_output, int)
        # Eastern is 3 hours ahead of Pacific
        self.assertTrue("12:30:00" in self.node.converted_datetime or "12:30" in self.node.converted_datetime)

    def test_iso_format_with_z_suffix(self):
        self.node.datetime_input = "2024-01-15T12:00:00Z"
        self.node.from_timezone = "UTC"
        self.node.to_timezone = "Europe/London"
        self.node.format_output = "iso8601"
        
        self.node.execute()
        
        self.assertIsNotNone(self.node.converted_datetime)
        self.assertFalse(self.node.false_path)

    def test_custom_format_output(self):
        self.node.datetime_input = "2024-01-15T12:00:00"
        self.node.from_timezone = "UTC"
        self.node.to_timezone = "Asia/Tokyo"
        self.node.format_output = "%Y-%m-%d %H:%M:%S"
        
        self.node.execute()
        
        self.assertIsNotNone(self.node.converted_datetime)
        self.assertRegex(self.node.converted_datetime, r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")

    def test_already_aware_datetime(self):
        # Test with datetime that already has timezone info
        utc_dt = datetime(2024, 1, 15, 12, 0, 0, tzinfo=pytz.UTC)
        self.node.datetime_input = utc_dt.isoformat()
        self.node.from_timezone = "UTC"  # Should be ignored since datetime is already aware
        self.node.to_timezone = "Europe/Paris"
        self.node.format_output = "iso8601"
        
        self.node.execute()
        
        self.assertIsNotNone(self.node.converted_datetime)
        self.assertFalse(self.node.false_path)

    def test_invalid_from_timezone(self):
        self.node.datetime_input = "2024-01-15T12:00:00"
        self.node.from_timezone = "Invalid/Timezone"
        self.node.to_timezone = "UTC"
        
        self.node.execute()
        
        self.assertIn("error", self.node.false_path)
        self.assertIsNone(self.node.converted_datetime)
        self.assertIsNone(self.node.timestamp_output)

    def test_invalid_to_timezone(self):
        self.node.datetime_input = "2024-01-15T12:00:00"
        self.node.from_timezone = "UTC"
        self.node.to_timezone = "Invalid/Timezone"
        
        self.node.execute()
        
        self.assertIn("error", self.node.false_path)
        self.assertIsNone(self.node.converted_datetime)
        self.assertIsNone(self.node.timestamp_output)

    def test_invalid_datetime_input(self):
        self.node.datetime_input = "not a datetime"
        self.node.from_timezone = "UTC"
        self.node.to_timezone = "America/New_York"
        
        self.node.execute()
        
        self.assertIn("error", self.node.false_path)
        self.assertIsNone(self.node.converted_datetime)
        self.assertIsNone(self.node.timestamp_output)

    def test_common_datetime_formats(self):
        test_formats = [
            "2024-01-15 12:00:00",
            "2024-01-15T12:00:00.123456",
            "2024-01-15",
        ]
        
        for dt_format in test_formats:
            with self.subTest(format=dt_format):
                self.node.datetime_input = dt_format
                self.node.from_timezone = "UTC"
                self.node.to_timezone = "Europe/London"
                self.node.format_output = "iso8601"
                
                # Reset state
                self.node.false_path = False
                self.node.converted_datetime = None
                
                self.node.execute()
                
                self.assertIsNotNone(self.node.converted_datetime)
                self.assertFalse(self.node.false_path)

    def test_same_timezone_conversion(self):
        self.node.datetime_input = "2024-01-15T12:00:00"
        self.node.from_timezone = "UTC"
        self.node.to_timezone = "UTC"
        self.node.format_output = "iso8601"
        
        self.node.execute()
        
        self.assertIsNotNone(self.node.converted_datetime)
        self.assertTrue("12:00:00" in self.node.converted_datetime)
        self.assertFalse(self.node.false_path)

    def test_daylight_saving_time_handling(self):
        # Test during DST period (July) and standard time (January)
        summer_cases = [
            ("2024-07-15T12:00:00", "America/New_York", "America/Los_Angeles"),
            ("2024-01-15T12:00:00", "America/New_York", "America/Los_Angeles"),
        ]
        
        for dt_input, from_tz, to_tz in summer_cases:
            with self.subTest(datetime=dt_input):
                self.node.datetime_input = dt_input
                self.node.from_timezone = from_tz
                self.node.to_timezone = to_tz
                self.node.format_output = "iso8601"
                
                # Reset state
                self.node.false_path = False
                self.node.converted_datetime = None
                
                self.node.execute()
                
                self.assertIsNotNone(self.node.converted_datetime)
                self.assertFalse(self.node.false_path)

    def test_parse_datetime_input_method(self):
        # Test the helper method directly
        test_dt = self.node.parse_datetime_input("2024-01-15T12:00:00")
        self.assertIsInstance(test_dt, datetime)
        self.assertEqual(test_dt.year, 2024)
        self.assertEqual(test_dt.hour, 12)

    def test_get_timezone_method(self):
        # Test the helper method directly
        utc_tz = self.node.get_timezone("UTC")
        self.assertEqual(utc_tz.zone, "UTC")
        
        # Test invalid timezone
        with self.assertRaises(ValueError):
            self.node.get_timezone("Invalid/Timezone")


if __name__ == "__main__":
    unittest.main()