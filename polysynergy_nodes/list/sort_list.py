from polysynergy_nodes.base.setup_context.dock_property import dock_property
from polysynergy_nodes.base.setup_context.node import Node
from polysynergy_nodes.base.setup_context.node_decorator import node
from polysynergy_nodes.base.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_nodes.base.setup_context.path_settings import PathSettings

@node(
    name="Sort List",
    category="list",
    icon="list.svg"
)
class SortList(Node):
    input_list: list = NodeVariableSettings(label="Input List", has_in=True, dock=True)
    key: str = NodeVariableSettings(label="Sort Key (optional)", has_in=True, dock=True)
    sort_order: str = NodeVariableSettings(
        label="Sort Order",
        default="asc",
        dock=dock_property(select_values={
            "asc": "Ascending",
            "desc": "Descending"
        }),
        has_in=True
    )

    true_path: bool | list = PathSettings(label="Sorted List", info="Sorted version of input list")
    false_path: bool | dict = PathSettings(label="Error", info="Triggered if sorting fails")

    def execute(self):
        try:
            if not isinstance(self.input_list, list):
                raise ValueError("Input must be a list")

            reverse = self.sort_order == "desc"

            def sort_key(item):
                # Als er een key is, probeer die uit dicts te halen
                if self.key and isinstance(item, dict):
                    value = item.get(self.key, "")
                else:
                    value = item

                # Fallback voor niet-vergelijkbare types
                if isinstance(value, (int, float, str)):
                    return value
                return str(value)

            self.true_path = sorted(self.input_list, key=sort_key, reverse=reverse)

        except Exception as e:
            self.false_path = {"error": str(e)}