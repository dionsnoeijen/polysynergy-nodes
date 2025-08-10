import unittest
from unittest.mock import patch
import time
from polysynergy_nodes.date_time.timeout import Timeout


class TestTimeout(unittest.TestCase):

    def setUp(self):
        self.node = Timeout()
        self.node.true_path = False

    def test_default_timeout_one_second(self):
        start_time = time.time()
        self.node.seconds = 1
        
        self.node.execute()
        
        end_time = time.time()
        elapsed = end_time - start_time
        
        # Should sleep for approximately 1 second (within 0.1s tolerance)
        self.assertGreaterEqual(elapsed, 0.9)
        self.assertLessEqual(elapsed, 1.1)
        self.assertTrue(self.node.true_path)

    def test_zero_second_timeout(self):
        start_time = time.time()
        self.node.seconds = 0
        
        self.node.execute()
        
        end_time = time.time()
        elapsed = end_time - start_time
        
        # Should complete almost immediately
        self.assertLessEqual(elapsed, 0.1)
        self.assertTrue(self.node.true_path)

    def test_half_second_timeout(self):
        start_time = time.time()
        self.node.seconds = 0.5
        
        self.node.execute()
        
        end_time = time.time()
        elapsed = end_time - start_time
        
        # Should sleep for approximately 0.5 seconds
        self.assertGreaterEqual(elapsed, 0.4)
        self.assertLessEqual(elapsed, 0.6)
        self.assertTrue(self.node.true_path)

    def test_longer_timeout(self):
        start_time = time.time()
        self.node.seconds = 2
        
        self.node.execute()
        
        end_time = time.time()
        elapsed = end_time - start_time
        
        # Should sleep for approximately 2 seconds
        self.assertGreaterEqual(elapsed, 1.9)
        self.assertLessEqual(elapsed, 2.1)
        self.assertTrue(self.node.true_path)

    @patch('time.sleep')
    def test_sleep_called_with_correct_value(self, mock_sleep):
        # Test that time.sleep is called with the correct value without actually waiting
        self.node.seconds = 5
        
        self.node.execute()
        
        mock_sleep.assert_called_once_with(5)
        self.assertTrue(self.node.true_path)

    @patch('time.sleep')
    def test_zero_timeout_still_calls_sleep(self, mock_sleep):
        # Even with 0 seconds, sleep should still be called
        self.node.seconds = 0
        
        self.node.execute()
        
        mock_sleep.assert_called_once_with(0)
        self.assertTrue(self.node.true_path)

    @patch('time.sleep')
    def test_float_seconds_value(self, mock_sleep):
        # Test with float value
        self.node.seconds = 1.5
        
        self.node.execute()
        
        mock_sleep.assert_called_once_with(1.5)
        self.assertTrue(self.node.true_path)

    @patch('time.sleep')
    def test_large_timeout_value(self, mock_sleep):
        # Test with larger timeout value
        self.node.seconds = 3600  # 1 hour
        
        self.node.execute()
        
        mock_sleep.assert_called_once_with(3600)
        self.assertTrue(self.node.true_path)

    @patch('time.sleep')
    def test_fractional_seconds(self, mock_sleep):
        # Test with very small fractional seconds
        self.node.seconds = 0.001  # 1 millisecond
        
        self.node.execute()
        
        mock_sleep.assert_called_once_with(0.001)
        self.assertTrue(self.node.true_path)

    def test_true_path_always_set(self):
        # Test that true_path is always set to True after execution
        test_values = [0, 0.1, 0.5, 1, 2]
        
        for seconds in test_values:
            with self.subTest(seconds=seconds):
                self.node.seconds = seconds
                self.node.true_path = False  # Reset
                
                with patch('time.sleep'):  # Mock to avoid actual waiting
                    self.node.execute()
                
                self.assertTrue(self.node.true_path)

    @patch('time.sleep', side_effect=KeyboardInterrupt("Test interrupt"))
    def test_keyboard_interrupt_handling(self, mock_sleep):
        # Test behavior when KeyboardInterrupt occurs during sleep
        self.node.seconds = 5
        
        # Should raise the KeyboardInterrupt (not catch it)
        with self.assertRaises(KeyboardInterrupt):
            self.node.execute()
        
        mock_sleep.assert_called_once_with(5)

    def test_node_properties(self):
        # Test node configuration properties
        self.assertEqual(self.node.seconds, 1)  # Default value
        self.assertFalse(self.node.true_path)   # Initial state

    def test_negative_seconds_handling(self):
        # Python's time.sleep handles negative values by doing nothing
        with patch('time.sleep') as mock_sleep:
            self.node.seconds = -1
            
            self.node.execute()
            
            mock_sleep.assert_called_once_with(-1)
            self.assertTrue(self.node.true_path)

    def test_very_small_timeout_precision(self):
        # Test very small timeout values
        start_time = time.time()
        self.node.seconds = 0.01  # 10 milliseconds
        
        self.node.execute()
        
        end_time = time.time()
        elapsed = end_time - start_time
        
        # Should complete quickly but allow for some system overhead
        self.assertLessEqual(elapsed, 0.1)
        self.assertTrue(self.node.true_path)

    def test_multiple_executions(self):
        # Test that the node can be executed multiple times
        with patch('time.sleep') as mock_sleep:
            
            # First execution
            self.node.seconds = 1
            self.node.execute()
            self.assertTrue(self.node.true_path)
            
            # Reset and second execution
            self.node.true_path = False
            self.node.seconds = 2
            self.node.execute()
            self.assertTrue(self.node.true_path)
            
            # Should have been called twice
            self.assertEqual(mock_sleep.call_count, 2)
            mock_sleep.assert_any_call(1)
            mock_sleep.assert_any_call(2)


if __name__ == "__main__":
    unittest.main()