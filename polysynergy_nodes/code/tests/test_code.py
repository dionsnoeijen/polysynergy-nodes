import pytest
from polysynergy_nodes.code import Code


@pytest.mark.asyncio
async def test_code_simple_return():
    """Test simple return statement"""
    node = Code()
    node.code = "return 42"

    result = await node.execute()

    assert result == 42
    assert node.true_path == 42
    assert node.false_path is False


@pytest.mark.asyncio
async def test_code_with_arguments():
    """Test code with arguments"""
    node = Code()
    node.arguments = {"x": 10, "y": 5}
    node.code = "return x + y"

    result = await node.execute()

    assert result == 15
    assert node.true_path == 15


@pytest.mark.asyncio
async def test_code_multiline():
    """Test multiline code"""
    node = Code()
    node.arguments = {"items": [1, 2, 3]}
    node.code = """result = []
for item in items:
    result.append(item * 2)
return result"""

    result = await node.execute()

    assert result == [2, 4, 6]
    assert node.true_path == [2, 4, 6]


@pytest.mark.asyncio
async def test_code_with_imports():
    """Test code with imports"""
    node = Code()
    node.arguments = {"data": {"key": "value"}}
    node.code = """import json
return json.dumps(data)"""

    result = await node.execute()

    assert result == '{"key": "value"}'


@pytest.mark.asyncio
async def test_code_async_operations():
    """Test async code"""
    node = Code()
    node.code = """import asyncio
await asyncio.sleep(0.001)
return "done" """

    result = await node.execute()

    assert result == "done"
    assert node.true_path == "done"


@pytest.mark.asyncio
async def test_code_exception_handling():
    """Test exception handling"""
    node = Code()
    node.code = "raise ValueError('test error')"

    result = await node.execute()

    assert result is None
    assert node.true_path is False
    assert node.false_path['error'] == 'test error'
    assert node.false_path['type'] == 'ValueError'


@pytest.mark.asyncio
async def test_code_no_return():
    """Test code without return statement"""
    node = Code()
    node.arguments = {"x": 10}
    node.code = "y = x * 2"

    result = await node.execute()

    assert result is None
    assert node.true_path is None


@pytest.mark.asyncio
async def test_code_string_manipulation():
    """Test string manipulation"""
    node = Code()
    node.arguments = {"text": "hello"}
    node.code = "return text.upper()"

    result = await node.execute()

    assert result == "HELLO"


@pytest.mark.asyncio
async def test_code_dict_operations():
    """Test dictionary operations"""
    node = Code()
    node.arguments = {"data": {"users": [{"name": "Alice", "age": 25}, {"name": "Bob", "age": 17}]}}
    node.code = """adults = [u for u in data['users'] if u['age'] >= 18]
return adults"""

    result = await node.execute()

    assert len(result) == 1
    assert result[0]['name'] == 'Alice'


@pytest.mark.asyncio
async def test_code_automatic_number_parsing():
    """Test automatic JSON parsing of string numbers"""
    node = Code()
    node.arguments = {"a": "10", "b": "20"}  # Strings from UI
    node.code = "return a + b"

    result = await node.execute()

    assert result == 30  # Should be number addition, not string concatenation
    assert node.true_path == 30


@pytest.mark.asyncio
async def test_code_automatic_boolean_parsing():
    """Test automatic JSON parsing of booleans"""
    node = Code()
    node.arguments = {"is_active": "true", "is_admin": "false"}
    node.code = "return is_active and not is_admin"

    result = await node.execute()

    assert result is True


@pytest.mark.asyncio
async def test_code_automatic_array_parsing():
    """Test automatic JSON parsing of arrays"""
    node = Code()
    node.arguments = {"numbers": "[1, 2, 3, 4, 5]"}
    node.code = "return sum(numbers)"

    result = await node.execute()

    assert result == 15


@pytest.mark.asyncio
async def test_code_mixed_types():
    """Test mixed argument types from UI and connections"""
    node = Code()
    node.arguments = {
        "count": "42",           # String from UI → should become int
        "name": "Alice",         # Plain string → stays string
        "active": "true",        # Boolean string → becomes bool
        "items": [1, 2, 3],      # Already list from connection → stays list
        "ratio": "3.14"          # Float string → becomes float
    }
    node.code = """result = {
    'count_doubled': count * 2,
    'greeting': f"Hello {name}",
    'is_active': active,
    'item_count': len(items),
    'ratio_squared': ratio ** 2
}
return result"""

    result = await node.execute()

    assert result['count_doubled'] == 84
    assert result['greeting'] == "Hello Alice"
    assert result['is_active'] is True
    assert result['item_count'] == 3
    assert result['ratio_squared'] == 9.8596
