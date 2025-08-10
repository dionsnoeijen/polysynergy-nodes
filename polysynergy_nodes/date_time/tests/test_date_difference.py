import unittest
from datetime import datetime
from polysynergy_nodes.date_time.date_difference import DateDifference


class TestDateDifference(unittest.TestCase):

    def setUp(self):
        self.node = DateDifference()
        self.node.false_path = False
        self.node.true_path = False
        self.node.total_seconds = None
        self.node.total_minutes = None
        self.node.total_hours = None
        self.node.total_days = None
        self.node.absolute_difference = None
        self.node.human_readable = None

    def test_positive_difference_in_hours(self):
        self.node.start_datetime = "2024-01-15T12:00:00"
        self.node.end_datetime = "2024-01-15T15:00:00"  # 3 hours later
        
        self.node.execute()
        
        self.assertEqual(self.node.total_seconds, 10800.0)  # 3 hours = 10800 seconds
        self.assertEqual(self.node.total_minutes, 180.0)    # 3 hours = 180 minutes
        self.assertEqual(self.node.total_hours, 3.0)        # 3 hours
        self.assertEqual(self.node.total_days, 0.125)       # 3/24 = 0.125 days
        self.assertEqual(self.node.absolute_difference, 10800.0)
        self.assertIn("3.0 hours", self.node.human_readable)
        self.assertFalse(self.node.false_path)

    def test_negative_difference_in_hours(self):
        self.node.start_datetime = "2024-01-15T15:00:00"
        self.node.end_datetime = "2024-01-15T12:00:00"  # 3 hours earlier
        
        self.node.execute()
        
        self.assertEqual(self.node.total_seconds, -10800.0)  # Negative 3 hours
        self.assertEqual(self.node.total_minutes, -180.0)    # Negative 180 minutes
        self.assertEqual(self.node.total_hours, -3.0)        # Negative 3 hours
        self.assertEqual(self.node.total_days, -0.125)       # Negative days
        self.assertEqual(self.node.absolute_difference, 10800.0)  # Always positive
        self.assertIn("-3.0 hours", self.node.human_readable)
        self.assertFalse(self.node.false_path)

    def test_difference_in_days(self):
        self.node.start_datetime = "2024-01-15T12:00:00"
        self.node.end_datetime = "2024-01-20T12:00:00"  # 5 days later
        
        self.node.execute()
        
        expected_seconds = 5 * 24 * 3600  # 5 days in seconds
        self.assertEqual(self.node.total_seconds, float(expected_seconds))
        self.assertEqual(self.node.total_days, 5.0)
        self.assertIn("5.0 days", self.node.human_readable)
        self.assertFalse(self.node.false_path)

    def test_difference_in_minutes(self):
        self.node.start_datetime = "2024-01-15T12:00:00"
        self.node.end_datetime = "2024-01-15T12:45:00"  # 45 minutes later
        
        self.node.execute()
        
        self.assertEqual(self.node.total_seconds, 2700.0)  # 45 minutes = 2700 seconds
        self.assertEqual(self.node.total_minutes, 45.0)
        self.assertIn("45.0 minutes", self.node.human_readable)
        self.assertFalse(self.node.false_path)

    def test_difference_in_seconds(self):
        self.node.start_datetime = "2024-01-15T12:00:00"
        self.node.end_datetime = "2024-01-15T12:00:30"  # 30 seconds later
        
        self.node.execute()
        
        self.assertEqual(self.node.total_seconds, 30.0)
        self.assertIn("30.0 seconds", self.node.human_readable)
        self.assertFalse(self.node.false_path)

    def test_zero_difference(self):
        self.node.start_datetime = "2024-01-15T12:00:00"
        self.node.end_datetime = "2024-01-15T12:00:00"  # Same time
        
        self.node.execute()
        
        self.assertEqual(self.node.total_seconds, 0.0)
        self.assertEqual(self.node.total_minutes, 0.0)
        self.assertEqual(self.node.total_hours, 0.0)
        self.assertEqual(self.node.total_days, 0.0)
        self.assertEqual(self.node.absolute_difference, 0.0)
        self.assertIn("0.0 seconds", self.node.human_readable)
        self.assertFalse(self.node.false_path)

    def test_iso_input_with_z_suffix(self):
        self.node.start_datetime = "2024-01-15T12:00:00Z"
        self.node.end_datetime = "2024-01-15T13:00:00Z"
        
        self.node.execute()
        
        self.assertEqual(self.node.total_hours, 1.0)
        self.assertIn("1.0 hours", self.node.human_readable)
        self.assertFalse(self.node.false_path)

    def test_common_datetime_input_formats(self):
        test_formats = [
            ("2024-01-15 12:00:00", "2024-01-15 13:00:00"),
            ("2024-01-15T12:00:00.123456", "2024-01-15T13:00:00.123456"),
            ("2024-01-15", "2024-01-16"),
        ]
        
        for start_format, end_format in test_formats:
            with self.subTest(start=start_format, end=end_format):
                self.node.start_datetime = start_format
                self.node.end_datetime = end_format
                
                # Reset state
                self.node.false_path = False
                self.node.total_seconds = None
                
                self.node.execute()
                
                self.assertIsNotNone(self.node.total_seconds)
                self.assertTrue(self.node.total_seconds > 0)  # All test cases are positive differences
                self.assertFalse(self.node.false_path)

    def test_cross_day_boundary_difference(self):
        self.node.start_datetime = "2024-01-15T23:30:00"
        self.node.end_datetime = "2024-01-16T01:30:00"  # 2 hours later, next day
        
        self.node.execute()
        
        self.assertEqual(self.node.total_hours, 2.0)
        self.assertIn("2.0 hours", self.node.human_readable)
        self.assertFalse(self.node.false_path)

    def test_cross_month_boundary_difference(self):
        self.node.start_datetime = "2024-01-30T12:00:00"
        self.node.end_datetime = "2024-02-02T12:00:00"  # 3 days later, next month
        
        self.node.execute()
        
        self.assertEqual(self.node.total_days, 3.0)
        self.assertIn("3.0 days", self.node.human_readable)
        self.assertFalse(self.node.false_path)

    def test_leap_year_handling(self):
        # Test February 29th in leap year 2024
        self.node.start_datetime = "2024-02-28T12:00:00"
        self.node.end_datetime = "2024-03-01T12:00:00"  # Crosses leap day
        
        self.node.execute()
        
        self.assertEqual(self.node.total_days, 2.0)  # Feb 28 -> Feb 29 -> Mar 1 = 2 days
        self.assertFalse(self.node.false_path)

    def test_large_time_difference(self):
        # Test difference across a year
        self.node.start_datetime = "2024-01-15T12:00:00"
        self.node.end_datetime = "2025-01-15T12:00:00"  # Exactly one year later
        
        self.node.execute()
        
        # 2024 is a leap year, so 366 days
        self.assertEqual(self.node.total_days, 366.0)
        self.assertIn("366.0 days", self.node.human_readable)
        self.assertFalse(self.node.false_path)

    def test_microseconds_difference(self):
        self.node.start_datetime = "2024-01-15T12:00:00.123456"
        self.node.end_datetime = "2024-01-15T12:00:00.623456"  # 0.5 seconds later
        
        self.node.execute()
        
        self.assertEqual(self.node.total_seconds, 0.5)
        self.assertIn("0.5 seconds", self.node.human_readable)
        self.assertFalse(self.node.false_path)

    def test_invalid_start_datetime(self):
        self.node.start_datetime = "not a datetime"
        self.node.end_datetime = "2024-01-15T12:00:00"
        
        self.node.execute()
        
        self.assertIn("error", self.node.false_path)
        self.assertIsNone(self.node.total_seconds)
        self.assertIsNone(self.node.human_readable)

    def test_invalid_end_datetime(self):
        self.node.start_datetime = "2024-01-15T12:00:00"
        self.node.end_datetime = "not a datetime"
        
        self.node.execute()
        
        self.assertIn("error", self.node.false_path)
        self.assertIsNone(self.node.total_seconds)
        self.assertIsNone(self.node.human_readable)

    def test_parse_datetime_input_method(self):
        # Test the helper method directly
        dt = self.node.parse_datetime_input("2024-01-15T12:00:00")
        self.assertIsInstance(dt, datetime)
        self.assertEqual(dt.year, 2024)
        self.assertEqual(dt.hour, 12)

    def test_format_human_readable_method(self):
        # Test the helper method directly
        
        # Test seconds
        result = self.node.format_human_readable(45.0)
        self.assertEqual(result, "45.0 seconds")
        
        # Test minutes
        result = self.node.format_human_readable(150.0)  # 2.5 minutes
        self.assertEqual(result, "2.5 minutes")
        
        # Test hours
        result = self.node.format_human_readable(7200.0)  # 2 hours
        self.assertEqual(result, "2.0 hours")
        
        # Test days
        result = self.node.format_human_readable(172800.0)  # 2 days
        self.assertEqual(result, "2.0 days")

    def test_fractional_time_units(self):
        # Test 1.5 hours difference
        self.node.start_datetime = "2024-01-15T12:00:00"
        self.node.end_datetime = "2024-01-15T13:30:00"  # 1.5 hours later
        
        self.node.execute()
        
        self.assertEqual(self.node.total_hours, 1.5)
        self.assertEqual(self.node.total_minutes, 90.0)
        self.assertIn("1.5 hours", self.node.human_readable)
        self.assertFalse(self.node.false_path)

    def test_datetime_object_input(self):
        # Test with actual datetime objects
        start_dt = datetime(2024, 1, 15, 12, 0, 0)
        end_dt = datetime(2024, 1, 15, 15, 0, 0)
        
        self.node.start_datetime = start_dt
        self.node.end_datetime = end_dt
        
        self.node.execute()
        
        self.assertEqual(self.node.total_hours, 3.0)
        self.assertFalse(self.node.false_path)


if __name__ == "__main__":
    unittest.main()