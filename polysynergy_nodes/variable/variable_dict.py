import json

from polysynergy_nodes.base.execution_context.replace_placeholders import replace_placeholders
from polysynergy_nodes.base.setup_context.node import Node
from polysynergy_nodes.base.setup_context.node_decorator import node
from polysynergy_nodes.base.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_nodes.base.setup_context.path_settings import PathSettings


@node(name="Variable Dict", category="variable")
class VariableDict(Node):
    value: dict[str, any] = NodeVariableSettings(label="Value", dock=True, has_out=True)
    value_as_json_string: str = NodeVariableSettings(label="Value as Json String", has_out=True)

    true_path: bool | dict = PathSettings(label="Dict", info="The value is a valid JSON string with placeholders replaced")
    false_path: bool | dict = PathSettings(label="Error")

    def execute(self):
        try:
            self.value_as_json_string = json.dumps(self.value)

            replaced = replace_placeholders(
                data=self.value_as_json_string,
                values=self.value,
                state=self.state
            )

            if isinstance(replaced, str):
                parsed = json.loads(replaced)
            else:
                parsed = replaced

            self.true_path = parsed
            return parsed

        except Exception as e:
            self.false_path = {'error': str(e)}
            return None