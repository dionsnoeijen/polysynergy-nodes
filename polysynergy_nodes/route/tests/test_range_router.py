import unittest
from unittest.mock import Mock
from polysynergy_nodes.route.range_router import RangeRouter


class TestRangeRouter(unittest.TestCase):

    def setUp(self):
        self.node = RangeRouter()
        
        # Reset paths
        self.node.false_path = False
        
        # Mock connections with source_handle
        self.mock_connection_low = Mock()
        self.mock_connection_low.source_handle = "ranges.0-50"
        self.mock_connection_low.make_killer = Mock()
        
        self.mock_connection_high = Mock()
        self.mock_connection_high.source_handle = "ranges.51-100"
        self.mock_connection_high.make_killer = Mock()
        
        self.mock_connection_negative = Mock()
        self.mock_connection_negative.source_handle = "ranges.<0"
        self.mock_connection_negative.make_killer = Mock()
        
        self.mock_connection_default = Mock()
        self.mock_connection_default.source_handle = "ranges.default"
        self.mock_connection_default.make_killer = Mock()

    def test_no_connections_triggers_false_path(self):
        self.node.out_connections = []
        self.node.value = 25
        
        self.node.execute()
        
        self.assertIn("error", self.node.false_path)

    def test_range_match_0_to_100(self):
        self.node.out_connections = [self.mock_connection_low, self.mock_connection_high]
        self.node.ranges = {"0-50": None, "51-100": None}
        self.node.value = 25
        
        self.node.execute()
        
        # Low range connection should not be killed
        self.mock_connection_low.make_killer.assert_not_called()
        # High range connection should be killed
        self.mock_connection_high.make_killer.assert_called_once()
        # Value should be stored in the low range
        self.assertEqual(self.node.ranges["0-50"], 25)

    def test_range_match_boundary_inclusive(self):
        self.node.out_connections = [self.mock_connection_low, self.mock_connection_high]
        self.node.ranges = {"0-50": None, "51-100": None}
        self.node.value = 50  # Test boundary
        
        self.node.execute()
        
        # Low range connection should not be killed (50 is included in 0-50)
        self.mock_connection_low.make_killer.assert_not_called()
        # High range connection should be killed
        self.mock_connection_high.make_killer.assert_called_once()
        # Value should be stored in the low range
        self.assertEqual(self.node.ranges["0-50"], 50)

    def test_greater_than_condition(self):
        self.node.out_connections = [self.mock_connection_low, self.mock_connection_high]
        self.node.ranges = {">50": None, "<=50": None}
        self.node.value = 75
        
        self.node.execute()
        
        # Greater than connection should not be killed
        self.mock_connection_low.make_killer.assert_not_called()
        # Less than or equal connection should be killed
        self.mock_connection_high.make_killer.assert_called_once()
        # Value should be stored in the greater than range
        self.assertEqual(self.node.ranges[">50"], 75)

    def test_less_than_condition(self):
        self.node.out_connections = [self.mock_connection_negative, self.mock_connection_low]
        self.node.ranges = {"<0": None, ">=0": None}
        self.node.value = -10
        
        self.node.execute()
        
        # Less than connection should not be killed
        self.mock_connection_negative.make_killer.assert_not_called()
        # Greater than or equal connection should be killed
        self.mock_connection_low.make_killer.assert_called_once()
        # Value should be stored in the less than range
        self.assertEqual(self.node.ranges["<0"], -10)

    def test_greater_than_or_equal_condition(self):
        self.node.out_connections = [self.mock_connection_low, self.mock_connection_high]
        self.node.ranges = {">=50": None, "<50": None}
        self.node.value = 50  # Test boundary
        
        self.node.execute()
        
        # Greater than or equal connection should not be killed
        self.mock_connection_low.make_killer.assert_not_called()
        # Less than connection should be killed
        self.mock_connection_high.make_killer.assert_called_once()
        # Value should be stored in the greater than or equal range
        self.assertEqual(self.node.ranges[">=50"], 50)

    def test_less_than_or_equal_condition(self):
        self.node.out_connections = [self.mock_connection_low, self.mock_connection_high]
        self.node.ranges = {"<=50": None, ">50": None}
        self.node.value = 50  # Test boundary
        
        self.node.execute()
        
        # Less than or equal connection should not be killed
        self.mock_connection_low.make_killer.assert_not_called()
        # Greater than connection should be killed
        self.mock_connection_high.make_killer.assert_called_once()
        # Value should be stored in the less than or equal range
        self.assertEqual(self.node.ranges["<=50"], 50)

    def test_exact_value_condition(self):
        self.node.out_connections = [self.mock_connection_low, self.mock_connection_high]
        self.node.ranges = {"==42": None, "!=42": None}
        self.node.value = 42
        
        self.node.execute()
        
        # Exact value connection should not be killed
        self.mock_connection_low.make_killer.assert_not_called()
        # Not equal connection should be killed
        self.mock_connection_high.make_killer.assert_called_once()
        # Value should be stored in the exact value range
        self.assertEqual(self.node.ranges["==42"], 42)

    def test_default_case_when_no_match(self):
        self.node.out_connections = [self.mock_connection_low, self.mock_connection_default]
        self.node.ranges = {"0-50": None, "default": None}
        self.node.value = 75  # Out of range
        
        self.node.execute()
        
        # Default connection should be chosen
        self.mock_connection_default.make_killer.assert_not_called()
        # Other connections should be killed
        self.mock_connection_low.make_killer.assert_called_once()
        # Value should be stored in default case
        self.assertEqual(self.node.ranges["default"], 75)

    def test_non_numeric_value_uses_default(self):
        self.node.out_connections = [self.mock_connection_low, self.mock_connection_default]
        self.node.ranges = {"0-50": None, "default": None}
        self.node.value = "not a number"
        
        self.node.execute()
        
        # Default connection should be chosen
        self.mock_connection_default.make_killer.assert_not_called()
        # Other connections should be killed
        self.mock_connection_low.make_killer.assert_called_once()
        # Value should be stored in default case
        self.assertEqual(self.node.ranges["default"], "not a number")

    def test_non_numeric_value_no_default_triggers_false_path(self):
        self.node.out_connections = [self.mock_connection_low, self.mock_connection_high]
        self.node.ranges = {"0-50": None, "51-100": None}
        self.node.value = "not a number"
        
        self.node.execute()
        
        # All connections should be killed
        self.mock_connection_low.make_killer.assert_called_once()
        self.mock_connection_high.make_killer.assert_called_once()
        # Should trigger false path
        self.assertIn("error", self.node.false_path)

    def test_no_match_no_default_triggers_false_path(self):
        self.node.out_connections = [self.mock_connection_low, self.mock_connection_high]
        self.node.ranges = {"0-50": None, "60-100": None}
        self.node.value = 55  # Falls between ranges
        
        self.node.execute()
        
        # All connections should be killed
        self.mock_connection_low.make_killer.assert_called_once()
        self.mock_connection_high.make_killer.assert_called_once()
        # Should trigger false path
        self.assertIn("error", self.node.false_path)

    def test_value_matches_range_method(self):
        # Test range matching method directly
        self.assertTrue(self.node._value_matches_range(25, "0-50"))
        self.assertFalse(self.node._value_matches_range(75, "0-50"))
        self.assertTrue(self.node._value_matches_range(75, ">50"))
        self.assertFalse(self.node._value_matches_range(25, ">50"))
        self.assertTrue(self.node._value_matches_range(50, "<=50"))
        self.assertFalse(self.node._value_matches_range(51, "<=50"))
        self.assertTrue(self.node._value_matches_range(50, ">=50"))
        self.assertFalse(self.node._value_matches_range(49, ">=50"))
        self.assertTrue(self.node._value_matches_range(25, "<50"))
        self.assertFalse(self.node._value_matches_range(50, "<50"))
        self.assertTrue(self.node._value_matches_range(42, "==42"))
        self.assertFalse(self.node._value_matches_range(43, "==42"))
        # Test invalid range format
        self.assertFalse(self.node._value_matches_range(25, "invalid"))


if __name__ == "__main__":
    unittest.main()