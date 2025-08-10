from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(name="String to Bytes", category="cast", icon="cast.svg")
class StringToBytes(Node):
    input_value: str = NodeVariableSettings(label="Input", dock=True, has_in=True)
    
    true_path: bytes = PathSettings(label="Bytes", info="Successfully converted bytes")
    false_path: dict = PathSettings(label="Error", info="Conversion failed")

    def execute(self):
        try:
            if isinstance(self.input_value, str):
                self.true_path = self.input_value.encode("utf-8")
            elif isinstance(self.input_value, bytes):
                # Already bytes, pass through
                self.true_path = self.input_value
            else:
                # Try to convert to string first, then to bytes
                self.true_path = str(self.input_value).encode("utf-8")
        except Exception as e:
            self.false_path = NodeError.format(e)
            self.true_path = False