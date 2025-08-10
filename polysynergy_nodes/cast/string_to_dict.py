import json
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(name="String to Dict", category="cast", icon="cast.svg")
class StringToDict(Node):
    input_value: str = NodeVariableSettings(label="JSON String", dock=True, has_in=True)
    
    true_path: dict = PathSettings(label="Dict", info="Successfully parsed JSON dictionary")
    false_path: dict = PathSettings(label="Error", info="JSON parsing failed")

    def execute(self):
        try:
            if isinstance(self.input_value, str):
                self.true_path = json.loads(self.input_value.strip())
            else:
                # Try to convert to string first, then parse JSON
                self.true_path = json.loads(str(self.input_value))
        except json.JSONDecodeError as e:
            self.false_path = NodeError.format(f"Invalid JSON: {e}")
            self.true_path = False
        except Exception as e:
            self.false_path = NodeError.format(e)
            self.true_path = False