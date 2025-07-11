import unittest
from polysynergy_nodes.list.filter_list import FilterList

class TestFilterList(unittest.TestCase):

    def setUp(self):
        self.node = FilterList()
        self.node.true_path = False
        self.node.false_path = False
        self.node.field = ""

    def run_test(self, input_list, match_value, match_mode, expected):
        self.node.input_list = input_list
        self.node.match_value = match_value
        self.node.match_mode = match_mode
        self.node.execute()
        self.assertEqual(sorted(self.node.true_path), sorted(expected), f"Failed on mode: {match_mode}")

    def test_all_modes(self):
        tests = [
            (["apple", "banana", "cherry"], "banana", "equals", ["banana"]),
            (["apple", "banana", "cherry"], "banana", "not_equals", ["apple", "cherry"]),
            (["apple", "banana", "cherry"], "an", "contains", ["banana"]),
            (["apple", "banana", "cherry"], "ap", "starts_with", ["apple"]),
            (["apple", "banana", "cherry"], "rry", "ends_with", ["cherry"]),
            (["apple", "banana", "cherry"], "z", "not_contains", ["apple", "banana", "cherry"]),
            ([1, 5, 10], "4", "greater_than", [5, 10]),
            ([1, 5, 10], "6", "less_than", [1, 5]),
            (["a", "b", "c"], ["a", "c"], "in", ["a", "c"]),
            (["a", "b", "c"], ["b"], "not_in", ["a", "c"]),
        ]
        for input_list, match_value, mode, expected in tests:
            with self.subTest(mode=mode):
                self.run_test(input_list, match_value, mode, expected)

if __name__ == '__main__':
    unittest.main()