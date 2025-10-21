import json

from polysynergy_node_runner.execution_context.replace_placeholders import replace_placeholders
from polysynergy_node_runner.setup_context.dock_property import dock_dict
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(name="Variable Dict", category="variable", version=1.0)
class VariableDict(Node):
    value: dict[str, any] = NodeVariableSettings(label="Value", dock=True, has_in=True)

    merge: dict | None = NodeVariableSettings(
        label="Merge",
        has_in=True,
        info="Dictionary to merge into value"
    )

    wrap: dict | None = NodeVariableSettings(
        label="Wrap",
        dock=dock_dict(
            key_label="Key",
            value_label="Dict (connect input)",
            info="Wrap multiple dicts under keys: {key1: dict1, key2: dict2}"
        ),
        has_in=True,
        info="Dynamically add keys and connect dicts to wrap them"
    )

    value_as_json_string: str = NodeVariableSettings(label="Value as Json String", has_out=True)

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

            # If wrap is used, prioritize that over value
            if self.wrap and isinstance(self.wrap, dict):
                # Wrap mode: each key maps to a dict
                result = {}
                for key, dict_value in self.wrap.items():
                    if dict_value is None:
                        # Skip None values (disconnected inputs)
                        continue

                    # Handle JSON strings (from SQL queries, etc.)
                    if isinstance(dict_value, str):
                        try:
                            dict_value = json.loads(dict_value)
                        except json.JSONDecodeError:
                            raise ValueError(
                                f"Wrap value for key '{key}' is a string but not valid JSON"
                            )

                    # Handle bytes (sometimes comes from database)
                    if isinstance(dict_value, bytes):
                        try:
                            dict_value = json.loads(dict_value.decode('utf-8'))
                        except (json.JSONDecodeError, UnicodeDecodeError):
                            raise ValueError(
                                f"Wrap value for key '{key}' is bytes but not valid JSON"
                            )

                    # Now it should be a dict or list
                    if not isinstance(dict_value, (dict, list)):
                        raise ValueError(
                            f"Wrap value for key '{key}' must be a dictionary or list, got {type(dict_value).__name__}"
                        )

                    result[key] = dict_value
                self.value = result
            else:
                # Normal mode: use value and merge
                # Get all incoming dicts on the merge handle
                merge_dicts = self._get_all_merge_inputs()

                # Merge all incoming dicts
                for merge_dict in merge_dicts:
                    self.value.update(merge_dict)

            # Try to serialize to JSON, but gracefully handle non-serializable objects like bytes
            try:
                self.value_as_json_string = json.dumps(self.value)

                replaced = replace_placeholders(
                    data=self.value_as_json_string,
                    values=self.value,
                    state=self.state,
                    current_node=self
                )
            except TypeError:
                # Contains non-serializable objects (e.g., bytes)
                # Skip JSON serialization and template replacement, use value directly
                self.value_as_json_string = None
                replaced = self.value

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