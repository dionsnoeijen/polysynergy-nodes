from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="Unique List",
    category="list",
    icon="list.svg"
)
class UniqueList(Node):
    input_list: list = NodeVariableSettings(label="Input List", has_in=True, dock=True)
    key: str = NodeVariableSettings(
        label="Key (optional)",
        has_in=True,
        dock=True,
        info="If list contains dicts, use this key to determine uniqueness"
    )

    true_path: bool | list = PathSettings(label="Unique List", info="List with duplicates removed")
    false_path: bool | dict = PathSettings(label="Error", info="Triggered if filtering fails")

    def execute(self):
        try:
            if not isinstance(self.input_list, list):
                raise ValueError("Input must be a list")

            seen = set()
            result = []

            for item in self.input_list:
                if self.key and isinstance(item, dict):
                    identifier = item.get(self.key)
                else:
                    identifier = item

                if identifier not in seen:
                    seen.add(identifier)
                    result.append(item)

            self.true_path = result

        except Exception as e:
            self.false_path = {"error": str(e)}
