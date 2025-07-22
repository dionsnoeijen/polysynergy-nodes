from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(name="Wrap List Values", category="list", icon="list.svg")
class WrapListValues(Node):
    items: list = NodeVariableSettings(label="Input List", has_in=True)
    key_name: str = NodeVariableSettings(label="Key Name", dock=True, default="value", has_in=True)

    true_path: list = PathSettings(label="Wrapped List")

    def execute(self):
        key = self.key_name or "value"
        if not isinstance(self.items, list):
            self.true_path = []
            return
        self.true_path = [{key: item} for item in self.items]