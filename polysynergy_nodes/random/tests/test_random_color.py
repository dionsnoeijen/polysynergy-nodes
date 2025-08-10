import asyncio
import unittest
import re
from polysynergy_nodes.random.random_color import RandomColor


class TestRandomColorNode(unittest.TestCase):

    def setUp(self):
        self.node = RandomColor()
        self.node.true_path = None
        self.node.false_path = None
        self.node.format = "hex"

    def test_hex_format(self):
        self.node.format = "hex"
        asyncio.run(self.node.execute())
        
        # Check if it's a valid hex color
        hex_pattern = r'^#[0-9a-f]{6}$'
        self.assertTrue(re.match(hex_pattern, self.node.true_path, re.IGNORECASE))

    def test_rgb_format(self):
        self.node.format = "rgb"
        asyncio.run(self.node.execute())
        
        # Check if it's a valid RGB format
        rgb_pattern = r'^rgb\((\d{1,3}), (\d{1,3}), (\d{1,3})\)$'
        match = re.match(rgb_pattern, self.node.true_path)
        self.assertTrue(match)
        
        # Check if values are within valid range (0-255)
        r, g, b = map(int, match.groups())
        self.assertTrue(0 <= r <= 255)
        self.assertTrue(0 <= g <= 255)
        self.assertTrue(0 <= b <= 255)

    def test_hsl_format(self):
        self.node.format = "hsl"
        asyncio.run(self.node.execute())
        
        # Check if it's a valid HSL format
        hsl_pattern = r'^hsl\((\d{1,3}), (\d{1,3})%, (\d{1,3})%\)$'
        match = re.match(hsl_pattern, self.node.true_path)
        self.assertTrue(match)
        
        # Check if values are within valid ranges
        h, s, l = map(int, match.groups())
        self.assertTrue(0 <= h <= 360)
        self.assertTrue(0 <= s <= 100)
        self.assertTrue(0 <= l <= 100)

    def test_name_format(self):
        self.node.format = "name"
        asyncio.run(self.node.execute())
        
        # Check if it's a string and not empty
        self.assertTrue(isinstance(self.node.true_path, str))
        self.assertTrue(len(self.node.true_path) > 0)

    def test_unsupported_format(self):
        self.node.format = "invalid"
        asyncio.run(self.node.execute())
        
        # Should have error in false_path
        self.assertIsNotNone(self.node.false_path)

    def test_multiple_hex_colors_unique(self):
        """Test that multiple calls generate different colors (probabilistically)"""
        colors = set()
        for _ in range(10):
            self.node.format = "hex"
            self.node.true_path = None
            asyncio.run(self.node.execute())
            colors.add(self.node.true_path)
        
        # Very unlikely to get all same colors
        self.assertTrue(len(colors) > 1)


if __name__ == "__main__":
    unittest.main()