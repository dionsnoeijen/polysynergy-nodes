from polysynergy_node_runner.setup_context.dock_property import dock_property
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="CSV Select Columns",
    category="csv",
    icon="csv.svg",
    version=1.0
)
class CsvSelectColumns(Node):
    data: list = NodeVariableSettings(
        label="Data",
        has_in=True,
        dock=True,
        info="List of dicts (CSV data with headers)"
    )

    columns: list = NodeVariableSettings(
        label="Columns",
        has_in=True,
        dock=True,
        info="List of column names to select (e.g., ['name', 'email'])"
    )

    ignore_missing: bool = NodeVariableSettings(
        label="Ignore Missing Columns",
        default=True,
        dock=True,
        has_in=True,
        info="If True, skip columns that don't exist. If False, raise error for missing columns"
    )

    selected_data: list = NodeVariableSettings(
        label="Selected Data",
        has_out=True,
        info="The data with only selected columns"
    )

    selected_columns: list = NodeVariableSettings(
        label="Selected Columns",
        has_out=True,
        info="List of columns that were actually selected"
    )

    row_count: int = NodeVariableSettings(
        label="Row Count",
        has_out=True,
        info="Number of rows in the result"
    )

    true_path: bool | list = PathSettings(
        label="Success",
        info="Returns the data with selected columns"
    )
    false_path: bool | dict = PathSettings(
        label="Error",
        info="Triggered if selection fails"
    )

    def execute(self):
        try:
            if not isinstance(self.data, list):
                raise ValueError("Data must be a list")

            if not self.data:
                self.selected_data = []
                self.selected_columns = []
                self.row_count = 0
                self.true_path = []
                self.false_path = False
                return

            if not isinstance(self.data[0], dict):
                raise ValueError("Data must be a list of dicts (use CSV to List with headers)")

            if not isinstance(self.columns, list):
                raise ValueError("Columns must be a list of column names")

            if not self.columns:
                raise ValueError("Columns list is empty")

            # Get available columns from first row
            available_columns = set(self.data[0].keys())

            # Validate columns
            selected_cols = []
            for col in self.columns:
                if col in available_columns:
                    selected_cols.append(col)
                elif not self.ignore_missing:
                    raise ValueError(f"Column '{col}' not found in data. Available columns: {', '.join(available_columns)}")

            if not selected_cols:
                raise ValueError("No valid columns selected")

            # Select only specified columns from each row
            result = []
            for row in self.data:
                selected_row = {col: row.get(col, "") for col in selected_cols}
                result.append(selected_row)

            self.selected_data = result
            self.selected_columns = selected_cols
            self.row_count = len(result)
            self.true_path = result
            self.false_path = False

        except Exception as e:
            self.false_path = {"error": str(e)}
            self.true_path = False
            self.selected_data = []
            self.selected_columns = []
            self.row_count = 0
