from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(name="Dict Join", category="cast", icon="cast.svg", version=1.0)
class DictJoin(Node):
    """
    Joins dictionary key-value pairs into a string with configurable separators.

    Useful for building query strings, CSV-like formats, or any custom string format from dictionary data.
    """

    input_dict: dict = NodeVariableSettings(
        label="Dictionary",
        dock=True,
        has_in=True,
        required=True,
        info="Dictionary to join into a string"
    )

    item_separator: str = NodeVariableSettings(
        label="Item Separator",
        dock=True,
        has_in=True,
        default="&",
        info="Separator between items (e.g., '&', ', ', '|')"
    )

    key_value_separator: str = NodeVariableSettings(
        label="Key-Value Separator",
        dock=True,
        has_in=True,
        default="=",
        info="Separator between key and value (e.g., '=', ': '). Leave empty for values only."
    )

    skip_empty: bool = NodeVariableSettings(
        label="Skip Empty",
        dock=True,
        has_in=True,
        default=True,
        info="Skip null or empty string values"
    )

    true_path: str | bool = PathSettings(
        label="Result",
        info="The joined string"
    )

    false_path: dict | bool = PathSettings(
        label="Error",
        info="Error information if input is invalid"
    )

    async def execute(self):
        # Validate input is a dict
        if not isinstance(self.input_dict, dict):
            self.false_path = NodeError.format(ValueError("Input must be a dictionary"))
            self.true_path = False
            return

        try:
            items = []

            for key, value in self.input_dict.items():
                # Skip empty values if configured
                if self.skip_empty and (value is None or value == ""):
                    continue

                # Convert value to string
                str_value = str(value) if value is not None else ""

                # Build item
                if self.key_value_separator:
                    # Include key: "key=value"
                    item = f"{key}{self.key_value_separator}{str_value}"
                else:
                    # Values only: just the value
                    item = str_value

                items.append(item)

            # Join all items
            self.true_path = self.item_separator.join(items)
            self.false_path = False

        except Exception as e:
            self.false_path = NodeError.format(e)
            self.true_path = False
