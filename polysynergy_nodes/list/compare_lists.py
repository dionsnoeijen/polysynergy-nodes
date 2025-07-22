from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings
from polysynergy_node_runner.setup_context.dock_property import dock_property

@node(
    name="Compare Lists",
    category="list",
    icon="list.svg",
)
class CompareLists(Node):
    list_a: list = NodeVariableSettings(label="List A", has_in=True)
    list_b: list = NodeVariableSettings(label="List B", has_in=True)

    comparison_type: str = NodeVariableSettings(
        label="Comparison Type",
        default="intersection",
        dock=dock_property(select_values={
            "only_in_a": "Only in A",
            "only_in_b": "Only in B",
            "intersection": "Intersection",
            "symmetric_difference": "Symmetric Difference"
        }),
        has_in=True
    )

    true_path: bool | list = PathSettings(label="Comparison Result", info="Result of the selected comparison type")
    false_path: bool | dict = PathSettings(label="Error", info="Error if input is invalid")

    def execute(self):
        try:
            a = set(self.list_a or [])
            b = set(self.list_b or [])

            if self.comparison_type == "only_in_a":
                self.true_path = list(a - b)
            elif self.comparison_type == "only_in_b":
                self.true_path = list(b - a)
            elif self.comparison_type == "intersection":
                self.true_path = list(a & b)
            elif self.comparison_type == "symmetric_difference":
                self.true_path = list(a ^ b)
            else:
                raise ValueError(f"Invalid comparison type: {self.comparison_type}")

        except Exception as e:
            self.false_path = {"error": str(e)}
