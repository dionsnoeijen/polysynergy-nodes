import asyncio
import pytest
from polysynergy_nodes.math.min_max import MinMax
from polysynergy_nodes.math.average import Average
from polysynergy_nodes.math.count import Count


class TestMinMax:
    def test_list_numbers(self):
        node = MinMax()
        node.true_path = False
        node.false_path = False
        node.values = [1, 5, 3, 9, 2]
        asyncio.run(node.execute())
        
        assert node.min_value == 1
        assert node.max_value == 9
        assert node.true_path is True

    def test_string_numbers(self):
        node = MinMax()
        node.true_path = False
        node.false_path = False
        node.values = "1, 5, 3.5, 9, 2"
        asyncio.run(node.execute())
        
        assert node.min_value == 1
        assert node.max_value == 9
        assert node.true_path is True

    def test_empty_values(self):
        node = MinMax()
        node.true_path = False
        node.false_path = False
        node.values = []
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert "No valid numbers" in str(node.false_path)


class TestAverage:
    def test_list_numbers(self):
        node = Average()
        node.true_path = False
        node.false_path = False
        node.values = [1, 2, 3, 4, 5]
        asyncio.run(node.execute())
        
        assert node.average == 3.0
        assert node.sum == 15
        assert node.count == 5
        assert node.true_path == 3.0

    def test_string_numbers(self):
        node = Average()
        node.true_path = False
        node.false_path = False
        node.values = "10, 20, 30"
        asyncio.run(node.execute())
        
        assert node.average == 20.0
        assert node.sum == 60
        assert node.count == 3


class TestCount:
    def test_count_list(self):
        node = Count()
        node.true_path = False
        node.false_path = False
        node.values = [1, 2, 3, 4, 5]
        asyncio.run(node.execute())
        
        assert node.count == 5
        assert node.true_path == 5

    def test_count_string(self):
        node = Count()
        node.true_path = False
        node.false_path = False
        node.values = "hello"
        asyncio.run(node.execute())
        
        assert node.count == 5
        assert node.true_path == 5

    def test_count_dict(self):
        node = Count()
        node.true_path = False
        node.false_path = False
        node.values = {"a": 1, "b": 2, "c": 3}
        asyncio.run(node.execute())
        
        assert node.count == 3
        assert node.true_path == 3

    def test_count_null(self):
        node = Count()
        node.true_path = False
        node.false_path = False
        node.values = None
        asyncio.run(node.execute())
        
        assert node.count == 0
        assert node.true_path == 0