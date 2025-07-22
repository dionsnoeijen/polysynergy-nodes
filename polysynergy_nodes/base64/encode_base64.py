import base64
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(name="Encode Base64", category="encoding")
class EncodeBase64(Node):

    value: str | bytes = NodeVariableSettings(label="Value", dock=True, has_in=True)

    true_path: bool | str = PathSettings(label="Encoded Value", info="The encoded value")
    false_path: bool | dict = PathSettings(label="Error", info="If the encoding fails")

    def execute(self):
        try:
            value = self.value.encode() if isinstance(self.value, str) else self.value
            self.true_path = base64.b64encode(value).decode()
        except Exception as e:
            self.false_path = NodeError.format(e)
