from polysynergy_node_runner.setup_context.dock_property import dock_property
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="Remove Item",
    category="list",
    icon="list.svg",
    version=1.0
)
class RemoveItem(Node):
    input_list: list = NodeVariableSettings(
        label="Input List",
        has_in=True,
        dock=True,
        info="The list to remove items from"
    )

    mode: str = NodeVariableSettings(
        label="Mode",
        default="by_value",
        dock=dock_property(
            select_values={
                "by_value": "Remove by value (first occurrence)",
                "by_value_all": "Remove by value (all occurrences)",
                "by_index": "Remove by index"
            }
        ),
        has_in=True,
        info="How to identify items to remove"
    )

    value: any = NodeVariableSettings(
        label="Value",
        has_in=True,
        dock=True,
        info="The value to remove (for by_value modes)"
    )

    index: int = NodeVariableSettings(
        label="Index",
        default=0,
        dock=True,
        has_in=True,
        info="Position to remove from (for by_index mode, 0-based)"
    )

    modified_list: list = NodeVariableSettings(
        label="Modified List",
        has_out=True,
        info="The list with item(s) removed"
    )

    removed_count: int = NodeVariableSettings(
        label="Removed Count",
        has_out=True,
        info="Number of items removed"
    )

    original_length: int = NodeVariableSettings(
        label="Original Length",
        has_out=True,
        info="Length of the original list"
    )

    new_length: int = NodeVariableSettings(
        label="New Length",
        has_out=True,
        info="Length of the modified list"
    )

    true_path: bool | list = PathSettings(
        label="Modified List",
        info="Returns the list with item(s) removed"
    )
    false_path: bool | dict = PathSettings(
        label="Error",
        info="Triggered if removal fails"
    )

    def execute(self):
        try:
            if not isinstance(self.input_list, list):
                raise ValueError("Input is not a list")

            self.original_length = len(self.input_list)
            result = self.input_list.copy()
            removed_count = 0

            if self.mode == "by_value":
                # Remove first occurrence of value
                try:
                    result.remove(self.value)
                    removed_count = 1
                except ValueError:
                    # Value not in list - not an error, just no removal
                    pass

            elif self.mode == "by_value_all":
                # Remove all occurrences of value
                initial_length = len(result)
                result = [item for item in result if item != self.value]
                removed_count = initial_length - len(result)

            elif self.mode == "by_index":
                # Remove by index
                if self.index < -len(result) or self.index >= len(result):
                    raise IndexError(f"Index {self.index} out of range for list of length {len(result)}")
                result.pop(self.index)
                removed_count = 1

            self.modified_list = result
            self.removed_count = removed_count
            self.new_length = len(result)
            self.true_path = result
            self.false_path = False

        except Exception as e:
            self.false_path = {"error": str(e)}
            self.true_path = False
            self.modified_list = []
            self.removed_count = 0
            self.original_length = 0
            self.new_length = 0
