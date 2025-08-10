import unittest
from datetime import datetime
import pytz
from polysynergy_nodes.date_time.localize_datetime import LocalizeDateTime


class TestLocalizeDateTime(unittest.TestCase):

    def setUp(self):
        self.node = LocalizeDateTime()
        self.node.false_path = False
        self.node.true_path = False
        self.node.localized_datetime = None
        self.node.timestamp_output = None

    def test_localize_naive_datetime_to_utc(self):
        self.node.datetime_input = "2024-01-15T12:00:00"
        self.node.timezone = "UTC"
        self.node.format_output = "iso8601"
        
        self.node.execute()
        
        self.assertIsNotNone(self.node.localized_datetime)
        self.assertIsInstance(self.node.timestamp_output, int)
        self.assertEqual(self.node.true_path, self.node.localized_datetime)
        self.assertFalse(self.node.false_path)

    def test_localize_to_eastern_timezone(self):
        self.node.datetime_input = "2024-01-15T12:00:00"
        self.node.timezone = "America/New_York"
        self.node.format_output = "iso8601"
        
        self.node.execute()
        
        self.assertIsNotNone(self.node.localized_datetime)
        self.assertTrue("12:00:00" in self.node.localized_datetime)
        self.assertTrue("-05:00" in self.node.localized_datetime or "-04:00" in self.node.localized_datetime)  # EST or EDT
        self.assertFalse(self.node.false_path)

    def test_localize_to_tokyo_timezone(self):
        self.node.datetime_input = "2024-01-15T12:00:00"
        self.node.timezone = "Asia/Tokyo"
        self.node.format_output = "iso8601"
        
        self.node.execute()
        
        self.assertIsNotNone(self.node.localized_datetime)
        self.assertTrue("12:00:00" in self.node.localized_datetime)
        self.assertTrue("+09:00" in self.node.localized_datetime)  # JST
        self.assertFalse(self.node.false_path)

    def test_custom_format_output(self):
        self.node.datetime_input = "2024-01-15T12:00:00"
        self.node.timezone = "Europe/London"
        self.node.format_output = "%Y-%m-%d %H:%M:%S %Z"
        
        self.node.execute()
        
        self.assertIsNotNone(self.node.localized_datetime)
        self.assertRegex(self.node.localized_datetime, r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} \w+")

    def test_remove_existing_timezone_info(self):
        # Test with datetime string that has timezone info - should be removed to make naive
        self.node.datetime_input = "2024-01-15T12:00:00+05:00"
        self.node.timezone = "UTC"
        self.node.format_output = "iso8601"
        
        self.node.execute()
        
        self.assertIsNotNone(self.node.localized_datetime)
        self.assertFalse(self.node.false_path)

    def test_remove_z_suffix(self):
        # Test with Z suffix - should be removed to make naive
        self.node.datetime_input = "2024-01-15T12:00:00Z"
        self.node.timezone = "America/Los_Angeles"
        self.node.format_output = "iso8601"
        
        self.node.execute()
        
        self.assertIsNotNone(self.node.localized_datetime)
        self.assertFalse(self.node.false_path)

    def test_invalid_timezone(self):
        self.node.datetime_input = "2024-01-15T12:00:00"
        self.node.timezone = "Invalid/Timezone"
        
        self.node.execute()
        
        self.assertIn("error", self.node.false_path)
        self.assertIsNone(self.node.localized_datetime)
        self.assertIsNone(self.node.timestamp_output)

    def test_invalid_datetime_input(self):
        self.node.datetime_input = "not a datetime"
        self.node.timezone = "UTC"
        
        self.node.execute()
        
        self.assertIn("error", self.node.false_path)
        self.assertIsNone(self.node.localized_datetime)
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
                self.node.timezone = "UTC"
                self.node.format_output = "iso8601"
                
                # Reset state
                self.node.false_path = False
                self.node.localized_datetime = None
                
                self.node.execute()
                
                self.assertIsNotNone(self.node.localized_datetime)
                self.assertFalse(self.node.false_path)

    def test_already_aware_datetime_object(self):
        # Test with actual datetime object that has timezone info
        aware_dt = datetime(2024, 1, 15, 12, 0, 0, tzinfo=pytz.UTC)
        self.node.datetime_input = aware_dt
        self.node.timezone = "America/New_York"
        self.node.format_output = "iso8601"
        
        self.node.execute()
        
        self.assertIsNotNone(self.node.localized_datetime)
        self.assertFalse(self.node.false_path)

    def test_daylight_saving_time_localization(self):
        # Test during DST period (July) and standard time (January)
        test_cases = [
            ("2024-07-15T12:00:00", "America/New_York"),  # EDT period
            ("2024-01-15T12:00:00", "America/New_York"),  # EST period
        ]
        
        for dt_input, timezone in test_cases:
            with self.subTest(datetime=dt_input, timezone=timezone):
                self.node.datetime_input = dt_input
                self.node.timezone = timezone
                self.node.format_output = "iso8601"
                
                # Reset state
                self.node.false_path = False
                self.node.localized_datetime = None
                
                self.node.execute()
                
                self.assertIsNotNone(self.node.localized_datetime)
                self.assertTrue("12:00:00" in self.node.localized_datetime)
                self.assertFalse(self.node.false_path)

    def test_parse_datetime_input_method(self):
        # Test the helper method directly
        test_dt = self.node.parse_datetime_input("2024-01-15T12:00:00+05:00")
        self.assertIsInstance(test_dt, datetime)
        self.assertEqual(test_dt.year, 2024)
        self.assertEqual(test_dt.hour, 12)
        self.assertIsNone(test_dt.tzinfo)  # Should be naive after processing

    def test_get_timezone_method(self):
        # Test the helper method directly
        utc_tz = self.node.get_timezone("UTC")
        self.assertEqual(utc_tz.zone, "UTC")
        
        # Test invalid timezone
        with self.assertRaises(ValueError):
            self.node.get_timezone("Invalid/Timezone")

    def test_format_datetime_method(self):
        # Test the helper method directly
        self.node.format_output = "iso8601"
        dt = datetime(2024, 1, 15, 12, 0, 0, tzinfo=pytz.UTC)
        formatted = self.node.format_datetime(dt)
        self.assertIn("2024-01-15", formatted)
        self.assertIn("12:00:00", formatted)

    def test_timezone_offset_parsing(self):
        # Test various timezone offset formats
        test_cases = [
            "2024-01-15T12:00:00+05:00",
            "2024-01-15T12:00:00-08:00", 
            "2024-01-15T12:00:00+0530",
        ]
        
        for dt_input in test_cases:
            with self.subTest(input=dt_input):
                self.node.datetime_input = dt_input
                self.node.timezone = "UTC"
                self.node.format_output = "iso8601"
                
                # Reset state
                self.node.false_path = False
                self.node.localized_datetime = None
                
                self.node.execute()
                
                self.assertIsNotNone(self.node.localized_datetime)
                self.assertFalse(self.node.false_path)


if __name__ == "__main__":
    unittest.main()