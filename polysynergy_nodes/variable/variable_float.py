from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings


@node(name="Variable Float", category="variable")
class VariableFloat(Node):
    value: float = NodeVariableSettings(label="Value", dock=True, has_out=True)

    def execute(self):
        return self.value