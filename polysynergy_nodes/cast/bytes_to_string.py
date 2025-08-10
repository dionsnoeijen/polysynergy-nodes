from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(name="Bytes to String", category="cast", icon="cast.svg")
class BytesToString(Node):
    input_value: bytes = NodeVariableSettings(label="Input", dock=True, has_in=True)
    
    true_path: str = PathSettings(label="String", info="Successfully converted string")
    false_path: dict = PathSettings(label="Error", info="Conversion failed")

    def execute(self):
        try:
            if isinstance(self.input_value, bytes):
                self.true_path = self.input_value.decode("utf-8")
            else:
                # Try to convert other types to string
                self.true_path = str(self.input_value)
        except Exception as e:
            self.false_path = NodeError.format(e)
            self.true_path = False