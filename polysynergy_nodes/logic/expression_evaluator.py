import re
from typing import Dict
from polysynergy_node_runner.setup_context.dock_property import dock_text_area, dock_dict
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings
from polysynergy_node_runner.setup_context.node_error import NodeError

@node(name="Expression Evaluator", category="logic", type="expression_evaluator", icon="logic.svg", version=1.0)
class ExpressionEvaluator(Node):
    # Variables dictionary for dynamic variable names
    variables: dict = NodeVariableSettings(
        label="Variables",
        dock=dock_dict(
            key_label="Variable Name",
            in_switch=True,
            value_field=True,
            type_field=True,
            out_switch=False,
            info="Variables to use in the expression (e.g., age, price, status)"
        ),
        default=[]
    )

    # Expression to evaluate
    expression: str = NodeVariableSettings(
        dock=dock_text_area(),
        has_in=True,
        has_out=False,
        info="Expression to evaluate using variable names (e.g., 'age > 18 && status == \"active\"')"
    )
    
    # Path settings
    true_path: bool = PathSettings(default=False)
    false_path: bool | str = PathSettings(default=False)

    def coerce_value(self, value: int | float | str | bool) -> int | float | str | bool:
        """Convert string values to appropriate types for comparison."""
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return value
        if isinstance(value, str):
            stripped = value.strip().lower()
            if stripped == "true":
                return True
            if stripped == "false":
                return False
            # Try to convert to number
            try:
                if '.' in stripped:
                    return float(stripped)
                else:
                    return int(stripped)
            except ValueError:
                return value
        return value

    def get_variables(self) -> Dict[str, int | float | str | bool]:
        """Get all variable values from the variables dict and coerce them."""
        coerced_vars = {}
        for var_name, value in self.variables.items():
            if value is not None:
                coerced_vars[var_name] = self.coerce_value(value)
        return coerced_vars

    def tokenize_expression(self, expression: str) -> list:
        """Tokenize the expression into operators, operands, and parentheses."""
        # Define token patterns
        token_pattern = r'(\|\||&&|>=|<=|==|!=|>|<|!|\(|\)|[a-zA-Z_][a-zA-Z0-9_]*|"[^"]*"|\d+\.?\d*)'
        tokens = re.findall(token_pattern, expression)
        return [token.strip() for token in tokens if token.strip()]

    def evaluate_comparison(self, left: int | float | str | bool, operator: str, right: int | float | str | bool) -> bool:
        """Evaluate a single comparison."""
        try:
            if operator == '==':
                return left == right
            elif operator == '!=':
                return left != right
            elif operator == '>':
                return left > right
            elif operator == '<':
                return left < right
            elif operator == '>=':
                return left >= right
            elif operator == '<=':
                return left <= right
            else:
                raise ValueError(f"Unknown comparison operator: {operator}")
        except TypeError:
            # Handle type comparison errors (e.g., comparing string to number)
            return False

    def evaluate_expression(self, expression: str, variables: Dict[str, int | float | str | bool]) -> bool:
        """Evaluate a boolean expression with support for &&, ||, !, and ()."""
        tokens = self.tokenize_expression(expression)
        
        # Replace variables with their values and check for undefined variables
        processed_tokens = []
        for token in tokens:
            if token in variables:
                processed_tokens.append(variables[token])
            elif token.startswith('"') and token.endswith('"'):
                # String literal
                processed_tokens.append(token[1:-1])
            elif token.replace('.', '').isdigit():
                # Numeric literal
                processed_tokens.append(float(token) if '.' in token else int(token))
            elif re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', token):
                # This looks like a variable name but it's not defined
                raise ValueError(f"Undefined variable: {token}")
            else:
                processed_tokens.append(token)
        
        return self.parse_or_expression(processed_tokens, 0)[0]

    def parse_or_expression(self, tokens: list, index: int) -> tuple:
        """Parse OR expressions (lowest precedence)."""
        left, index = self.parse_and_expression(tokens, index)
        
        while index < len(tokens) and tokens[index] == '||':
            index += 1  # Skip '||'
            right, index = self.parse_and_expression(tokens, index)
            left = left or right
            
        return left, index

    def parse_and_expression(self, tokens: list, index: int) -> tuple:
        """Parse AND expressions (higher precedence than OR)."""
        left, index = self.parse_not_expression(tokens, index)
        
        while index < len(tokens) and tokens[index] == '&&':
            index += 1  # Skip '&&'
            right, index = self.parse_not_expression(tokens, index)
            left = left and right
            
        return left, index

    def parse_not_expression(self, tokens: list, index: int) -> tuple:
        """Parse NOT expressions (higher precedence than AND)."""
        if index < len(tokens) and tokens[index] == '!':
            index += 1  # Skip '!'
            value, index = self.parse_primary_expression(tokens, index)
            return not value, index
        else:
            return self.parse_primary_expression(tokens, index)

    def parse_primary_expression(self, tokens: list, index: int) -> tuple:
        """Parse primary expressions (comparisons and parentheses)."""
        if index < len(tokens) and tokens[index] == '(':
            index += 1  # Skip '('
            value, index = self.parse_or_expression(tokens, index)
            if index < len(tokens) and tokens[index] == ')':
                index += 1  # Skip ')'
            return value, index
        else:
            return self.parse_comparison(tokens, index)

    def parse_comparison(self, tokens: list, index: int) -> tuple:
        """Parse comparison expressions."""
        if index >= len(tokens):
            raise ValueError("Unexpected end of expression")
            
        left = tokens[index]
        index += 1
        
        # Check if this is a comparison
        if index < len(tokens) and tokens[index] in ['==', '!=', '>', '<', '>=', '<=']:
            operator = tokens[index]
            index += 1
            
            if index >= len(tokens):
                raise ValueError("Missing right operand in comparison")
                
            right = tokens[index]
            index += 1
            
            result = self.evaluate_comparison(left, operator, right)
            return result, index
        else:
            # Single value (should be boolean)
            if isinstance(left, bool):
                return left, index
            else:
                # Try to convert to boolean
                return bool(left), index

    async def execute(self):
        try:
            if not self.expression or not self.expression.strip():
                self.false_path = NodeError.format("Expression cannot be empty")
                return
            
            variables = self.get_variables()
            
            if not variables:
                self.false_path = NodeError.format("At least one variable must be provided")
                return
            
            # Evaluate the expression
            result = self.evaluate_expression(self.expression, variables)
            
            if result:
                self.true_path = True
                self.false_path = False
            else:
                self.true_path = False
                self.false_path = False
                
        except Exception as e:
            self.true_path = False
            self.false_path = NodeError.format(f"Expression evaluation error: {str(e)}")