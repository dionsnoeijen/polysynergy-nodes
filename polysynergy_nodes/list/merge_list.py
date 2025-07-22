from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings

@node(
    name="Merge Lists",
    category="list",
    icon="list.svg",
)
class MergeLists(Node):
    list_a: list = NodeVariableSettings(label="List A", has_in=True)
    list_b: list = NodeVariableSettings(label="List B", has_in=True)
    remove_duplicates: bool = NodeVariableSettings(label="Remove Duplicates", has_in=True, default=False)

    true_path: bool | list = PathSettings(label="Merged List", info="Combined list of A and B")
    false_path: bool | dict = PathSettings(label="Error", info="Triggered if merging fails")

    def execute(self):
        try:
            if not isinstance(self.list_a, list):
                raise ValueError("List A is not a valid list")
            if not isinstance(self.list_b, list):
                raise ValueError("List B is not a valid list")

            merged = self.list_a + self.list_b

            if self.remove_duplicates:
                seen = set()
                unique = []
                for item in merged:
                    if str(item) not in seen:
                        seen.add(str(item))
                        unique.append(item)
                merged = unique

            self.true_path = merged
        except Exception as e:
            self.false_path = {"error": str(e)}
