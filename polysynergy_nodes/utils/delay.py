import asyncio
from typing import Any, Union
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings
from polysynergy_node_runner.setup_context.node_error import NodeError

@node(name="Delay", category="utils", version=1.0)
class Delay(Node):
    seconds: Union[int, float] = NodeVariableSettings(label="Seconds", dock=True, has_in=True, has_out=False, info="Number of seconds to wait", default=1.0)
    value: Any = NodeVariableSettings(label="Value", dock=True, has_in=True, has_out=False, info="Value to pass through after delay")
    
    result: Any = NodeVariableSettings(label="Result", has_out=True, info="The input value after delay")
    
    true_path: Any = PathSettings(label="Result", info="The value after delay")
    false_path: Any = PathSettings(label="Error", info="Error information")

    async def execute(self):
        try:
            # Convert seconds to float
            if isinstance(self.seconds, str):
                try:
                    delay_seconds = float(self.seconds)
                except ValueError:
                    raise ValueError("Seconds must be a number")
            elif isinstance(self.seconds, (int, float)):
                delay_seconds = float(self.seconds)
            else:
                delay_seconds = 1.0
            
            # Ensure delay is not negative and not too large
            if delay_seconds < 0:
                delay_seconds = 0
            elif delay_seconds > 300:  # Max 5 minutes
                delay_seconds = 300
            
            # Wait for the specified time
            await asyncio.sleep(delay_seconds)
            
            # Pass through the value
            self.result = self.value
            self.true_path = self.value
            self.false_path = False
                
        except Exception as e:
            self.true_path = False
            self.false_path = NodeError.format(str(e))