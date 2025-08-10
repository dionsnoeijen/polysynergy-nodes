import unittest
from datetime import datetime
from polysynergy_nodes.date_time.format_datetime import FormatDateTime


class TestFormatDateTime(unittest.TestCase):

    def setUp(self):
        self.node = FormatDateTime()
        self.node.false_path = False
        self.node.true_path = False
        self.node.formatted_datetime = None
        self.node.iso_format = None
        self.node.timestamp_output = None

    def test_iso_format_input_to_custom_format(self):
        self.node.datetime_input = "2024-01-15T12:30:45"
        self.node.format_string = "%Y-%m-%d %H:%M:%S"
        self.node.locale_code = ""
        
        self.node.execute()
        
        self.assertIsNotNone(self.node.formatted_datetime)
        self.assertEqual(self.node.formatted_datetime, "2024-01-15 12:30:45")
        self.assertIsNotNone(self.node.iso_format)
        self.assertIsInstance(self.node.timestamp_output, int)
        self.assertEqual(self.node.true_path, self.node.formatted_datetime)
        self.assertFalse(self.node.false_path)

    def test_predefined_iso8601_format(self):
        self.node.datetime_input = "2024-01-15T12:30:45"
        self.node.format_string = "iso8601"
        
        self.node.execute()
        
        self.assertIsNotNone(self.node.formatted_datetime)
        self.assertIn("2024-01-15", self.node.formatted_datetime)
        self.assertIn("12:30:45", self.node.formatted_datetime)
        self.assertFalse(self.node.false_path)

    def test_predefined_timestamp_format(self):
        self.node.datetime_input = "2024-01-15T12:30:45"
        self.node.format_string = "timestamp"
        
        self.node.execute()
        
        self.assertIsNotNone(self.node.formatted_datetime)
        self.assertTrue(self.node.formatted_datetime.isdigit())
        self.assertFalse(self.node.false_path)

    def test_predefined_rfc2822_format(self):
        self.node.datetime_input = "2024-01-15T12:30:45"
        self.node.format_string = "rfc2822"
        
        self.node.execute()
        
        self.assertIsNotNone(self.node.formatted_datetime)
        # RFC 2822 format: "Mon, 15 Jan 2024 12:30:45 "
        self.assertIn("Jan", self.node.formatted_datetime)
        self.assertIn("2024", self.node.formatted_datetime)
        self.assertFalse(self.node.false_path)

    def test_predefined_rfc3339_format(self):
        self.node.datetime_input = "2024-01-15T12:30:45"
        self.node.format_string = "rfc3339"
        
        self.node.execute()
        
        self.assertIsNotNone(self.node.formatted_datetime)
        self.assertIn("2024-01-15", self.node.formatted_datetime)
        self.assertIn("T", self.node.formatted_datetime)
        self.assertFalse(self.node.false_path)

    def test_date_only_output_format(self):
        self.node.datetime_input = "2024-01-15T12:30:45"
        self.node.format_string = "%Y-%m-%d"
        
        self.node.execute()
        
        self.assertEqual(self.node.formatted_datetime, "2024-01-15")
        self.assertFalse(self.node.false_path)

    def test_twelve_hour_format_with_am_pm(self):
        self.node.datetime_input = "2024-01-15T14:30:45"  # 2:30 PM
        self.node.format_string = "%b %d, %Y %I:%M %p"
        
        self.node.execute()
        
        self.assertIsNotNone(self.node.formatted_datetime)
        self.assertIn("Jan 15, 2024", self.node.formatted_datetime)
        self.assertIn("02:30 PM", self.node.formatted_datetime)
        self.assertFalse(self.node.false_path)

    def test_full_day_and_month_names(self):
        self.node.datetime_input = "2024-01-15T12:30:45"  # Monday
        self.node.format_string = "%A, %B %d, %Y"
        
        self.node.execute()
        
        self.assertIsNotNone(self.node.formatted_datetime)
        self.assertIn("Monday", self.node.formatted_datetime)
        self.assertIn("January", self.node.formatted_datetime)
        self.assertIn("15, 2024", self.node.formatted_datetime)
        self.assertFalse(self.node.false_path)

    def test_european_format(self):
        self.node.datetime_input = "2024-01-15T12:30:45"
        self.node.format_string = "%d/%m/%Y %H:%M"
        
        self.node.execute()
        
        self.assertEqual(self.node.formatted_datetime, "15/01/2024 12:30")
        self.assertFalse(self.node.false_path)

    def test_us_format(self):
        self.node.datetime_input = "2024-01-15T14:30:45"
        self.node.format_string = "%m/%d/%Y %I:%M %p"
        
        self.node.execute()
        
        self.assertEqual(self.node.formatted_datetime, "01/15/2024 02:30 PM")
        self.assertFalse(self.node.false_path)

    def test_unix_timestamp_input(self):
        # Unix timestamp for 2024-01-15 12:30:45 UTC (approximately)
        self.node.datetime_input = 1705320645
        self.node.format_string = "%Y-%m-%d %H:%M:%S"
        
        self.node.execute()
        
        self.assertIsNotNone(self.node.formatted_datetime)
        self.assertIn("2024-01", self.node.formatted_datetime)  # Should be around that date
        self.assertFalse(self.node.false_path)

    def test_timestamp_string_input(self):
        # Unix timestamp as string
        self.node.datetime_input = "1705320645"
        self.node.format_string = "%Y-%m-%d %H:%M:%S"
        
        self.node.execute()
        
        self.assertIsNotNone(self.node.formatted_datetime)
        self.assertFalse(self.node.false_path)

    def test_common_input_formats(self):
        test_formats = [
            "2024-01-15 12:30:45",
            "2024-01-15T12:30:45.123456",
            "2024-01-15T12:30:45Z",
            "01/15/2024 12:30:45",
            "15/01/2024",
        ]
        
        for input_format in test_formats:
            with self.subTest(format=input_format):
                self.node.datetime_input = input_format
                self.node.format_string = "%Y-%m-%d %H:%M:%S"
                
                # Reset state
                self.node.false_path = False
                self.node.formatted_datetime = None
                
                self.node.execute()
                
                self.assertIsNotNone(self.node.formatted_datetime)
                self.assertFalse(self.node.false_path)

    def test_datetime_object_input(self):
        # Test with actual datetime object
        dt_obj = datetime(2024, 1, 15, 12, 30, 45)
        self.node.datetime_input = dt_obj
        self.node.format_string = "%Y-%m-%d %H:%M:%S"
        
        self.node.execute()
        
        self.assertEqual(self.node.formatted_datetime, "2024-01-15 12:30:45")
        self.assertFalse(self.node.false_path)

    def test_invalid_datetime_input(self):
        self.node.datetime_input = "not a datetime"
        self.node.format_string = "%Y-%m-%d %H:%M:%S"
        
        self.node.execute()
        
        self.assertIn("error", self.node.false_path)
        self.assertIsNone(self.node.formatted_datetime)
        self.assertIsNone(self.node.timestamp_output)

    def test_invalid_format_string(self):
        self.node.datetime_input = "2024-01-15T12:30:45"
        self.node.format_string = "%X %Y"  # Invalid format specifier
        
        self.node.execute()
        
        # Should still work with some format specifiers, but might fail with others
        # This test checks that errors are handled gracefully
        if self.node.false_path:
            self.assertIn("error", self.node.false_path)

    def test_microseconds_handling(self):
        self.node.datetime_input = "2024-01-15T12:30:45.123456"
        self.node.format_string = "%Y-%m-%d %H:%M:%S.%f"
        
        self.node.execute()
        
        self.assertIsNotNone(self.node.formatted_datetime)
        self.assertIn("123456", self.node.formatted_datetime)
        self.assertFalse(self.node.false_path)

    def test_timezone_in_input(self):
        self.node.datetime_input = "2024-01-15T12:30:45+05:00"
        self.node.format_string = "%Y-%m-%d %H:%M:%S"
        
        self.node.execute()
        
        self.assertIsNotNone(self.node.formatted_datetime)
        # Should format the datetime part correctly
        self.assertIn("2024-01-15", self.node.formatted_datetime)
        self.assertFalse(self.node.false_path)

    def test_parse_datetime_input_method(self):
        # Test the helper method directly
        dt = self.node.parse_datetime_input("2024-01-15T12:30:45")
        self.assertIsInstance(dt, datetime)
        self.assertEqual(dt.year, 2024)
        self.assertEqual(dt.hour, 12)

    def test_format_datetime_method_custom(self):
        # Test the helper method directly
        self.node.format_string = "%Y-%m-%d %H:%M:%S"
        dt = datetime(2024, 1, 15, 12, 30, 45)
        formatted = self.node.format_datetime(dt)
        self.assertEqual(formatted, "2024-01-15 12:30:45")

    def test_format_datetime_method_iso8601(self):
        # Test the helper method directly
        self.node.format_string = "iso8601"
        dt = datetime(2024, 1, 15, 12, 30, 45)
        formatted = self.node.format_datetime(dt)
        self.assertIn("2024-01-15", formatted)
        self.assertIn("12:30:45", formatted)

    def test_iso_format_output_consistency(self):
        # Ensure iso_format output is always ISO regardless of format_string
        self.node.datetime_input = "2024-01-15T12:30:45"
        self.node.format_string = "%d/%m/%Y %H:%M"  # Different format
        
        self.node.execute()
        
        self.assertIsNotNone(self.node.iso_format)
        self.assertIn("2024-01-15", self.node.iso_format)
        self.assertIn("T", self.node.iso_format)
        self.assertIn("12:30:45", self.node.iso_format)
        # Formatted output should be different
        self.assertIn("15/01/2024", self.node.formatted_datetime)

    def test_leap_year_formatting(self):
        # Test February 29th in leap year
        self.node.datetime_input = "2024-02-29T12:00:00"
        self.node.format_string = "%B %d, %Y"
        
        self.node.execute()
        
        self.assertIsNotNone(self.node.formatted_datetime)
        self.assertEqual(self.node.formatted_datetime, "February 29, 2024")
        self.assertFalse(self.node.false_path)

    def test_edge_case_times(self):
        # Test formatting edge cases like midnight and end of year
        edge_cases = [
            ("2024-01-01T00:00:00", "New Year midnight"),
            ("2024-12-31T23:59:59", "End of year"),
            ("2024-07-04T12:00:00", "Independence Day noon"),
        ]
        
        for dt_input, description in edge_cases:
            with self.subTest(case=description):
                self.node.datetime_input = dt_input
                self.node.format_string = "%Y-%m-%d %H:%M:%S"
                
                # Reset state
                self.node.false_path = False
                self.node.formatted_datetime = None
                
                self.node.execute()
                
                self.assertIsNotNone(self.node.formatted_datetime)
                self.assertFalse(self.node.false_path)

    def test_float_timestamp_input(self):
        # Test float timestamp (Unix timestamp with fractional seconds)
        self.node.datetime_input = 1705320645.123
        self.node.format_string = "%Y-%m-%d %H:%M:%S"
        
        self.node.execute()
        
        self.assertIsNotNone(self.node.formatted_datetime)
        self.assertFalse(self.node.false_path)


if __name__ == "__main__":
    unittest.main()