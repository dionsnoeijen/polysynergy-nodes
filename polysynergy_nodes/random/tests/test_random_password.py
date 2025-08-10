import asyncio
import unittest
import string
from polysynergy_nodes.random.random_password import RandomPassword


class TestRandomPasswordNode(unittest.TestCase):

    def setUp(self):
        self.node = RandomPassword()
        self.node.true_path = None
        self.node.false_path = None
        self.node.length = 12
        self.node.include_uppercase = True
        self.node.include_lowercase = True
        self.node.include_numbers = True
        self.node.include_symbols = True
        self.node.exclude_ambiguous = False

    def test_default_password_generation(self):
        asyncio.run(self.node.execute())
        
        self.assertTrue(isinstance(self.node.true_path, str))
        self.assertEqual(len(self.node.true_path), 12)

    def test_custom_length(self):
        self.node.length = 20
        asyncio.run(self.node.execute())
        
        self.assertEqual(len(self.node.true_path), 20)

    def test_lowercase_only(self):
        self.node.include_uppercase = False
        self.node.include_numbers = False
        self.node.include_symbols = False
        self.node.include_lowercase = True
        asyncio.run(self.node.execute())
        
        # Should only contain lowercase letters
        self.assertTrue(all(c in string.ascii_lowercase for c in self.node.true_path))

    def test_uppercase_only(self):
        self.node.include_lowercase = False
        self.node.include_numbers = False
        self.node.include_symbols = False
        self.node.include_uppercase = True
        asyncio.run(self.node.execute())
        
        # Should only contain uppercase letters
        self.assertTrue(all(c in string.ascii_uppercase for c in self.node.true_path))

    def test_numbers_only(self):
        self.node.include_lowercase = False
        self.node.include_uppercase = False
        self.node.include_symbols = False
        self.node.include_numbers = True
        asyncio.run(self.node.execute())
        
        # Should only contain numbers
        self.assertTrue(all(c in string.digits for c in self.node.true_path))

    def test_symbols_only(self):
        self.node.include_lowercase = False
        self.node.include_uppercase = False
        self.node.include_numbers = False
        self.node.include_symbols = True
        asyncio.run(self.node.execute())
        
        # Should only contain symbols
        symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        self.assertTrue(all(c in symbols for c in self.node.true_path))

    def test_exclude_ambiguous_characters(self):
        self.node.exclude_ambiguous = True
        self.node.include_symbols = False  # Focus on letters/numbers for clearer test
        asyncio.run(self.node.execute())
        
        # Should not contain ambiguous characters
        ambiguous_chars = ['l', 'o', 'I', 'O', '0', '1']
        self.assertTrue(not any(c in self.node.true_path for c in ambiguous_chars))

    def test_no_character_types_selected(self):
        self.node.include_lowercase = False
        self.node.include_uppercase = False
        self.node.include_numbers = False
        self.node.include_symbols = False
        asyncio.run(self.node.execute())
        
        # Should have error
        self.assertIsNotNone(self.node.false_path)

    def test_zero_length(self):
        self.node.length = 0
        asyncio.run(self.node.execute())
        
        # Should have error
        self.assertIsNotNone(self.node.false_path)

    def test_negative_length(self):
        self.node.length = -5
        asyncio.run(self.node.execute())
        
        # Should have error
        self.assertIsNotNone(self.node.false_path)

    def test_password_uniqueness(self):
        """Test that multiple calls generate different passwords"""
        passwords = set()
        for _ in range(10):
            self.node.true_path = None
            asyncio.run(self.node.execute())
            passwords.add(self.node.true_path)
        
        # Very unlikely to get all same passwords
        self.assertTrue(len(passwords) > 1)


if __name__ == "__main__":
    unittest.main()