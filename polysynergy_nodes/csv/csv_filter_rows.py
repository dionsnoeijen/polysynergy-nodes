from polysynergy_node_runner.setup_context.dock_property import dock_property
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="CSV Filter Rows",
    category="csv",
    icon="csv.svg",
    version=1.0
)
class CsvFilterRows(Node):
    data: list = NodeVariableSettings(
        label="Data",
        has_in=True,
        dock=True,
        info="List of dicts (CSV data with headers)"
    )

    column: str = NodeVariableSettings(
        label="Column Name",
        has_in=True,
        dock=True,
        info="The column to filter on"
    )

    operator: str = NodeVariableSettings(
        label="Operator",
        default="equals",
        dock=dock_property(
            select_values={
                "equals": "Equals (==)",
                "not_equals": "Not Equals (!=)",
                "contains": "Contains",
                "not_contains": "Not Contains",
                "starts_with": "Starts With",
                "ends_with": "Ends With",
                "greater_than": "Greater Than (>)",
                "less_than": "Less Than (<)",
                "greater_equal": "Greater or Equal (>=)",
                "less_equal": "Less or Equal (<=)"
            }
        ),
        has_in=True,
        info="The comparison operator"
    )

    value: any = NodeVariableSettings(
        label="Value",
        has_in=True,
        dock=True,
        info="The value to compare against"
    )

    filtered_data: list = NodeVariableSettings(
        label="Filtered Data",
        has_out=True,
        info="The filtered list of rows"
    )

    match_count: int = NodeVariableSettings(
        label="Match Count",
        has_out=True,
        info="Number of rows that matched the filter"
    )

    true_path: bool | list = PathSettings(
        label="Success",
        info="Returns the filtered data"
    )
    false_path: bool | dict = PathSettings(
        label="Error",
        info="Triggered if filtering fails"
    )

    def execute(self):
        try:
            if not isinstance(self.data, list):
                raise ValueError("Data must be a list")

            if not self.data:
                self.filtered_data = []
                self.match_count = 0
                self.true_path = []
                self.false_path = False
                return

            if not isinstance(self.data[0], dict):
                raise ValueError("Data must be a list of dicts (use CSV to List with headers)")

            if self.column not in self.data[0]:
                raise ValueError(f"Column '{self.column}' not found in data")

            # Filter based on operator
            filtered = []
            for row in self.data:
                row_value = row.get(self.column, "")

                match = False
                if self.operator == "equals":
                    match = str(row_value) == str(self.value)
                elif self.operator == "not_equals":
                    match = str(row_value) != str(self.value)
                elif self.operator == "contains":
                    match = str(self.value) in str(row_value)
                elif self.operator == "not_contains":
                    match = str(self.value) not in str(row_value)
                elif self.operator == "starts_with":
                    match = str(row_value).startswith(str(self.value))
                elif self.operator == "ends_with":
                    match = str(row_value).endswith(str(self.value))
                elif self.operator == "greater_than":
                    try:
                        match = float(row_value) > float(self.value)
                    except (ValueError, TypeError):
                        match = False
                elif self.operator == "less_than":
                    try:
                        match = float(row_value) < float(self.value)
                    except (ValueError, TypeError):
                        match = False
                elif self.operator == "greater_equal":
                    try:
                        match = float(row_value) >= float(self.value)
                    except (ValueError, TypeError):
                        match = False
                elif self.operator == "less_equal":
                    try:
                        match = float(row_value) <= float(self.value)
                    except (ValueError, TypeError):
                        match = False

                if match:
                    filtered.append(row)

            self.filtered_data = filtered
            self.match_count = len(filtered)
            self.true_path = filtered
            self.false_path = False

        except Exception as e:
            self.false_path = {"error": str(e)}
            self.true_path = False
            self.filtered_data = []
            self.match_count = 0
