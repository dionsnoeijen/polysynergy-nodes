import asyncio
import pytest
from polysynergy_nodes.logic.expression_evaluator import ExpressionEvaluator


class TestExpressionEvaluator:
    def test_simple_comparison_greater_than(self):
        node = ExpressionEvaluator()
        node.true_path = False
        node.false_path = False
        node.a = 10
        node.b = 5
        node.expression = "a > b"
        asyncio.run(node.execute())
        
        assert node.true_path is True
        assert node.false_path is False

    def test_simple_comparison_less_than(self):
        node = ExpressionEvaluator()
        node.true_path = False
        node.false_path = False
        node.a = 5
        node.b = 10
        node.expression = "a < b"
        asyncio.run(node.execute())
        
        assert node.true_path is True
        assert node.false_path is False

    def test_simple_comparison_equal(self):
        node = ExpressionEvaluator()
        node.true_path = False
        node.false_path = False
        node.a = 10
        node.b = 10
        node.expression = "a == b"
        asyncio.run(node.execute())
        
        assert node.true_path is True
        assert node.false_path is False

    def test_simple_comparison_not_equal(self):
        node = ExpressionEvaluator()
        node.true_path = False
        node.false_path = False
        node.a = 10
        node.b = 5
        node.expression = "a != b"
        asyncio.run(node.execute())
        
        assert node.true_path is True
        assert node.false_path is False

    def test_and_expression_both_true(self):
        node = ExpressionEvaluator()
        node.true_path = False
        node.false_path = False
        node.a = 10
        node.b = 5
        node.c = 20
        node.expression = "(a > b) && (c > a)"
        asyncio.run(node.execute())
        
        assert node.true_path is True
        assert node.false_path is False

    def test_and_expression_one_false(self):
        node = ExpressionEvaluator()
        node.true_path = False
        node.false_path = False
        node.a = 10
        node.b = 5
        node.c = 8
        node.expression = "(a > b) && (c > a)"
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert node.false_path is False

    def test_or_expression_one_true(self):
        node = ExpressionEvaluator()
        node.true_path = False
        node.false_path = False
        node.a = 10
        node.b = 5
        node.c = 8
        node.expression = "(a > b) || (c > a)"
        asyncio.run(node.execute())
        
        assert node.true_path is True
        assert node.false_path is False

    def test_or_expression_both_false(self):
        node = ExpressionEvaluator()
        node.true_path = False
        node.false_path = False
        node.a = 5
        node.b = 10
        node.c = 3
        node.expression = "(a > b) || (c > a)"
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert node.false_path is False

    def test_complex_expression(self):
        """Test: (a > b) || (b > 20) - the original example."""
        node = ExpressionEvaluator()
        node.true_path = False
        node.false_path = False
        node.a = 5
        node.b = 25
        node.expression = "(a > b) || (b > 20)"
        asyncio.run(node.execute())
        
        assert node.true_path is True  # b > 20 is true
        assert node.false_path is False

    def test_complex_expression_false(self):
        """Test: (a > b) || (b > 20) where both conditions are false."""
        node = ExpressionEvaluator()
        node.true_path = False
        node.false_path = False
        node.a = 5
        node.b = 15
        node.expression = "(a > b) || (b > 20)"
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert node.false_path is False

    def test_not_expression(self):
        node = ExpressionEvaluator()
        node.true_path = False
        node.false_path = False
        node.a = 5
        node.b = 10
        node.expression = "!(a > b)"
        asyncio.run(node.execute())
        
        assert node.true_path is True  # !(5 > 10) = !false = true
        assert node.false_path is False

    def test_nested_parentheses(self):
        node = ExpressionEvaluator()
        node.true_path = False
        node.false_path = False
        node.a = 10
        node.b = 5
        node.c = 20
        node.d = 15
        node.expression = "((a > b) && (c > d)) || (b < 3)"
        asyncio.run(node.execute())
        
        # a > b = true, c > d = true, b < 3 = false
        # (true && true) || false = true || false = true
        assert node.true_path is True
        assert node.false_path is False

    def test_string_comparison(self):
        node = ExpressionEvaluator()
        node.true_path = False
        node.false_path = False
        node.a = "hello"
        node.b = "world"
        node.expression = "a != b"
        asyncio.run(node.execute())
        
        assert node.true_path is True
        assert node.false_path is False

    def test_string_to_number_coercion(self):
        node = ExpressionEvaluator()
        node.true_path = False
        node.false_path = False
        node.a = "10"
        node.b = 5
        node.expression = "a > b"
        asyncio.run(node.execute())
        
        assert node.true_path is True  # "10" coerced to 10
        assert node.false_path is False

    def test_boolean_coercion(self):
        node = ExpressionEvaluator()
        node.true_path = False
        node.false_path = False
        node.a = "true"
        node.b = "false"
        node.expression = "a == b"
        asyncio.run(node.execute())
        
        assert node.true_path is False  # true != false
        assert node.false_path is False

    def test_numeric_literals_in_expression(self):
        node = ExpressionEvaluator()
        node.true_path = False
        node.false_path = False
        node.a = 15
        node.expression = "a > 10"
        asyncio.run(node.execute())
        
        assert node.true_path is True
        assert node.false_path is False

    def test_float_comparisons(self):
        node = ExpressionEvaluator()
        node.true_path = False
        node.false_path = False
        node.a = 3.14
        node.b = 2.5
        node.expression = "a >= b"
        asyncio.run(node.execute())
        
        assert node.true_path is True
        assert node.false_path is False

    def test_empty_expression(self):
        node = ExpressionEvaluator()
        node.true_path = False
        node.false_path = False
        node.a = 10
        node.expression = ""
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert "Expression cannot be empty" in str(node.false_path)

    def test_no_variables_provided(self):
        node = ExpressionEvaluator()
        node.true_path = False
        node.false_path = False
        node.expression = "a > b"
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert "At least one variable must be provided" in str(node.false_path)

    def test_invalid_expression_syntax(self):
        node = ExpressionEvaluator()
        node.true_path = False
        node.false_path = False
        node.a = 10
        node.expression = "a >"  # Missing right operand
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert "Expression evaluation error" in str(node.false_path)

    def test_undefined_variable_in_expression(self):
        node = ExpressionEvaluator()
        node.true_path = False
        node.false_path = False
        node.a = 10
        node.expression = "a > z"  # z is not defined
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert "Expression evaluation error" in str(node.false_path)

    def test_type_mismatch_comparison(self):
        """Test comparing incompatible types gracefully."""
        node = ExpressionEvaluator()
        node.true_path = False
        node.false_path = False
        node.a = "hello"
        node.b = 10
        node.expression = "a > b"
        asyncio.run(node.execute())
        
        # Should handle type mismatch gracefully
        assert node.true_path is False
        assert node.false_path is False

    def test_operator_precedence(self):
        """Test that && has higher precedence than ||."""
        node = ExpressionEvaluator()
        node.true_path = False
        node.false_path = False
        node.a = 1
        node.b = 2
        node.c = 3
        node.d = 4
        # Should be evaluated as: (a > b) || ((c > b) && (d > c))
        node.expression = "a > b || c > b && d > c"
        asyncio.run(node.execute())
        
        # a > b = false, c > b = true, d > c = true
        # false || (true && true) = false || true = true
        assert node.true_path is True
        assert node.false_path is False