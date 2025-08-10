from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(name="String to Float", category="cast", icon="cast.svg")
class StringToFloat(Node):
    input_value: str = NodeVariableSettings(label="String", dock=True, has_in=True)
    
    true_path: float = PathSettings(label="Float", info="Successfully converted to float")
    false_path: dict = PathSettings(label="Error", info="Conversion to float failed")

    def execute(self):
        try:
            if isinstance(self.input_value, str):
                # Strip whitespace and convert
                self.true_path = float(self.input_value.strip())
            elif isinstance(self.input_value, (int, float)):
                # Already a number, convert to float
                self.true_path = float(self.input_value)
            else:
                # Try to convert to string first, then to float
                self.true_path = float(str(self.input_value).strip())
        except ValueError as e:
            self.false_path = NodeError.format(f"Invalid float format: {e}")
            self.true_path = False
        except Exception as e:
            self.false_path = NodeError.format(e)
            self.true_path = False