from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="Aggregate List",
    category="list",
    icon="list.svg",
    version=1.0
)
class AggregateList(Node):
    input_list: list = NodeVariableSettings(
        label="Input List",
        has_in=True,
        dock=True,
        info="List of numbers (or dicts with numeric field)"
    )

    field: str = NodeVariableSettings(
        label="Field",
        default="",
        dock=True,
        has_in=True,
        info="If list contains dicts, aggregate this numeric field (leave empty for direct values)"
    )

    min_value: float = NodeVariableSettings(
        label="Minimum",
        has_out=True,
        info="Minimum value in the list"
    )

    max_value: float = NodeVariableSettings(
        label="Maximum",
        has_out=True,
        info="Maximum value in the list"
    )

    sum_value: float = NodeVariableSettings(
        label="Sum",
        has_out=True,
        info="Sum of all values"
    )

    average_value: float = NodeVariableSettings(
        label="Average",
        has_out=True,
        info="Average (mean) of all values"
    )

    count: int = NodeVariableSettings(
        label="Count",
        has_out=True,
        info="Number of values aggregated"
    )

    true_path: bool | dict = PathSettings(
        label="Aggregations",
        info="Returns dict with all aggregation results"
    )
    false_path: bool | dict = PathSettings(
        label="Error",
        info="Triggered if aggregation fails"
    )

    def execute(self):
        try:
            if not isinstance(self.input_list, list):
                raise ValueError("Input is not a list")

            if len(self.input_list) == 0:
                raise ValueError("Cannot aggregate empty list")

            # Extract numeric values
            values = []
            for item in self.input_list:
                if self.field and isinstance(item, dict):
                    value = item.get(self.field)
                else:
                    value = item

                # Convert to float and add to values
                try:
                    values.append(float(value))
                except (TypeError, ValueError):
                    # Skip non-numeric values
                    continue

            if len(values) == 0:
                raise ValueError("No numeric values found in list")

            # Calculate aggregations
            self.min_value = min(values)
            self.max_value = max(values)
            self.sum_value = sum(values)
            self.average_value = sum(values) / len(values)
            self.count = len(values)

            self.true_path = {
                "min": self.min_value,
                "max": self.max_value,
                "sum": self.sum_value,
                "average": self.average_value,
                "count": self.count
            }
            self.false_path = False

        except Exception as e:
            self.false_path = {"error": str(e)}
            self.true_path = False
            self.min_value = 0
            self.max_value = 0
            self.sum_value = 0
            self.average_value = 0
            self.count = 0
