import unittest
from unittest.mock import Mock
from datetime import datetime, time
from polysynergy_nodes.route.time_router import TimeRouter


class TestTimeRouter(unittest.TestCase):

    def setUp(self):
        self.node = TimeRouter()
        
        # Reset paths
        self.node.false_path = False
        
        # Mock connections with source_handle
        self.mock_connection_morning = Mock()
        self.mock_connection_morning.source_handle = "time_ranges.morning"
        self.mock_connection_morning.make_killer = Mock()
        
        self.mock_connection_afternoon = Mock()
        self.mock_connection_afternoon.source_handle = "time_ranges.afternoon"
        self.mock_connection_afternoon.make_killer = Mock()
        
        self.mock_connection_evening = Mock()
        self.mock_connection_evening.source_handle = "time_ranges.evening"
        self.mock_connection_evening.make_killer = Mock()
        
        self.mock_connection_night = Mock()
        self.mock_connection_night.source_handle = "time_ranges.night"
        self.mock_connection_night.make_killer = Mock()
        
        self.mock_connection_weekday = Mock()
        self.mock_connection_weekday.source_handle = "time_ranges.weekday"
        self.mock_connection_weekday.make_killer = Mock()
        
        self.mock_connection_weekend = Mock()
        self.mock_connection_weekend.source_handle = "time_ranges.weekend"
        self.mock_connection_weekend.make_killer = Mock()
        
        self.mock_connection_default = Mock()
        self.mock_connection_default.source_handle = "time_ranges.default"
        self.mock_connection_default.make_killer = Mock()

    def test_no_connections_triggers_false_path(self):
        self.node.out_connections = []
        self.node.datetime_value = datetime(2024, 1, 15, 10, 30)  # Monday morning
        
        self.node.execute()
        
        self.assertIn("error", self.node.false_path)

    def test_morning_time_routing(self):
        self.node.out_connections = [self.mock_connection_morning, self.mock_connection_afternoon]
        self.node.time_ranges = {"morning": None, "afternoon": None}
        self.node.datetime_value = datetime(2024, 1, 15, 8, 30)  # 8:30 AM
        
        self.node.execute()
        
        # Morning connection should not be killed
        self.mock_connection_morning.make_killer.assert_not_called()
        # Afternoon connection should be killed
        self.mock_connection_afternoon.make_killer.assert_called_once()
        # Value should be stored in morning
        self.assertEqual(self.node.time_ranges["morning"], datetime(2024, 1, 15, 8, 30))

    def test_afternoon_time_routing(self):
        self.node.out_connections = [self.mock_connection_morning, self.mock_connection_afternoon]
        self.node.time_ranges = {"morning": None, "afternoon": None}
        self.node.datetime_value = datetime(2024, 1, 15, 14, 30)  # 2:30 PM
        
        self.node.execute()
        
        # Afternoon connection should not be killed
        self.mock_connection_afternoon.make_killer.assert_not_called()
        # Morning connection should be killed
        self.mock_connection_morning.make_killer.assert_called_once()
        # Value should be stored in afternoon
        self.assertEqual(self.node.time_ranges["afternoon"], datetime(2024, 1, 15, 14, 30))

    def test_evening_time_routing(self):
        self.node.out_connections = [self.mock_connection_evening, self.mock_connection_night]
        self.node.time_ranges = {"evening": None, "night": None}
        self.node.datetime_value = datetime(2024, 1, 15, 19, 0)  # 7:00 PM
        
        self.node.execute()
        
        # Evening connection should not be killed
        self.mock_connection_evening.make_killer.assert_not_called()
        # Night connection should be killed
        self.mock_connection_night.make_killer.assert_called_once()
        # Value should be stored in evening
        self.assertEqual(self.node.time_ranges["evening"], datetime(2024, 1, 15, 19, 0))

    def test_night_time_routing(self):
        self.node.out_connections = [self.mock_connection_evening, self.mock_connection_night]
        self.node.time_ranges = {"evening": None, "night": None}
        self.node.datetime_value = datetime(2024, 1, 15, 23, 30)  # 11:30 PM
        
        self.node.execute()
        
        # Night connection should not be killed
        self.mock_connection_night.make_killer.assert_not_called()
        # Evening connection should be killed
        self.mock_connection_evening.make_killer.assert_called_once()
        # Value should be stored in night
        self.assertEqual(self.node.time_ranges["night"], datetime(2024, 1, 15, 23, 30))

    def test_weekday_routing(self):
        self.node.out_connections = [self.mock_connection_weekday, self.mock_connection_weekend]
        self.node.time_ranges = {"weekday": None, "weekend": None}
        self.node.datetime_value = datetime(2024, 1, 15, 10, 0)  # Monday
        
        self.node.execute()
        
        # Weekday connection should not be killed
        self.mock_connection_weekday.make_killer.assert_not_called()
        # Weekend connection should be killed
        self.mock_connection_weekend.make_killer.assert_called_once()
        # Value should be stored in weekday
        self.assertEqual(self.node.time_ranges["weekday"], datetime(2024, 1, 15, 10, 0))

    def test_weekend_routing(self):
        self.node.out_connections = [self.mock_connection_weekday, self.mock_connection_weekend]
        self.node.time_ranges = {"weekday": None, "weekend": None}
        self.node.datetime_value = datetime(2024, 1, 13, 10, 0)  # Saturday
        
        self.node.execute()
        
        # Weekend connection should not be killed
        self.mock_connection_weekend.make_killer.assert_not_called()
        # Weekday connection should be killed
        self.mock_connection_weekday.make_killer.assert_called_once()
        # Value should be stored in weekend
        self.assertEqual(self.node.time_ranges["weekend"], datetime(2024, 1, 13, 10, 0))

    def test_priority_time_of_day_over_day_type(self):
        # When both time of day and day type ranges exist, time of day should have priority
        self.node.out_connections = [self.mock_connection_morning, self.mock_connection_weekday]
        self.node.time_ranges = {"morning": None, "weekday": None}
        self.node.datetime_value = datetime(2024, 1, 15, 8, 0)  # Monday morning
        
        self.node.execute()
        
        # Morning should be chosen over weekday (priority)
        self.mock_connection_morning.make_killer.assert_not_called()
        self.mock_connection_weekday.make_killer.assert_called_once()
        self.assertEqual(self.node.time_ranges["morning"], datetime(2024, 1, 15, 8, 0))

    def test_unix_timestamp_parsing(self):
        self.node.out_connections = [self.mock_connection_morning, self.mock_connection_afternoon]
        self.node.time_ranges = {"morning": None, "afternoon": None}
        # Unix timestamp for 2024-01-15 08:30:00
        self.node.datetime_value = 1705309800
        
        self.node.execute()
        
        # Morning connection should not be killed
        self.mock_connection_morning.make_killer.assert_not_called()
        # Afternoon connection should be killed
        self.mock_connection_afternoon.make_killer.assert_called_once()
        # Original timestamp should be stored
        self.assertEqual(self.node.time_ranges["morning"], 1705309800)

    def test_iso_string_parsing(self):
        self.node.out_connections = [self.mock_connection_afternoon, self.mock_connection_evening]
        self.node.time_ranges = {"afternoon": None, "evening": None}
        self.node.datetime_value = "2024-01-15T14:30:00"
        
        self.node.execute()
        
        # Afternoon connection should not be killed
        self.mock_connection_afternoon.make_killer.assert_not_called()
        # Evening connection should be killed
        self.mock_connection_evening.make_killer.assert_called_once()
        # Original string should be stored
        self.assertEqual(self.node.time_ranges["afternoon"], "2024-01-15T14:30:00")

    def test_common_string_formats(self):
        # Test various string formats
        test_cases = [
            ("2024-01-15 14:30:00", "afternoon"),
            ("2024-01-15", "default"),  # Date only, would need time for specific routing
            ("14:30:00", "afternoon"),
            ("14:30", "afternoon")
        ]
        
        for datetime_str, expected_range in test_cases:
            with self.subTest(datetime_str=datetime_str):
                self.node.out_connections = [self.mock_connection_afternoon, self.mock_connection_default]
                self.node.time_ranges = {"afternoon": None, "default": None}
                self.node.datetime_value = datetime_str
                
                # Reset mocks
                self.mock_connection_afternoon.make_killer.reset_mock()
                self.mock_connection_default.make_killer.reset_mock()
                
                self.node.execute()
                
                if expected_range == "afternoon":
                    self.mock_connection_afternoon.make_killer.assert_not_called()
                    self.assertEqual(self.node.time_ranges["afternoon"], datetime_str)
                else:
                    self.mock_connection_default.make_killer.assert_not_called()
                    self.assertEqual(self.node.time_ranges["default"], datetime_str)

    def test_invalid_datetime_uses_default(self):
        self.node.out_connections = [self.mock_connection_morning, self.mock_connection_default]
        self.node.time_ranges = {"morning": None, "default": None}
        self.node.datetime_value = "invalid datetime string"
        
        self.node.execute()
        
        # Default connection should be chosen
        self.mock_connection_default.make_killer.assert_not_called()
        # Morning connection should be killed
        self.mock_connection_morning.make_killer.assert_called_once()
        # Original value should be stored in default
        self.assertEqual(self.node.time_ranges["default"], "invalid datetime string")

    def test_invalid_datetime_no_default_triggers_false_path(self):
        self.node.out_connections = [self.mock_connection_morning, self.mock_connection_afternoon]
        self.node.time_ranges = {"morning": None, "afternoon": None}
        self.node.datetime_value = "invalid datetime string"
        
        self.node.execute()
        
        # All connections should be killed
        self.mock_connection_morning.make_killer.assert_called_once()
        self.mock_connection_afternoon.make_killer.assert_called_once()
        # Should trigger false path
        self.assertIn("error", self.node.false_path)

    def test_no_matching_time_range_uses_default(self):
        # When only weekend range exists but it's a weekday morning
        self.node.out_connections = [self.mock_connection_weekend, self.mock_connection_default]
        self.node.time_ranges = {"weekend": None, "default": None}
        self.node.datetime_value = datetime(2024, 1, 15, 10, 0)  # Monday
        
        self.node.execute()
        
        # Default should be chosen
        self.mock_connection_default.make_killer.assert_not_called()
        # Weekend connection should be killed
        self.mock_connection_weekend.make_killer.assert_called_once()
        # Original value should be stored in default
        self.assertEqual(self.node.time_ranges["default"], datetime(2024, 1, 15, 10, 0))

    def test_parse_datetime_method(self):
        # Test datetime parsing method directly
        dt = datetime(2024, 1, 15, 10, 30)
        self.assertEqual(self.node._parse_datetime(dt), dt)
        
        # Unix timestamp
        self.assertIsNotNone(self.node._parse_datetime(1705309800))
        
        # ISO string
        result = self.node._parse_datetime("2024-01-15T14:30:00")
        self.assertIsInstance(result, datetime)
        self.assertEqual(result.hour, 14)
        
        # Other formats
        self.assertIsNotNone(self.node._parse_datetime("2024-01-15 14:30:00"))
        self.assertIsNotNone(self.node._parse_datetime("2024-01-15"))
        self.assertIsNotNone(self.node._parse_datetime("14:30:00"))
        self.assertIsNotNone(self.node._parse_datetime("14:30"))
        
        # Invalid formats
        self.assertIsNone(self.node._parse_datetime("invalid"))
        self.assertIsNone(self.node._parse_datetime(None))

    def test_get_time_category_method(self):
        # Test time categorization method directly
        
        # Morning (5-11)
        self.assertEqual(self.node._get_time_category(datetime(2024, 1, 15, 8, 0)), "morning")
        
        # Afternoon (12-16)  
        self.assertEqual(self.node._get_time_category(datetime(2024, 1, 15, 14, 0)), "afternoon")
        
        # Evening (17-20)
        self.assertEqual(self.node._get_time_category(datetime(2024, 1, 15, 19, 0)), "evening")
        
        # Night (21-4)
        self.assertEqual(self.node._get_time_category(datetime(2024, 1, 15, 23, 0)), "night")
        self.assertEqual(self.node._get_time_category(datetime(2024, 1, 15, 2, 0)), "night")
        
        # Test priority: time_of_day available in ranges
        self.node.time_ranges = {"morning": None}
        self.assertEqual(self.node._get_time_category(datetime(2024, 1, 15, 8, 0)), "morning")
        
        # Test fallback to day_type when time_of_day not available
        self.node.time_ranges = {"weekday": None}
        self.assertEqual(self.node._get_time_category(datetime(2024, 1, 15, 8, 0)), "weekday")  # Monday
        
        # Test fallback to default when neither available
        self.node.time_ranges = {"some_other": None}
        self.assertEqual(self.node._get_time_category(datetime(2024, 1, 15, 8, 0)), "default")


if __name__ == "__main__":
    unittest.main()