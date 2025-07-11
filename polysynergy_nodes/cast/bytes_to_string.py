from polysynergy_nodes.base.setup_context.node import Node
from polysynergy_nodes.base.setup_context.node_decorator import node
from polysynergy_nodes.base.setup_context.node_variable_settings import NodeVariableSettings


@node(name="Bytes to String", category="cast", has_enabled_switch=False)
class BytesToString(Node):
    input_value: bytes = NodeVariableSettings(label="Input", dock=True, has_in=True)
    output_value: str = NodeVariableSettings(label="Output", dock=True, has_out=True)

    def execute(self):
        if isinstance(self.input_value, bytes):
            self.output_value = self.input_value.decode("utf-8")
        else:
            self.output_value = str(self.input_value)

        return {"value": self.output_value}