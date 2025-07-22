import base64
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="Decode Base64",
    category="encoding",
    icon="base64.svg",
)
class DecodeBase64(Node):

    value: bytes | str = NodeVariableSettings(label="Value", dock=True, has_in=True)

    true_path: bool | str = PathSettings(label="Decoded Value", info="The decoded value")
    false_path: bool | dict = PathSettings(label="Error", info="If the decoding fails")

    def execute(self):
        try:
            self.true_path = base64.b64decode(self.value).decode()
        except Exception as e:
            self.false_path = NodeError.format(e)
