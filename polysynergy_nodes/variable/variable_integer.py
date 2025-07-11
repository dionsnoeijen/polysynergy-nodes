from polysynergy_nodes.base.setup_context.node import Node
from polysynergy_nodes.base.setup_context.node_decorator import node
from polysynergy_nodes.base.setup_context.node_variable_settings import NodeVariableSettings


@node(name="Variable Integer", category="variable")
class VariableInteger(Node):
    value: int = NodeVariableSettings(label="Value", dock=True, has_out=True)

    def execute(self):
        return self.value