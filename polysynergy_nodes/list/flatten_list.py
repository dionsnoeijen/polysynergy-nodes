from polysynergy_node_runner.setup_context.dock_property import dock_property
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="Flatten List",
    category="list",
    icon="list.svg",
    version=1.0
)
class FlattenList(Node):
    input_list: list = NodeVariableSettings(
        label="Input List",
        has_in=True,
        dock=True,
        info="Nested list to flatten (e.g., [[1,2], [3,4]] → [1,2,3,4])"
    )

    depth: str = NodeVariableSettings(
        label="Flatten Depth",
        default="all",
        dock=dock_property(
            select_values={
                "1": "One level",
                "2": "Two levels",
                "all": "All levels (fully flat)"
            }
        ),
        has_in=True,
        info="How many levels deep to flatten"
    )

    flattened_list: list = NodeVariableSettings(
        label="Flattened List",
        has_out=True,
        info="The flattened list"
    )

    original_length: int = NodeVariableSettings(
        label="Original Length",
        has_out=True,
        info="Number of items in original list"
    )

    flattened_length: int = NodeVariableSettings(
        label="Flattened Length",
        has_out=True,
        info="Number of items in flattened list"
    )

    true_path: bool | list = PathSettings(
        label="Flattened List",
        info="Returns the flattened list"
    )
    false_path: bool | dict = PathSettings(
        label="Error",
        info="Triggered if flattening fails"
    )

    def execute(self):
        try:
            if not isinstance(self.input_list, list):
                raise ValueError("Input is not a list")

            self.original_length = len(self.input_list)

            if self.depth == "all":
                result = self._flatten_fully(self.input_list)
            elif self.depth == "1":
                result = self._flatten_one_level(self.input_list)
            elif self.depth == "2":
                result = self._flatten_one_level(
                    self._flatten_one_level(self.input_list)
                )
            else:
                result = self.input_list

            self.flattened_list = result
            self.flattened_length = len(result)
            self.true_path = result
            self.false_path = False

        except Exception as e:
            self.false_path = {"error": str(e)}
            self.true_path = False
            self.flattened_list = []
            self.flattened_length = 0
            self.original_length = 0

    def _flatten_one_level(self, lst):
        """Flatten one level of nesting"""
        result = []
        for item in lst:
            if isinstance(item, list):
                result.extend(item)
            else:
                result.append(item)
        return result

    def _flatten_fully(self, lst):
        """Recursively flatten all levels"""
        result = []
        for item in lst:
            if isinstance(item, list):
                result.extend(self._flatten_fully(item))
            else:
                result.append(item)
        return result
