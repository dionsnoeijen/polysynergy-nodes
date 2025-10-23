from polysynergy_node_runner.setup_context.dock_property import dock_property
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="Get Item by Index",
    category="list",
    icon="list.svg",
    version=1.0
)
class GetItemByIndex(Node):
    input_list: list = NodeVariableSettings(
        label="Input List",
        has_in=True,
        dock=True,
        info="The list to get an item from"
    )

    index: int = NodeVariableSettings(
        label="Index",
        default=0,
        dock=True,
        has_in=True,
        info="Position of the item to get (0-based, negative indices count from end)"
    )

    use_safe_mode: bool = NodeVariableSettings(
        label="Safe Mode",
        default=True,
        dock=True,
        has_in=True,
        info="If True, returns error path for out-of-bounds; if False, raises exception"
    )

    default_value: any = NodeVariableSettings(
        label="Default Value",
        default=None,
        dock=True,
        has_in=True,
        info="Value to return if index is out of bounds (only in safe mode)"
    )

    item: any = NodeVariableSettings(
        label="Item",
        has_out=True,
        info="The item at the specified index"
    )

    list_length: int = NodeVariableSettings(
        label="List Length",
        has_out=True,
        info="Total length of the list"
    )

    true_path: bool | any = PathSettings(
        label="Item Found",
        info="Returns the item at the specified index"
    )
    false_path: bool | dict = PathSettings(
        label="Error/Not Found",
        info="Triggered if index is out of bounds or operation fails"
    )

    def execute(self):
        try:
            if not isinstance(self.input_list, list):
                raise ValueError("Input is not a list")

            self.list_length = len(self.input_list)

            # Check if index is out of bounds
            if self.index < -len(self.input_list) or self.index >= len(self.input_list):
                if self.use_safe_mode:
                    self.item = self.default_value
                    self.true_path = self.default_value
                    self.false_path = {
                        "error": f"Index {self.index} out of range for list of length {len(self.input_list)}",
                        "default_value": self.default_value
                    }
                    return
                else:
                    raise IndexError(f"Index {self.index} out of range for list of length {len(self.input_list)}")

            self.item = self.input_list[self.index]
            self.true_path = self.item
            self.false_path = False

        except Exception as e:
            self.false_path = {"error": str(e)}
            self.true_path = False
            self.item = None
            self.list_length = 0
