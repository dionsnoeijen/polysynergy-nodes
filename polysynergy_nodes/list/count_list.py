from polysynergy_nodes.base.setup_context.node import Node
from polysynergy_nodes.base.setup_context.node_decorator import node
from polysynergy_nodes.base.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_nodes.base.setup_context.path_settings import PathSettings


@node(
    name="Count List",
    category="list",
    icon="list.svg",
)
class CountList(Node):
    input_list: list = NodeVariableSettings(label="List", has_in=True)

    true_path: bool | int = PathSettings(label="Count", info="Length > 0")
    false_path: bool | int = PathSettings(label="Empty", info="Length == 0")

    def execute(self):
        count = len(self.input_list)
        if count > 0:
            self.true_path = count
        else:
            self.false_path = True