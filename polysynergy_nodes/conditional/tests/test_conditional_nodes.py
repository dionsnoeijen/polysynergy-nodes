import asyncio
import pytest
from polysynergy_nodes.conditional.if_then_else import IfThenElse
from polysynergy_nodes.conditional.switch import Switch


class TestIfThenElse:
    def test_condition_true(self):
        node = IfThenElse()
        node.true_path = False
        node.false_path = False
        node.condition = True
        node.then_value = "yes"
        node.else_value = "no"
        asyncio.run(node.execute())
        
        assert node.true_path == "yes"
        assert node.false_path is False

    def test_condition_false(self):
        node = IfThenElse()
        node.true_path = False
        node.false_path = False
        node.condition = False
        node.then_value = "yes"
        node.else_value = "no"
        asyncio.run(node.execute())
        
        assert node.true_path == "no"
        assert node.false_path is False

    def test_string_condition_truthy(self):
        node = IfThenElse()
        node.true_path = False
        node.false_path = False
        node.condition = "hello"
        node.then_value = 100
        node.else_value = 200
        asyncio.run(node.execute())
        
        assert node.true_path == 100
        assert node.false_path is False

    def test_string_condition_falsy(self):
        node = IfThenElse()
        node.true_path = False
        node.false_path = False
        node.condition = ""
        node.then_value = 100
        node.else_value = 200
        asyncio.run(node.execute())
        
        assert node.true_path == 200
        assert node.false_path is False

    def test_number_condition(self):
        node = IfThenElse()
        node.true_path = False
        node.false_path = False
        node.condition = 0
        node.then_value = "positive"
        node.else_value = "zero_or_negative"
        asyncio.run(node.execute())
        
        assert node.true_path == "zero_or_negative"
        assert node.false_path is False


class TestSwitch:
    def test_first_case_match(self):
        node = Switch()
        node.true_path = False
        node.false_path = False
        node.value = "A"
        node.case_1 = "A"
        node.result_1 = "Result A"
        node.case_2 = "B"
        node.result_2 = "Result B"
        node.default_result = "Default"
        asyncio.run(node.execute())
        
        assert node.true_path == "Result A"
        assert node.false_path is False

    def test_second_case_match(self):
        node = Switch()
        node.true_path = False
        node.false_path = False
        node.value = "B"
        node.case_1 = "A"
        node.result_1 = "Result A"
        node.case_2 = "B"
        node.result_2 = "Result B"
        node.default_result = "Default"
        asyncio.run(node.execute())
        
        assert node.true_path == "Result B"
        assert node.false_path is False

    def test_default_case(self):
        node = Switch()
        node.true_path = False
        node.false_path = False
        node.value = "C"
        node.case_1 = "A"
        node.result_1 = "Result A"
        node.case_2 = "B"
        node.result_2 = "Result B"
        node.default_result = "Default"
        asyncio.run(node.execute())
        
        assert node.true_path == "Default"
        assert node.false_path is False

    def test_number_cases(self):
        node = Switch()
        node.true_path = False
        node.false_path = False
        node.value = 42
        node.case_1 = 10
        node.result_1 = "Ten"
        node.case_2 = 42
        node.result_2 = "Forty Two"
        node.default_result = "Other"
        asyncio.run(node.execute())
        
        assert node.true_path == "Forty Two"
        assert node.false_path is False