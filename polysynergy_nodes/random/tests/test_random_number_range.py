import asyncio
import unittest
from polysynergy_nodes.random.random_number_range import RandomNumberRange


class TestRandomNumberRangeNode(unittest.TestCase):

    def setUp(self):
        self.node = RandomNumberRange()
        self.node.true_path = None
        self.node.false_path = None
        self.node.count = 5
        self.node.min_value = 0
        self.node.max_value = 100
        self.node.number_type = "int"
        self.node.unique = False
        self.node.decimal_places = 2

    def test_default_integer_generation(self):
        asyncio.run(self.node.execute())
        
        self.assertTrue(isinstance(self.node.true_path, list))
        self.assertEqual(len(self.node.true_path), 5)
        
        # All should be integers within range
        for num in self.node.true_path:
            self.assertTrue(isinstance(num, int))
            self.assertTrue(0 <= num <= 100)

    def test_float_generation(self):
        self.node.number_type = "float"
        self.node.decimal_places = 2
        asyncio.run(self.node.execute())
        
        self.assertEqual(len(self.node.true_path), 5)
        
        # All should be floats within range with correct decimal places
        for num in self.node.true_path:
            self.assertTrue(isinstance(num, float))
            self.assertTrue(0 <= num <= 100)
            # Check decimal places (allowing for floating point precision)
            self.assertEqual(round(num, 2), num)

    def test_unique_integers(self):
        self.node.unique = True
        self.node.count = 10
        self.node.min_value = 1
        self.node.max_value = 10
        asyncio.run(self.node.execute())
        
        # Should have 10 unique numbers
        self.assertEqual(len(self.node.true_path), 10)
        self.assertEqual(len(set(self.node.true_path)), 10)

    def test_unique_integers_impossible(self):
        self.node.unique = True
        self.node.count = 11  # More than possible unique values
        self.node.min_value = 1
        self.node.max_value = 10  # Only 10 possible values
        asyncio.run(self.node.execute())
        
        # Should have error
        self.assertIsNotNone(self.node.false_path)

    def test_unique_floats(self):
        self.node.number_type = "float"
        self.node.unique = True
        self.node.count = 5
        asyncio.run(self.node.execute())
        
        # Should have unique float values
        self.assertEqual(len(self.node.true_path), 5)
        self.assertEqual(len(set(self.node.true_path)), 5)

    def test_custom_range(self):
        self.node.min_value = 50
        self.node.max_value = 60
        self.node.count = 10
        asyncio.run(self.node.execute())
        
        # All should be within custom range
        for num in self.node.true_path:
            self.assertTrue(50 <= num <= 60)

    def test_negative_range(self):
        self.node.min_value = -50
        self.node.max_value = -10
        self.node.count = 5
        asyncio.run(self.node.execute())
        
        # All should be within negative range
        for num in self.node.true_path:
            self.assertTrue(-50 <= num <= -10)

    def test_zero_count(self):
        self.node.count = 0
        asyncio.run(self.node.execute())
        
        # Should have error
        self.assertIsNotNone(self.node.false_path)

    def test_invalid_range(self):
        self.node.min_value = 100
        self.node.max_value = 50  # Min > Max
        asyncio.run(self.node.execute())
        
        # Should have error
        self.assertIsNotNone(self.node.false_path)

    def test_large_count(self):
        self.node.count = 100
        self.node.min_value = 1
        self.node.max_value = 1000
        asyncio.run(self.node.execute())
        
        self.assertEqual(len(self.node.true_path), 100)
        
        # All should be within range
        for num in self.node.true_path:
            self.assertTrue(1 <= num <= 1000)

    def test_decimal_places_precision(self):
        self.node.number_type = "float"
        self.node.decimal_places = 3
        self.node.count = 5
        asyncio.run(self.node.execute())
        
        # Check that all floats have correct precision
        for num in self.node.true_path:
            self.assertEqual(round(num, 3), num)


if __name__ == "__main__":
    unittest.main()