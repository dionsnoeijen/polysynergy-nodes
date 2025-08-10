import unittest
from datetime import datetime
from polysynergy_nodes.date_time.parse_datetime import ParseDateTime


class TestParseDateTime(unittest.TestCase):

    def setUp(self):
        self.node = ParseDateTime()
        self.node.false_path = False
        self.node.true_path = False
        self.node.parsed_datetime = None
        self.node.timestamp_output = None
        self.node.year = None
        self.node.month = None
        self.node.day = None
        self.node.hour = None
        self.node.minute = None
        self.node.second = None

    def test_iso_format_parsing(self):
        self.node.datetime_string = "2024-01-15T12:30:45"
        self.node.format_string = ""  # Auto-detect
        self.node.output_format = "iso8601"
        
        self.node.execute()
        
        self.assertIsNotNone(self.node.parsed_datetime)
        self.assertEqual(self.node.year, 2024)
        self.assertEqual(self.node.month, 1)
        self.assertEqual(self.node.day, 15)
        self.assertEqual(self.node.hour, 12)
        self.assertEqual(self.node.minute, 30)
        self.assertEqual(self.node.second, 45)
        self.assertIsInstance(self.node.timestamp_output, int)
        self.assertEqual(self.node.true_path, self.node.parsed_datetime)
        self.assertFalse(self.node.false_path)

    def test_iso_format_with_z_suffix(self):
        self.node.datetime_string = "2024-01-15T12:30:45Z"
        self.node.format_string = ""
        self.node.output_format = "iso8601"
        
        self.node.execute()
        
        self.assertIsNotNone(self.node.parsed_datetime)
        self.assertEqual(self.node.year, 2024)
        self.assertEqual(self.node.hour, 12)
        self.assertFalse(self.node.false_path)

    def test_iso_format_with_timezone_offset(self):
        self.node.datetime_string = "2024-01-15T12:30:45+05:00"
        self.node.format_string = ""
        self.node.output_format = "iso8601"
        
        self.node.execute()
        
        self.assertIsNotNone(self.node.parsed_datetime)
        self.assertEqual(self.node.year, 2024)
        self.assertEqual(self.node.hour, 12)
        self.assertFalse(self.node.false_path)

    def test_custom_format_string(self):
        self.node.datetime_string = "15/01/2024 12:30:45"
        self.node.format_string = "%d/%m/%Y %H:%M:%S"
        self.node.output_format = "iso8601"
        
        self.node.execute()
        
        self.assertIsNotNone(self.node.parsed_datetime)
        self.assertEqual(self.node.year, 2024)
        self.assertEqual(self.node.month, 1)
        self.assertEqual(self.node.day, 15)
        self.assertEqual(self.node.hour, 12)
        self.assertFalse(self.node.false_path)

    def test_us_date_format_auto_detection(self):
        self.node.datetime_string = "01/15/2024 2:30:45 PM"
        self.node.format_string = ""  # Auto-detect
        self.node.output_format = "iso8601"
        
        self.node.execute()
        
        self.assertIsNotNone(self.node.parsed_datetime)
        self.assertEqual(self.node.year, 2024)
        self.assertEqual(self.node.month, 1)
        self.assertEqual(self.node.day, 15)
        self.assertEqual(self.node.hour, 14)  # 2:30 PM = 14:30
        self.assertFalse(self.node.false_path)

    def test_european_date_format_auto_detection(self):
        self.node.datetime_string = "15/01/2024"
        self.node.format_string = ""  # Auto-detect
        self.node.output_format = "iso8601"
        
        self.node.execute()
        
        self.assertIsNotNone(self.node.parsed_datetime)
        self.assertEqual(self.node.year, 2024)
        self.assertEqual(self.node.month, 1)
        self.assertEqual(self.node.day, 15)
        self.assertFalse(self.node.false_path)

    def test_date_only_formats(self):
        test_formats = [
            "2024-01-15",
            "January 15, 2024",
            "Jan 15, 2024",
            "15 January 2024",
            "15 Jan 2024",
        ]
        
        for date_str in test_formats:
            with self.subTest(format=date_str):
                self.node.datetime_string = date_str
                self.node.format_string = ""
                self.node.output_format = "iso8601"
                
                # Reset state
                self.node.false_path = False
                self.node.parsed_datetime = None
                
                self.node.execute()
                
                self.assertIsNotNone(self.node.parsed_datetime)
                self.assertEqual(self.node.year, 2024)
                self.assertEqual(self.node.month, 1)
                self.assertEqual(self.node.day, 15)
                self.assertFalse(self.node.false_path)

    def test_time_only_formats(self):
        test_formats = [
            "12:30:45",
            "12:30",
            "2:30:45 PM",
            "2:30 PM",
        ]
        
        for time_str in test_formats:
            with self.subTest(format=time_str):
                self.node.datetime_string = time_str
                self.node.format_string = ""
                self.node.output_format = "iso8601"
                
                # Reset state
                self.node.false_path = False
                self.node.parsed_datetime = None
                
                self.node.execute()
                
                self.assertIsNotNone(self.node.parsed_datetime)
                # Time-only formats will have today's date
                self.assertFalse(self.node.false_path)

    def test_timestamp_parsing(self):
        # Unix timestamp for 2024-01-15 12:30:45 UTC
        self.node.datetime_string = "1705320645"
        self.node.format_string = ""  # Auto-detect
        self.node.output_format = "iso8601"
        
        self.node.execute()
        
        self.assertIsNotNone(self.node.parsed_datetime)
        self.assertFalse(self.node.false_path)

    def test_compact_timestamp_formats(self):
        test_formats = [
            "20240115",      # YYYYMMDD
            "20240115123045", # YYYYMMDDHHMMSS
        ]
        
        for ts_format in test_formats:
            with self.subTest(format=ts_format):
                self.node.datetime_string = ts_format
                self.node.format_string = ""
                self.node.output_format = "iso8601"
                
                # Reset state
                self.node.false_path = False
                self.node.parsed_datetime = None
                
                self.node.execute()
                
                self.assertIsNotNone(self.node.parsed_datetime)
                self.assertEqual(self.node.year, 2024)
                self.assertEqual(self.node.month, 1)
                self.assertEqual(self.node.day, 15)
                self.assertFalse(self.node.false_path)

    def test_custom_output_format(self):
        self.node.datetime_string = "2024-01-15T12:30:45"
        self.node.format_string = ""
        self.node.output_format = "%Y-%m-%d %H:%M:%S"
        
        self.node.execute()
        
        self.assertIsNotNone(self.node.parsed_datetime)
        self.assertRegex(self.node.parsed_datetime, r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")
        self.assertEqual(self.node.true_path, self.node.parsed_datetime)

    def test_microseconds_handling(self):
        self.node.datetime_string = "2024-01-15T12:30:45.123456"
        self.node.format_string = ""
        self.node.output_format = "iso8601"
        
        self.node.execute()
        
        self.assertIsNotNone(self.node.parsed_datetime)
        self.assertEqual(self.node.year, 2024)
        self.assertEqual(self.node.second, 45)
        # Microseconds should be parsed correctly
        self.assertFalse(self.node.false_path)

    def test_invalid_datetime_string(self):
        self.node.datetime_string = "not a valid datetime"
        self.node.format_string = ""
        
        self.node.execute()
        
        self.assertIn("error", self.node.false_path)
        self.assertIsNone(self.node.parsed_datetime)
        self.assertIsNone(self.node.timestamp_output)
        self.assertIsNone(self.node.year)

    def test_invalid_custom_format(self):
        self.node.datetime_string = "2024-01-15T12:30:45"
        self.node.format_string = "%d/%m/%Y"  # Wrong format for the input
        
        self.node.execute()
        
        self.assertIn("error", self.node.false_path)
        self.assertIsNone(self.node.parsed_datetime)

    def test_custom_format_with_wrong_input(self):
        self.node.datetime_string = "15/01/2024"
        self.node.format_string = "%Y-%m-%d"  # Wrong format
        
        self.node.execute()
        
        self.assertIn("error", self.node.false_path)
        self.assertIsNone(self.node.parsed_datetime)

    def test_auto_parse_datetime_method(self):
        # Test the helper method directly
        dt = self.node.auto_parse_datetime("2024-01-15T12:30:45")
        self.assertIsInstance(dt, datetime)
        self.assertEqual(dt.year, 2024)
        self.assertEqual(dt.hour, 12)

    def test_parse_with_format_method(self):
        # Test the helper method directly
        dt = self.node.parse_with_format("15/01/2024", "%d/%m/%Y")
        self.assertIsInstance(dt, datetime)
        self.assertEqual(dt.year, 2024)
        self.assertEqual(dt.month, 1)
        self.assertEqual(dt.day, 15)

    def test_format_datetime_method(self):
        # Test the helper method directly
        self.node.output_format = "iso8601"
        dt = datetime(2024, 1, 15, 12, 30, 45)
        formatted = self.node.format_datetime(dt)
        self.assertIn("2024-01-15", formatted)
        self.assertIn("12:30:45", formatted)

    def test_component_extraction(self):
        # Test that all date/time components are correctly extracted
        self.node.datetime_string = "2024-12-31T23:59:59"
        self.node.format_string = ""
        self.node.output_format = "iso8601"
        
        self.node.execute()
        
        self.assertEqual(self.node.year, 2024)
        self.assertEqual(self.node.month, 12)
        self.assertEqual(self.node.day, 31)
        self.assertEqual(self.node.hour, 23)
        self.assertEqual(self.node.minute, 59)
        self.assertEqual(self.node.second, 59)
        self.assertFalse(self.node.false_path)

    def test_leap_year_date(self):
        # Test February 29th in leap year
        self.node.datetime_string = "2024-02-29T12:00:00"
        self.node.format_string = ""
        self.node.output_format = "iso8601"
        
        self.node.execute()
        
        self.assertIsNotNone(self.node.parsed_datetime)
        self.assertEqual(self.node.year, 2024)
        self.assertEqual(self.node.month, 2)
        self.assertEqual(self.node.day, 29)
        self.assertFalse(self.node.false_path)

    def test_edge_case_times(self):
        # Test edge cases like midnight and noon
        edge_cases = [
            ("2024-01-15T00:00:00", 0, 0, 0),  # Midnight
            ("2024-01-15T12:00:00", 12, 0, 0), # Noon
            ("2024-01-15T23:59:59", 23, 59, 59), # End of day
        ]
        
        for dt_str, expected_hour, expected_minute, expected_second in edge_cases:
            with self.subTest(datetime=dt_str):
                self.node.datetime_string = dt_str
                self.node.format_string = ""
                self.node.output_format = "iso8601"
                
                # Reset state
                self.node.false_path = False
                self.node.hour = None
                
                self.node.execute()
                
                self.assertEqual(self.node.hour, expected_hour)
                self.assertEqual(self.node.minute, expected_minute)
                self.assertEqual(self.node.second, expected_second)
                self.assertFalse(self.node.false_path)


if __name__ == "__main__":
    unittest.main()