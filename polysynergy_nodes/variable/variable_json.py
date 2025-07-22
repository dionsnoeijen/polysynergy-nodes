import json
import traceback

from polysynergy_node_runner.execution_context.replace_placeholders import replace_placeholders
from polysynergy_node_runner.setup_context.dock_property import dock_json
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="Variable Json",
    category="variable",
    icon='json.svg',
    version=1.01,
)
class VariableJson(Node):
    value: str | dict | list = NodeVariableSettings(
        label="Value",
        dock=dock_json(),
        has_in=True,
    )
    values: dict = NodeVariableSettings(label="Values", dock=True, has_in=True, has_out=True)
    append: dict | None = NodeVariableSettings(label="Append", dock=True, has_in=True)

    value_as_dict_or_list: dict | list = NodeVariableSettings(label="Value as dict or list", has_out=True)

    true_path: bool | str = PathSettings(label="Json String", info="The value is a valid JSON string with placeholders replaced")
    false_path: bool | dict = PathSettings(label="Error")

    def execute(self):
        try:
            self.values = replace_placeholders(data=self.values, values=self.values, state=self.state)
            self.append = replace_placeholders(data=self.append, values=self.values, state=self.state)

            if isinstance(self.value, str):
                json_str = self.value
            else:
                try:
                    json_str = json.dumps(self.value)
                except (TypeError, ValueError):
                    raise ValueError("Value is not JSON-serializable")

            replaced = replace_placeholders(data=json_str, values=self.values, state=self.state)

            if isinstance(replaced, str):
                parsed = json.loads(replaced)
            else:
                parsed = replaced

            if isinstance(parsed, dict) and self.append:
                if not isinstance(self.append, dict):
                    raise ValueError("Append must be a dictionary")
                parsed.update(self.append)

            self.value_as_dict_or_list = parsed

            self.true_path = json.dumps(parsed)

        except Exception as e:
            self.false_path = {
                'error': str(e),
                'traceback': traceback.format_exc(),
                'value_input': self.value,
                'values_input': self.values,
                'append_input': self.append,
                'node': self.handle,
                'node_type': self.path
            }
