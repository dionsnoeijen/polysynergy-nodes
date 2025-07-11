from polysynergy_nodes.base.setup_context.dock_property import dock_property
from polysynergy_nodes.base.setup_context.node import Node
from polysynergy_nodes.base.setup_context.node_decorator import node
from polysynergy_nodes.base.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_nodes.base.setup_context.path_settings import PathSettings


@node(
    name="Filter List",
    category="list",
    icon="list.svg",
)
class FilterList(Node):
    input_list: list = NodeVariableSettings(label="Input List", has_in=True, dock=True)
    field: str = NodeVariableSettings(label="Field to Match", has_in=True, dock=True, info="If list contains dicts, this selects the field to filter on.")
    match_value: str = NodeVariableSettings(label="Match Value", has_in=True, dock=True)
    match_mode: str = NodeVariableSettings(
        label="Match Mode",
        default="equals",
        dock=dock_property(
            select_values={
                "equals": "Equals",
                "not_equals": "Not Equals",
                "contains": "Contains",
                "not_contains": "Not Contains",
                "starts_with": "Starts With",
                "ends_with": "Ends With",
                "greater_than": "Greater Than",
                "less_than": "Less Than",
                "in": "In List",
                "not_in": "Not In List"
            }
        ),
        has_in=True
    )

    true_path: bool | list = PathSettings(label="Filtered List", info="List of items that matched the condition")
    false_path: bool | dict = PathSettings(label="Error", info="Triggered if filtering fails")

    def execute(self):
        try:
            if not isinstance(self.input_list, list):
                raise ValueError("Input is not a list")

            result = []

            for item in self.input_list:
                value = item
                if isinstance(item, dict) and self.field:
                    value = item.get(self.field)

                if self._matches(value):
                    result.append(item)

            self.true_path = result
        except Exception as e:
            self.false_path = {"error": str(e)}

    def _matches(self, value):
        mode = self.match_mode
        target = self.match_value

        try:
            if mode == "equals":
                return value == target
            elif mode == "not_equals":
                return value != target
            elif mode == "contains":
                return target in value
            elif mode == "not_contains":
                return target not in value
            elif mode == "starts_with":
                return str(value).startswith(str(target))
            elif mode == "ends_with":
                return str(value).endswith(str(target))
            elif mode == "greater_than":
                return float(value) > float(target)
            elif mode == "less_than":
                return float(value) < float(target)
            elif mode == "in":
                return value in target if isinstance(target, list) else value in str(target)
            elif mode == "not_in":
                return value not in target if isinstance(target, list) else value not in str(target)
        except Exception:
            return False

        return False
