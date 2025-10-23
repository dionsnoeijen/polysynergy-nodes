from polysynergy_node_runner.setup_context.dock_property import dock_property
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="Slice List",
    category="list",
    icon="list.svg",
    version=1.0
)
class SliceList(Node):
    input_list: list = NodeVariableSettings(
        label="Input List",
        has_in=True,
        dock=True,
        info="The list to slice"
    )

    slice_mode: str = NodeVariableSettings(
        label="Slice Mode",
        default="last_n",
        dock=dock_property(
            select_values={
                "first_n": "First N items",
                "last_n": "Last N items",
                "range": "Range (from index to index)",
                "from_index": "From index to end",
                "to_index": "From start to index"
            }
        ),
        has_in=True,
        info="How to slice the list"
    )

    count: int = NodeVariableSettings(
        label="Count",
        default=10,
        dock=True,
        has_in=True,
        info="Number of items to take (for first_n/last_n modes)"
    )

    start_index: int = NodeVariableSettings(
        label="Start Index",
        default=0,
        dock=True,
        has_in=True,
        info="Starting index (0-based, for range/from_index modes)"
    )

    end_index: int = NodeVariableSettings(
        label="End Index",
        default=10,
        dock=True,
        has_in=True,
        info="Ending index (exclusive, for range/to_index modes)"
    )

    sliced_list: list = NodeVariableSettings(
        label="Sliced List",
        has_out=True,
        info="The resulting sliced list"
    )

    original_length: int = NodeVariableSettings(
        label="Original Length",
        has_out=True,
        info="Length of the original list"
    )

    sliced_length: int = NodeVariableSettings(
        label="Sliced Length",
        has_out=True,
        info="Length of the sliced list"
    )

    true_path: bool | list = PathSettings(
        label="Sliced List",
        info="Returns the sliced list"
    )
    false_path: bool | dict = PathSettings(
        label="Error",
        info="Triggered if slicing fails"
    )

    def execute(self):
        try:
            if not isinstance(self.input_list, list):
                raise ValueError("Input is not a list")

            self.original_length = len(self.input_list)
            result = []

            if self.slice_mode == "first_n":
                # Take first N items
                result = self.input_list[:self.count]

            elif self.slice_mode == "last_n":
                # Take last N items
                result = self.input_list[-self.count:] if self.count > 0 else self.input_list

            elif self.slice_mode == "range":
                # Take items from start_index to end_index
                result = self.input_list[self.start_index:self.end_index]

            elif self.slice_mode == "from_index":
                # Take items from start_index to end
                result = self.input_list[self.start_index:]

            elif self.slice_mode == "to_index":
                # Take items from start to end_index
                result = self.input_list[:self.end_index]

            self.sliced_list = result
            self.sliced_length = len(result)
            self.true_path = result
            self.false_path = False

        except Exception as e:
            self.false_path = {"error": str(e)}
            self.true_path = False
            self.sliced_list = []
            self.sliced_length = 0
            self.original_length = 0
