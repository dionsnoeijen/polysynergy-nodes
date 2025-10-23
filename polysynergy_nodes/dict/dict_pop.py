import json
from typing import Any
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="Dict Pop",
    category="dict",
    icon="dict.svg",
    version=1.0
)
class DictPop(Node):
    input_dict: dict | str | bytes = NodeVariableSettings(
        label="Input Dict",
        has_in=True,
        info="The dictionary to pop from (can be dict, JSON string, or bytes)"
    )

    key: str = NodeVariableSettings(
        label="Key",
        has_in=True,
        dock=True,
        info="The key to pop from the dictionary"
    )

    default_value: Any = NodeVariableSettings(
        label="Default Value",
        default=None,
        has_in=True,
        dock=True,
        info="Value to return if key doesn't exist"
    )

    popped_value: Any = NodeVariableSettings(
        label="Popped Value",
        has_out=True,
        info="The value that was removed from the dict"
    )

    remaining_dict: dict = NodeVariableSettings(
        label="Remaining Dict",
        has_out=True,
        info="The dictionary without the popped key"
    )

    key_existed: bool = NodeVariableSettings(
        label="Key Existed",
        has_out=True,
        info="Whether the key was present in the dict"
    )

    true_path: bool | Any = PathSettings(
        label="Popped Value",
        info="Returns the popped value (or default if key didn't exist)"
    )
    false_path: bool | dict = PathSettings(
        label="Error",
        info="Triggered if operation fails"
    )

    def execute(self):
        try:
            # Auto-parse JSON string/bytes to dict
            if isinstance(self.input_dict, (str, bytes)):
                try:
                    # Decode bytes to string if needed
                    dict_str = self.input_dict.decode('utf-8') if isinstance(self.input_dict, bytes) else self.input_dict
                    self.input_dict = json.loads(dict_str)
                except json.JSONDecodeError as e:
                    raise ValueError(f"Input string is not valid JSON: {str(e)}")
                except UnicodeDecodeError as e:
                    raise ValueError(f"Cannot decode bytes to string: {str(e)}")

            if not isinstance(self.input_dict, dict):
                raise ValueError("Input is not a dictionary")

            # Make a copy to avoid modifying the original
            result_dict = self.input_dict.copy()

            # Pop the key
            if self.key in result_dict:
                self.popped_value = result_dict.pop(self.key)
                self.key_existed = True
            else:
                self.popped_value = self.default_value
                self.key_existed = False

            self.remaining_dict = result_dict
            self.true_path = self.popped_value
            self.false_path = False

        except Exception as e:
            self.false_path = {"error": str(e)}
            self.true_path = False
            self.popped_value = None
            self.remaining_dict = {}
            self.key_existed = False
