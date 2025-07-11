from polysynergy_nodes.base.setup_context.node import Node
from polysynergy_nodes.base.setup_context.node_decorator import node
from polysynergy_nodes.base.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_nodes.base.setup_context.path_settings import PathSettings

@node(
    name="Contains In List",
    category="list",
    icon="list.svg",
)
class ContainsList(Node):
    input_list: list = NodeVariableSettings(label="List", has_in=True, dock=True)
    match_value: any = NodeVariableSettings(label="Value", has_in=True, dock=True)
    key: str = NodeVariableSettings(label="Key", has_in=True, dock=True, info="Optional: use when list contains dicts")

    true_path: bool | str = PathSettings(label="Match Found", info="Triggered if match is found")
    false_path: bool | dict = PathSettings(label="No Match or Error", info="Triggered if no match or invalid input")

    def execute(self):
        try:
            if not isinstance(self.input_list, list):
                raise ValueError("Input must be a list")

            found = False
            for item in self.input_list:
                value = item
                if self.key:
                    if not isinstance(item, dict):
                        continue
                    value = item.get(self.key)
                if str(value) == str(self.match_value):
                    found = True
                    break

            if found:
                self.true_path = True
                self.false_path = False
            else:
                self.true_path = False
                self.false_path = {"error": "Value not found"}

        except Exception as e:
            self.false_path = {"error": str(e)}
            self.true_path = False
