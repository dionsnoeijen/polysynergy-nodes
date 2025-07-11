import json

from polysynergy_nodes.base.setup_context.dock_property import dock_json
from polysynergy_nodes.base.setup_context.node import Node
from polysynergy_nodes.base.setup_context.node_decorator import node
from polysynergy_nodes.base.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_nodes.base.setup_context.path_settings import PathSettings
from polysynergy_nodes.base.setup_context.node_error import NodeError


@node(
    name="Zip Inject",
    category="list",
    icon="list.svg",
    version=1.1,
)
class ZipInject(Node):

    source_list: list = NodeVariableSettings(
        label="Source List (dicts)",
        has_in=True
    )

    source_list_as_string: str = NodeVariableSettings(
        label="Source List (as JSON String)",
        has_in=True,
        dock=dock_json()
    )

    values_to_inject: list = NodeVariableSettings(
        label="Values to Inject",
        has_in=True
    )

    values_to_inject_as_string: str = NodeVariableSettings(
        label="Values to Inject (as JSON String)",
        has_in=True,
        dock=dock_json()
    )

    target_path: str = NodeVariableSettings(
        label="Target Path (e.g. result.score)",
        has_in=True,
        dock=True,
        required=True
    )

    true_path: list = PathSettings(label="Zipped Output")
    false_path: bool | dict = PathSettings(label="Error")

    def _parse_json_input(self, value, fallback_name):
        if isinstance(value, (list, dict)):
            return value
        try:
            return json.loads(value)
        except Exception as e:
            raise ValueError(f"Invalid JSON input in {fallback_name}: {str(e)}")

    def execute(self):
        try:
            items = self._parse_json_input(self.source_list or self.source_list_as_string, "source_list")
            values = self._parse_json_input(self.values_to_inject or self.values_to_inject_as_string, "values_to_inject")

            if not isinstance(items, list):
                raise ValueError("Parsed source_list is not a list.")
            if not isinstance(values, list):
                raise ValueError("Parsed values_to_inject is not a list.")
            if len(items) != len(values):
                raise ValueError("List length is not equal.")

            path_parts = self.target_path.split(".") if self.target_path else []

            for item, value in zip(items, values):
                if not path_parts:
                    if not isinstance(value, dict):
                        raise ValueError("When target_path is empty, each value_to_inject must be a dict.")
                    item.update(value)
                else:
                    target = item
                    for part in path_parts[:-1]:
                        target = target.setdefault(part, {})
                    target[path_parts[-1]] = value

            self.true_path = items

        except Exception as e:
            self.false_path = NodeError.format(e)