from polysynergy_node_runner.setup_context.dock_property import dock_property
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="Append/Insert Item",
    category="list",
    icon="list.svg",
    version=1.0
)
class AppendInsertItem(Node):
    input_list: list = NodeVariableSettings(
        label="Input List",
        has_in=True,
        dock=True,
        info="The list to add an item to"
    )

    item: any = NodeVariableSettings(
        label="Item",
        has_in=True,
        dock=True,
        info="The item to add to the list"
    )

    mode: str = NodeVariableSettings(
        label="Mode",
        default="append",
        dock=dock_property(
            select_values={
                "append": "Append (add to end)",
                "prepend": "Prepend (add to start)",
                "insert": "Insert at index"
            }
        ),
        has_in=True,
        info="Where to add the item"
    )

    index: int = NodeVariableSettings(
        label="Index",
        default=0,
        dock=True,
        has_in=True,
        info="Position to insert at (for insert mode, 0-based)"
    )

    modified_list: list = NodeVariableSettings(
        label="Modified List",
        has_out=True,
        info="The list with the item added"
    )

    new_length: int = NodeVariableSettings(
        label="New Length",
        has_out=True,
        info="Length of the modified list"
    )

    true_path: bool | list = PathSettings(
        label="Modified List",
        info="Returns the list with item added"
    )
    false_path: bool | dict = PathSettings(
        label="Error",
        info="Triggered if operation fails"
    )

    def execute(self):
        try:
            if not isinstance(self.input_list, list):
                raise ValueError("Input is not a list")

            # Create a copy to avoid modifying the original
            result = self.input_list.copy()

            if self.mode == "append":
                result.append(self.item)
            elif self.mode == "prepend":
                result.insert(0, self.item)
            elif self.mode == "insert":
                # Ensure index is within valid range
                if self.index < 0 or self.index > len(result):
                    raise ValueError(f"Index {self.index} out of range for list of length {len(result)}")
                result.insert(self.index, self.item)

            self.modified_list = result
            self.new_length = len(result)
            self.true_path = result
            self.false_path = False

        except Exception as e:
            self.false_path = {"error": str(e)}
            self.true_path = False
            self.modified_list = []
            self.new_length = 0
