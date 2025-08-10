import asyncio
import pytest
from polysynergy_nodes.utils.is_null import IsNull
from polysynergy_nodes.utils.default_value import DefaultValue
from polysynergy_nodes.utils.type_of import TypeOf
from polysynergy_nodes.utils.delay import Delay


class TestIsNull:
    def test_none_value(self):
        node = IsNull()
        node.true_path = False
        node.false_path = False
        node.value = None
        asyncio.run(node.execute())
        
        assert node.true_path is True
        assert node.is_null is True
        assert node.false_path is False

    def test_empty_string(self):
        node = IsNull()
        node.true_path = False
        node.false_path = False
        node.value = ""
        asyncio.run(node.execute())
        
        assert node.true_path is True
        assert node.is_null is True

    def test_whitespace_string(self):
        node = IsNull()
        node.true_path = False
        node.false_path = False
        node.value = "   "
        asyncio.run(node.execute())
        
        assert node.true_path is True
        assert node.is_null is True

    def test_null_string(self):
        node = IsNull()
        node.true_path = False
        node.false_path = False
        node.value = "null"
        asyncio.run(node.execute())
        
        assert node.true_path is True
        assert node.is_null is True

    def test_none_string(self):
        node = IsNull()
        node.true_path = False
        node.false_path = False
        node.value = "None"
        asyncio.run(node.execute())
        
        assert node.true_path is True
        assert node.is_null is True

    def test_undefined_string(self):
        node = IsNull()
        node.true_path = False
        node.false_path = False
        node.value = "undefined"
        asyncio.run(node.execute())
        
        assert node.true_path is True
        assert node.is_null is True

    def test_empty_list(self):
        node = IsNull()
        node.true_path = False
        node.false_path = False
        node.value = []
        asyncio.run(node.execute())
        
        assert node.true_path is True
        assert node.is_null is True

    def test_empty_dict(self):
        node = IsNull()
        node.true_path = False
        node.false_path = False
        node.value = {}
        asyncio.run(node.execute())
        
        assert node.true_path is True
        assert node.is_null is True

    def test_empty_tuple(self):
        node = IsNull()
        node.true_path = False
        node.false_path = False
        node.value = ()
        asyncio.run(node.execute())
        
        assert node.true_path is True
        assert node.is_null is True

    def test_non_empty_string(self):
        node = IsNull()
        node.true_path = False
        node.false_path = False
        node.value = "hello"
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert node.is_null is False

    def test_non_empty_list(self):
        node = IsNull()
        node.true_path = False
        node.false_path = False
        node.value = [1, 2, 3]
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert node.is_null is False

    def test_number_zero(self):
        node = IsNull()
        node.true_path = False
        node.false_path = False
        node.value = 0
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert node.is_null is False

    def test_boolean_false(self):
        node = IsNull()
        node.true_path = False
        node.false_path = False
        node.value = False
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert node.is_null is False


class TestDefaultValue:
    def test_none_value_uses_default(self):
        node = DefaultValue()
        node.true_path = False
        node.false_path = False
        node.value = None
        node.default = "fallback"
        asyncio.run(node.execute())
        
        assert node.true_path == "fallback"
        assert node.result == "fallback"
        assert node.false_path is False

    def test_empty_string_uses_default(self):
        node = DefaultValue()
        node.true_path = False
        node.false_path = False
        node.value = ""
        node.default = "default_text"
        asyncio.run(node.execute())
        
        assert node.true_path == "default_text"
        assert node.result == "default_text"

    def test_valid_value_ignores_default(self):
        node = DefaultValue()
        node.true_path = False
        node.false_path = False
        node.value = "primary_value"
        node.default = "fallback"
        asyncio.run(node.execute())
        
        assert node.true_path == "primary_value"
        assert node.result == "primary_value"

    def test_zero_is_valid_value(self):
        node = DefaultValue()
        node.true_path = False
        node.false_path = False
        node.value = 0
        node.default = 42
        asyncio.run(node.execute())
        
        assert node.true_path == 0
        assert node.result == 0

    def test_false_is_valid_value(self):
        node = DefaultValue()
        node.true_path = False
        node.false_path = False
        node.value = False
        node.default = True
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert node.result is False

    def test_empty_list_uses_default(self):
        node = DefaultValue()
        node.true_path = False
        node.false_path = False
        node.value = []
        node.default = [1, 2, 3]
        asyncio.run(node.execute())
        
        assert node.true_path == [1, 2, 3]
        assert node.result == [1, 2, 3]

    def test_non_empty_list_ignores_default(self):
        node = DefaultValue()
        node.true_path = False
        node.false_path = False
        node.value = ["a", "b"]
        node.default = [1, 2, 3]
        asyncio.run(node.execute())
        
        assert node.true_path == ["a", "b"]
        assert node.result == ["a", "b"]

    def test_null_string_uses_default(self):
        node = DefaultValue()
        node.true_path = False
        node.false_path = False
        node.value = "null"
        node.default = "replacement"
        asyncio.run(node.execute())
        
        assert node.true_path == "replacement"
        assert node.result == "replacement"


class TestTypeOf:
    def test_string_type(self):
        node = TypeOf()
        node.true_path = False
        node.false_path = False
        node.value = "hello world"
        asyncio.run(node.execute())
        
        assert node.true_path == "string"
        assert node.type_name == "string"
        assert node.false_path is False

    def test_integer_type(self):
        node = TypeOf()
        node.true_path = False
        node.false_path = False
        node.value = 42
        asyncio.run(node.execute())
        
        assert node.true_path == "integer"
        assert node.type_name == "integer"

    def test_float_type(self):
        node = TypeOf()
        node.true_path = False
        node.false_path = False
        node.value = 3.14159
        asyncio.run(node.execute())
        
        assert node.true_path == "float"
        assert node.type_name == "float"

    def test_boolean_type(self):
        node = TypeOf()
        node.true_path = False
        node.false_path = False
        node.value = True
        asyncio.run(node.execute())
        
        assert node.true_path == "boolean"
        assert node.type_name == "boolean"

    def test_list_type(self):
        node = TypeOf()
        node.true_path = False
        node.false_path = False
        node.value = [1, 2, 3]
        asyncio.run(node.execute())
        
        assert node.true_path == "array"
        assert node.type_name == "array"

    def test_dict_type(self):
        node = TypeOf()
        node.true_path = False
        node.false_path = False
        node.value = {"key": "value"}
        asyncio.run(node.execute())
        
        assert node.true_path == "object"
        assert node.type_name == "object"

    def test_none_type(self):
        node = TypeOf()
        node.true_path = False
        node.false_path = False
        node.value = None
        asyncio.run(node.execute())
        
        assert node.true_path == "null"
        assert node.type_name == "null"

    def test_tuple_type(self):
        node = TypeOf()
        node.true_path = False
        node.false_path = False
        node.value = (1, 2, 3)
        asyncio.run(node.execute())
        
        assert node.true_path == "tuple"
        assert node.type_name == "tuple"

    def test_set_type(self):
        node = TypeOf()
        node.true_path = False
        node.false_path = False
        node.value = {1, 2, 3}
        asyncio.run(node.execute())
        
        assert node.true_path == "set"
        assert node.type_name == "set"


class TestDelay:
    def test_delay_with_integer(self):
        node = Delay()
        node.true_path = False
        node.false_path = False
        node.seconds = 0.1  # Short delay for testing
        node.value = "test_value"
        
        import time
        start_time = time.time()
        asyncio.run(node.execute())
        end_time = time.time()
        
        # Should have waited at least 0.1 seconds
        assert end_time - start_time >= 0.09  # Allow small tolerance
        assert node.true_path == "test_value"
        assert node.result == "test_value"
        assert node.false_path is False

    def test_delay_with_float(self):
        node = Delay()
        node.true_path = False
        node.false_path = False
        node.seconds = 0.05
        node.value = 42
        
        import time
        start_time = time.time()
        asyncio.run(node.execute())
        end_time = time.time()
        
        assert end_time - start_time >= 0.04
        assert node.true_path == 42
        assert node.result == 42

    def test_delay_with_string_seconds(self):
        node = Delay()
        node.true_path = False
        node.false_path = False
        node.seconds = "0.05"
        node.value = "converted"
        
        import time
        start_time = time.time()
        asyncio.run(node.execute())
        end_time = time.time()
        
        assert end_time - start_time >= 0.04
        assert node.true_path == "converted"

    def test_delay_zero_seconds(self):
        node = Delay()
        node.true_path = False
        node.false_path = False
        node.seconds = 0
        node.value = "instant"
        
        asyncio.run(node.execute())
        
        assert node.true_path == "instant"
        assert node.result == "instant"

    def test_delay_negative_seconds(self):
        node = Delay()
        node.true_path = False
        node.false_path = False
        node.seconds = -5
        node.value = "negative_handled"
        
        asyncio.run(node.execute())
        
        # Negative should be treated as 0
        assert node.true_path == "negative_handled"

    def test_delay_max_seconds(self):
        node = Delay()
        node.true_path = False
        node.false_path = False
        node.seconds = 500  # Too large
        node.value = "capped"
        
        asyncio.run(node.execute())
        
        # Should be capped to 300 seconds, but we just check it executes
        assert node.true_path == "capped"

    def test_delay_invalid_string_seconds(self):
        node = Delay()
        node.true_path = False
        node.false_path = False
        node.seconds = "not_a_number"
        node.value = "error_case"
        
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert "must be a number" in str(node.false_path)

    def test_delay_with_none_value(self):
        node = Delay()
        node.true_path = False
        node.false_path = False
        node.seconds = 0.01
        node.value = None
        
        asyncio.run(node.execute())
        
        assert node.true_path is None
        assert node.result is None