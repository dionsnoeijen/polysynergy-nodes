import asyncio
import pytest
from polysynergy_nodes.collection.array_get import ArrayGet
from polysynergy_nodes.collection.dict_get import DictGet
from polysynergy_nodes.collection.length import Length


class TestArrayGet:
    def test_get_valid_index(self):
        node = ArrayGet()
        node.true_path = False
        node.false_path = False
        node.array = ['a', 'b', 'c', 'd']
        node.index = 2
        asyncio.run(node.execute())
        
        assert node.true_path == 'c'
        assert node.item == 'c'
        assert node.false_path is False

    def test_get_first_index(self):
        node = ArrayGet()
        node.true_path = False
        node.false_path = False
        node.array = [10, 20, 30]
        node.index = 0
        asyncio.run(node.execute())
        
        assert node.true_path == 10
        assert node.item == 10

    def test_get_last_index(self):
        node = ArrayGet()
        node.true_path = False
        node.false_path = False
        node.array = [10, 20, 30]
        node.index = 2
        asyncio.run(node.execute())
        
        assert node.true_path == 30
        assert node.item == 30

    def test_negative_indexing(self):
        node = ArrayGet()
        node.true_path = False
        node.false_path = False
        node.array = ['x', 'y', 'z']
        node.index = -1
        asyncio.run(node.execute())
        
        assert node.true_path == 'z'
        assert node.item == 'z'

    def test_negative_indexing_middle(self):
        node = ArrayGet()
        node.true_path = False
        node.false_path = False
        node.array = ['a', 'b', 'c', 'd', 'e']
        node.index = -2
        asyncio.run(node.execute())
        
        assert node.true_path == 'd'
        assert node.item == 'd'

    def test_index_out_of_bounds_positive(self):
        node = ArrayGet()
        node.true_path = False
        node.false_path = False
        node.array = ['a', 'b', 'c']
        node.index = 5
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert "out of range" in str(node.false_path)

    def test_index_out_of_bounds_negative(self):
        node = ArrayGet()
        node.true_path = False
        node.false_path = False
        node.array = ['a', 'b', 'c']
        node.index = -5
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert "out of range" in str(node.false_path)

    def test_empty_array(self):
        node = ArrayGet()
        node.true_path = False
        node.false_path = False
        node.array = []
        node.index = 0
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert "out of range" in str(node.false_path)

    def test_non_list_input(self):
        node = ArrayGet()
        node.true_path = False
        node.false_path = False
        node.array = "not a list"
        node.index = 0
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert "must be a list" in str(node.false_path)

    def test_string_index_conversion(self):
        node = ArrayGet()
        node.true_path = False
        node.false_path = False
        node.array = [1, 2, 3, 4, 5]
        node.index = "2"  # String that can be converted to int
        asyncio.run(node.execute())
        
        assert node.true_path == 3
        assert node.item == 3

    def test_invalid_string_index(self):
        node = ArrayGet()
        node.true_path = False
        node.false_path = False
        node.array = [1, 2, 3]
        node.index = "invalid"
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert "must be an integer" in str(node.false_path)

    def test_mixed_type_array(self):
        node = ArrayGet()
        node.true_path = False
        node.false_path = False
        node.array = [1, "hello", {"key": "value"}, [1, 2, 3]]
        node.index = 2
        asyncio.run(node.execute())
        
        assert node.true_path == {"key": "value"}
        assert node.item == {"key": "value"}


class TestDictGet:
    def test_get_existing_key(self):
        node = DictGet()
        node.true_path = False
        node.false_path = False
        node.dict_obj = {"name": "John", "age": 30, "city": "New York"}
        node.key = "name"
        node.default_value = "Unknown"
        asyncio.run(node.execute())
        
        assert node.true_path == "John"
        assert node.value == "John"
        assert node.false_path is False

    def test_get_missing_key_with_default(self):
        node = DictGet()
        node.true_path = False
        node.false_path = False
        node.dict_obj = {"name": "John", "age": 30}
        node.key = "country"
        node.default_value = "USA"
        asyncio.run(node.execute())
        
        assert node.true_path == "USA"
        assert node.value == "USA"

    def test_get_missing_key_no_default(self):
        node = DictGet()
        node.true_path = False
        node.false_path = False
        node.dict_obj = {"name": "John"}
        node.key = "age"
        node.default_value = None
        asyncio.run(node.execute())
        
        assert node.true_path is None
        assert node.value is None

    def test_different_value_types(self):
        node = DictGet()
        node.true_path = False
        node.false_path = False
        node.dict_obj = {
            "string": "hello",
            "number": 42,
            "boolean": True,
            "list": [1, 2, 3],
            "dict": {"nested": "value"}
        }
        node.key = "list"
        node.default_value = []
        asyncio.run(node.execute())
        
        assert node.true_path == [1, 2, 3]
        assert node.value == [1, 2, 3]

    def test_non_string_key_conversion(self):
        node = DictGet()
        node.true_path = False
        node.false_path = False
        node.dict_obj = {"123": "numeric_key", "True": "boolean_key"}
        node.key = 123  # Non-string key
        node.default_value = "not_found"
        asyncio.run(node.execute())
        
        assert node.true_path == "numeric_key"
        assert node.value == "numeric_key"

    def test_empty_dictionary(self):
        node = DictGet()
        node.true_path = False
        node.false_path = False
        node.dict_obj = {}
        node.key = "anything"
        node.default_value = "empty_dict_default"
        asyncio.run(node.execute())
        
        assert node.true_path == "empty_dict_default"
        assert node.value == "empty_dict_default"

    def test_non_dict_input(self):
        node = DictGet()
        node.true_path = False
        node.false_path = False
        node.dict_obj = "not a dictionary"
        node.key = "key"
        node.default_value = "default"
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert "must be a dictionary" in str(node.false_path)

    def test_none_value_in_dict(self):
        node = DictGet()
        node.true_path = False
        node.false_path = False
        node.dict_obj = {"key": None}
        node.key = "key"
        node.default_value = "default"
        asyncio.run(node.execute())
        
        # Should return None (the actual value), not the default
        assert node.true_path is None
        assert node.value is None


class TestLength:
    def test_list_length(self):
        node = Length()
        node.true_path = False
        node.false_path = False
        node.value = [1, 2, 3, 4, 5]
        asyncio.run(node.execute())
        
        assert node.true_path == 5
        assert node.length == 5
        assert node.false_path is False

    def test_string_length(self):
        node = Length()
        node.true_path = False
        node.false_path = False
        node.value = "Hello World"
        asyncio.run(node.execute())
        
        assert node.true_path == 11
        assert node.length == 11

    def test_dict_length(self):
        node = Length()
        node.true_path = False
        node.false_path = False
        node.value = {"a": 1, "b": 2, "c": 3}
        asyncio.run(node.execute())
        
        assert node.true_path == 3
        assert node.length == 3

    def test_empty_list_length(self):
        node = Length()
        node.true_path = False
        node.false_path = False
        node.value = []
        asyncio.run(node.execute())
        
        assert node.true_path == 0
        assert node.length == 0

    def test_empty_string_length(self):
        node = Length()
        node.true_path = False
        node.false_path = False
        node.value = ""
        asyncio.run(node.execute())
        
        assert node.true_path == 0
        assert node.length == 0

    def test_empty_dict_length(self):
        node = Length()
        node.true_path = False
        node.false_path = False
        node.value = {}
        asyncio.run(node.execute())
        
        assert node.true_path == 0
        assert node.length == 0

    def test_tuple_length(self):
        node = Length()
        node.true_path = False
        node.false_path = False
        node.value = (1, 2, 3, 4)
        asyncio.run(node.execute())
        
        assert node.true_path == 4
        assert node.length == 4

    def test_set_length(self):
        node = Length()
        node.true_path = False
        node.false_path = False
        node.value = {1, 2, 3, 4, 5}
        asyncio.run(node.execute())
        
        assert node.true_path == 5
        assert node.length == 5

    def test_none_value(self):
        node = Length()
        node.true_path = False
        node.false_path = False
        node.value = None
        asyncio.run(node.execute())
        
        assert node.true_path == 0
        assert node.length == 0

    def test_non_iterable_type(self):
        node = Length()
        node.true_path = False
        node.false_path = False
        node.value = 42  # Integer has no length
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert "Cannot get length" in str(node.false_path)