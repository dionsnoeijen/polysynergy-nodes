import csv
import io
from polysynergy_node_runner.setup_context.dock_property import dock_property
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="List to CSV",
    category="csv",
    icon="csv.svg",
    version=1.0
)
class ListToCsv(Node):
    data: list = NodeVariableSettings(
        label="Data",
        has_in=True,
        dock=True,
        info="List of dicts or list of lists to convert to CSV"
    )

    delimiter: str = NodeVariableSettings(
        label="Delimiter",
        default=",",
        dock=True,
        has_in=True,
        info="The delimiter character (default: comma)"
    )

    include_headers: bool = NodeVariableSettings(
        label="Include Headers",
        default=True,
        dock=True,
        has_in=True,
        info="Include column headers in output (only for dict lists)"
    )

    headers: list = NodeVariableSettings(
        label="Custom Headers",
        default=None,
        dock=True,
        has_in=True,
        info="Optional custom headers (for list of lists). If not provided, auto-detected from dict keys"
    )

    csv_string: str = NodeVariableSettings(
        label="CSV String",
        has_out=True,
        info="The resulting CSV data as string"
    )

    row_count: int = NodeVariableSettings(
        label="Row Count",
        has_out=True,
        info="Number of rows written (excluding headers)"
    )

    true_path: bool | str = PathSettings(
        label="Success",
        info="Returns the CSV string"
    )
    false_path: bool | dict = PathSettings(
        label="Error",
        info="Triggered if conversion fails"
    )

    def execute(self):
        try:
            if not isinstance(self.data, list):
                raise ValueError("Data must be a list")

            if not self.data:
                raise ValueError("Data list is empty")

            # Create a StringIO object to write CSV to string
            output = io.StringIO()

            # Check if data is list of dicts or list of lists
            if isinstance(self.data[0], dict):
                # List of dicts
                fieldnames = self.headers if self.headers else list(self.data[0].keys())
                writer = csv.DictWriter(output, fieldnames=fieldnames, delimiter=self.delimiter)

                if self.include_headers:
                    writer.writeheader()

                writer.writerows(self.data)

            elif isinstance(self.data[0], (list, tuple)):
                # List of lists/tuples
                writer = csv.writer(output, delimiter=self.delimiter)

                if self.include_headers and self.headers:
                    writer.writerow(self.headers)

                writer.writerows(self.data)

            else:
                raise ValueError("Data must be a list of dicts or list of lists")

            self.csv_string = output.getvalue()
            self.row_count = len(self.data)
            self.true_path = self.csv_string
            self.false_path = False

        except Exception as e:
            self.false_path = {"error": str(e)}
            self.true_path = False
            self.csv_string = ""
            self.row_count = 0
