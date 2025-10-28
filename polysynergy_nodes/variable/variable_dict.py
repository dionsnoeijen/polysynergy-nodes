import json

from polysynergy_node_runner.execution_context.replace_placeholders import replace_placeholders
from polysynergy_node_runner.setup_context.dock_property import dock_dict, dock_property
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
        dock=dock_dict(
            key_label="Key",
            value_label="Dict (connect input)",
            info="Merge multiple dicts"
        ),
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

    operation: str = NodeVariableSettings(
        label="Operation",
        dock=dock_property(select_values={
            "merge": "Merge - Update/overwrite keys",
            "append_or_extend": "Append/Extend - Smart list operations"
        }),
        default="merge",
        info="Merge updates dict keys. Append/Extend adds to lists (auto-detects single item vs multiple items)"
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
                            # If it's not valid JSON, treat it as a plain string value
                            # This allows both JSON strings and plain strings
                            pass  # Keep dict_value as-is (plain string)

                    # Handle bytes (sometimes comes from database)
                    if isinstance(dict_value, bytes):
                        try:
                            dict_value = json.loads(dict_value.decode('utf-8'))
                        except (json.JSONDecodeError, UnicodeDecodeError):
                            raise ValueError(
                                f"Wrap value for key '{key}' is bytes but not valid JSON"
                            )

                    # Accept dict, list, str, int, float, bool, None - basically any JSON-serializable value
                    # This allows wrapping both complex structures (dict/list) and simple values (strings, numbers)
                    result[key] = dict_value
                self.value = result
            else:
                # Normal mode: use value and merge
                # Get all incoming dicts on the merge handle
                merge_dicts = self._get_all_merge_inputs()

                print(f"[VariableDict DEBUG] value BEFORE merge: {self.value}")
                print(f"[VariableDict DEBUG] merge_dicts: {merge_dicts}")
                print(f"[VariableDict DEBUG] operation: {self.operation}")

                # Merge all incoming dicts with selected operation
                for merge_dict in merge_dicts:
                    if self.operation == "append_or_extend":
                        # Smart list operations: auto-detect append vs extend
                        for key, new_value in merge_dict.items():
                            print(f"[VariableDict DEBUG] Processing key='{key}', new_value='{new_value}'")
                            if key in self.value and isinstance(self.value[key], list):
                                # Key exists and is a list
                                if isinstance(new_value, list):
                                    # New value is list → extend
                                    print(f"[VariableDict DEBUG] EXTENDING list with: {new_value}")
                                    self.value[key].extend(new_value)
                                else:
                                    # New value is single item → append
                                    print(f"[VariableDict DEBUG] APPENDING item: {new_value}")
                                    self.value[key].append(new_value)
                            else:
                                # Key doesn't exist or not a list → fallback to merge
                                print(f"[VariableDict DEBUG] MERGING (key doesn't exist or not list): {key} = {new_value}")
                                self.value[key] = new_value
                    else:  # "merge" (default)
                        # Original behavior: overwrite keys
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