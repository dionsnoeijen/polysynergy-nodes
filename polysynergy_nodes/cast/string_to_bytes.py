from polysynergy_nodes.base.setup_context.node import Node
from polysynergy_nodes.base.setup_context.node_decorator import node
from polysynergy_nodes.base.setup_context.node_variable_settings import NodeVariableSettings


@node(name="String to Bytes", category="cast")
class StringToBytes(Node):
    input_value: str | bytes = NodeVariableSettings(label="Input", dock=True, has_in=True, has_out=True)
    output_value: bytes = NodeVariableSettings(label="Output", dock=True, has_out=True)

    def execute(self):
        if isinstance(self.input_value, str):
            self.output_value = self.input_value.encode("utf-8")
        else:
            self.output_value = self.input_value

        return {"value": self.output_value}