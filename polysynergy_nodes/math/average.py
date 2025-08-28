from typing import Any, Union, List
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings
from polysynergy_node_runner.setup_context.node_error import NodeError

@node(name="Average", category="math", version=1.0, icon="average.svg")
class Average(Node):
    values: Union[List, str] = NodeVariableSettings(label="Values", dock=True, has_in=True, has_out=False, info="List of numbers or comma-separated string")
    
    average: Union[int, float] = NodeVariableSettings(label="Average", has_out=True)
    count: int = NodeVariableSettings(label="Count", has_out=True, info="Number of values processed")
    sum: Union[int, float] = NodeVariableSettings(label="Sum", has_out=True, info="Total of all values")
    
    true_path: Union[int, float] = PathSettings(label="Result", info="The calculated average")
    false_path: Any = PathSettings(label="Error", info="Error information")

    def parse_values(self, values):
        """Parse input values into a list of numbers."""
        if isinstance(values, list):
            # Convert list items to numbers
            numbers = []
            for item in values:
                if isinstance(item, (int, float)):
                    numbers.append(item)
                elif isinstance(item, str) and item.strip():
                    try:
                        if '.' in item:
                            numbers.append(float(item.strip()))
                        else:
                            numbers.append(int(item.strip()))
                    except ValueError:
                        continue
            return numbers
        elif isinstance(values, str):
            # Parse comma-separated string
            numbers = []
            for item in values.split(','):
                item = item.strip()
                if item:
                    try:
                        if '.' in item:
                            numbers.append(float(item))
                        else:
                            numbers.append(int(item))
                    except ValueError:
                        continue
            return numbers
        else:
            return []

    async def execute(self):
        try:
            numbers = self.parse_values(self.values)
            
            if not numbers:
                raise ValueError("No valid numbers provided")
            
            total = sum(numbers)
            count = len(numbers)
            avg = total / count
            
            self.sum = total
            self.count = count
            self.average = avg
            self.true_path = avg
            self.false_path = False
                
        except Exception as e:
            self.true_path = False
            self.false_path = NodeError.format(str(e))