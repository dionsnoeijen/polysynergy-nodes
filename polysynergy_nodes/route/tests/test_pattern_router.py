import unittest
from unittest.mock import Mock
from polysynergy_nodes.route.pattern_router import PatternRouter


class TestPatternRouter(unittest.TestCase):

    def setUp(self):
        self.node = PatternRouter()
        
        # Reset paths
        self.node.false_path = False
        
        # Mock connections with source_handle
        self.mock_connection_email = Mock()
        self.mock_connection_email.source_handle = "patterns.^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        self.mock_connection_email.make_killer = Mock()
        
        self.mock_connection_phone = Mock()
        self.mock_connection_phone.source_handle = "patterns.^\d{3}-\d{3}-\d{4}$"
        self.mock_connection_phone.make_killer = Mock()
        
        self.mock_connection_url = Mock()
        self.mock_connection_url.source_handle = "patterns.^https?://.*"
        self.mock_connection_url.make_killer = Mock()
        
        self.mock_connection_default = Mock()
        self.mock_connection_default.source_handle = "patterns.default"
        self.mock_connection_default.make_killer = Mock()

    def test_no_connections_triggers_false_path(self):
        self.node.out_connections = []
        self.node.value = "test@example.com"
        
        self.node.execute()
        
        self.assertIn("error", self.node.false_path)

    def test_email_pattern_match(self):
        email_pattern = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
        self.node.out_connections = [self.mock_connection_email, self.mock_connection_phone]
        self.node.patterns = {email_pattern: None, "^\\d{3}-\\d{3}-\\d{4}$": None}
        self.node.value = "user@example.com"
        
        self.node.execute()
        
        # Email pattern connection should not be killed
        self.mock_connection_email.make_killer.assert_not_called()
        # Phone pattern connection should be killed
        self.mock_connection_phone.make_killer.assert_called_once()
        # Value should be stored in the email pattern
        self.assertEqual(self.node.patterns[email_pattern], "user@example.com")

    def test_phone_pattern_match(self):
        phone_pattern = "^\\d{3}-\\d{3}-\\d{4}$"
        self.node.out_connections = [self.mock_connection_email, self.mock_connection_phone]
        self.node.patterns = {"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$": None, phone_pattern: None}
        self.node.value = "123-456-7890"
        
        self.node.execute()
        
        # Phone pattern connection should not be killed
        self.mock_connection_phone.make_killer.assert_not_called()
        # Email pattern connection should be killed
        self.mock_connection_email.make_killer.assert_called_once()
        # Value should be stored in the phone pattern
        self.assertEqual(self.node.patterns[phone_pattern], "123-456-7890")

    def test_url_pattern_match(self):
        url_pattern = "^https?://.*"
        self.node.out_connections = [self.mock_connection_url, self.mock_connection_email]
        self.node.patterns = {url_pattern: None, "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$": None}
        self.node.value = "https://example.com"
        
        self.node.execute()
        
        # URL pattern connection should not be killed
        self.mock_connection_url.make_killer.assert_not_called()
        # Email pattern connection should be killed
        self.mock_connection_email.make_killer.assert_called_once()
        # Value should be stored in the URL pattern
        self.assertEqual(self.node.patterns[url_pattern], "https://example.com")

    def test_simple_word_pattern_match(self):
        word_pattern = "^hello.*"
        self.node.out_connections = [self.mock_connection_email, self.mock_connection_phone]
        self.mock_connection_email.source_handle = "patterns.^hello.*"
        self.mock_connection_phone.source_handle = "patterns.^world.*"
        self.node.patterns = {word_pattern: None, "^world.*": None}
        self.node.value = "hello world"
        
        self.node.execute()
        
        # Word pattern connection should not be killed
        self.mock_connection_email.make_killer.assert_not_called()
        # Other pattern connection should be killed
        self.mock_connection_phone.make_killer.assert_called_once()
        # Value should be stored in the word pattern
        self.assertEqual(self.node.patterns[word_pattern], "hello world")

    def test_default_case_when_no_match(self):
        self.node.out_connections = [self.mock_connection_email, self.mock_connection_default]
        self.node.patterns = {"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$": None, "default": None}
        self.node.value = "not an email"
        
        self.node.execute()
        
        # Default connection should be chosen
        self.mock_connection_default.make_killer.assert_not_called()
        # Email pattern connection should be killed
        self.mock_connection_email.make_killer.assert_called_once()
        # Value should be stored in default case
        self.assertEqual(self.node.patterns["default"], "not an email")

    def test_no_match_no_default_triggers_false_path(self):
        self.node.out_connections = [self.mock_connection_email, self.mock_connection_phone]
        self.node.patterns = {"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$": None, "^\\d{3}-\\d{3}-\\d{4}$": None}
        self.node.value = "not matching any pattern"
        
        self.node.execute()
        
        # All connections should be killed
        self.mock_connection_email.make_killer.assert_called_once()
        self.mock_connection_phone.make_killer.assert_called_once()
        # Should trigger false path
        self.assertIn("error", self.node.false_path)

    def test_invalid_regex_pattern_no_match(self):
        invalid_pattern = "[invalid_regex"
        self.node.out_connections = [self.mock_connection_email, self.mock_connection_default]
        self.mock_connection_email.source_handle = "patterns.[invalid_regex"
        self.node.patterns = {invalid_pattern: None, "default": None}
        self.node.value = "test string"
        
        self.node.execute()
        
        # Invalid regex should not match, default should be chosen
        self.mock_connection_default.make_killer.assert_not_called()
        # Invalid pattern connection should be killed
        self.mock_connection_email.make_killer.assert_called_once()
        # Value should be stored in default case
        self.assertEqual(self.node.patterns["default"], "test string")

    def test_non_string_value_converted_to_string(self):
        number_pattern = "^\\d+$"
        self.node.out_connections = [self.mock_connection_email, self.mock_connection_phone]
        self.mock_connection_email.source_handle = "patterns.^\\d+$"
        self.mock_connection_phone.source_handle = "patterns.^[a-zA-Z]+$"
        self.node.patterns = {number_pattern: None, "^[a-zA-Z]+$": None}
        self.node.value = 12345  # Integer value
        
        self.node.execute()
        
        # Number pattern connection should not be killed (12345 -> "12345")
        self.mock_connection_email.make_killer.assert_not_called()
        # Letter pattern connection should be killed
        self.mock_connection_phone.make_killer.assert_called_once()
        # Original value should be stored
        self.assertEqual(self.node.patterns[number_pattern], 12345)

    def test_case_sensitive_pattern_matching(self):
        case_pattern = "^Hello.*"
        self.node.out_connections = [self.mock_connection_email, self.mock_connection_phone]
        self.mock_connection_email.source_handle = "patterns.^Hello.*"
        self.mock_connection_phone.source_handle = "patterns.^hello.*"
        self.node.patterns = {case_pattern: None, "^hello.*": None}
        self.node.value = "Hello World"
        
        self.node.execute()
        
        # Case-sensitive match should work
        self.mock_connection_email.make_killer.assert_not_called()
        # Lowercase pattern should be killed
        self.mock_connection_phone.make_killer.assert_called_once()
        # Value should be stored in the matching pattern
        self.assertEqual(self.node.patterns[case_pattern], "Hello World")

    def test_value_matches_pattern_method(self):
        # Test pattern matching method directly
        self.assertTrue(self.node._value_matches_pattern("test@example.com", "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"))
        self.assertFalse(self.node._value_matches_pattern("not an email", "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"))
        self.assertTrue(self.node._value_matches_pattern("123-456-7890", "^\\d{3}-\\d{3}-\\d{4}$"))
        self.assertFalse(self.node._value_matches_pattern("123456789", "^\\d{3}-\\d{3}-\\d{4}$"))
        # Test invalid regex
        self.assertFalse(self.node._value_matches_pattern("test", "[invalid_regex"))


if __name__ == "__main__":
    unittest.main()