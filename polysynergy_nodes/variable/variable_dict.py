import json

from polysynergy_node_runner.execution_context.replace_placeholders import replace_placeholders
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(name="Variable Dict", category="variable", version=1.0)
class VariableDict(Node):
    value: dict[str, any] = NodeVariableSettings(label="Value", dock=True, has_out=True)
    value_as_json_string: str = NodeVariableSettings(label="Value as Json String", has_out=True)

    merge: dict | None = NodeVariableSettings(
        label="Merge",
        has_in=True,
        info="Dictionary to merge into value"
    )

    true_path: bool | dict = PathSettings(label="Dict", info="The value is a valid JSON string with placeholders replaced")
    false_path: bool | dict = PathSettings(label="Error")

    def _get_all_merge_inputs(self):
        """Get all dict values from connections to the 'merge' handle"""
        merge_dicts = []
        connections = [c for c in self.get_in_connections() if c.target_handle == 'merge']

        for conn in connections:
            source_node = self.state.get_node_by_id(conn.source_node_id)
            # Get the value from the source node's output handle
            source_value = getattr(source_node, conn.source_handle, None)
            if isinstance(source_value, dict):
                merge_dicts.append(source_value)

        return merge_dicts

    async def execute(self):
        try:
            # Ensure value is a dict
            if not isinstance(self.value, dict):
                self.value = {}

            # Get all incoming dicts on the merge handle
            merge_dicts = self._get_all_merge_inputs()

            # Merge all incoming dicts
            for merge_dict in merge_dicts:
                self.value.update(merge_dict)

            self.value_as_json_string = json.dumps(self.value)

            replaced = replace_placeholders(
                data=self.value_as_json_string,
                values=self.value,
                state=self.state,
                current_node=self
            )

            if isinstance(replaced, str):
                parsed = json.loads(replaced)
            else:
                parsed = replaced

            self.true_path = parsed
            self.false_path = False
            return parsed

        except Exception as e:
            self.false_path = {'error': str(e)}
            self.true_path = False
            return None