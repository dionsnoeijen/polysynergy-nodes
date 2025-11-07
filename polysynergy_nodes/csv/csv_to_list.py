import csv
import io
from polysynergy_node_runner.setup_context.dock_property import dock_property
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="CSV to List",
    category="csv",
    icon="csv.svg",
    version=1.0
)
class CsvToList(Node):
    csv_string: str = NodeVariableSettings(
        label="CSV String",
        has_in=True,
        dock=True,
        info="The CSV data as a string"
    )

    delimiter: str = NodeVariableSettings(
        label="Delimiter",
        default=",",
        dock=True,
        has_in=True,
        info="The delimiter character (default: comma)"
    )

    has_headers: bool = NodeVariableSettings(
        label="Has Headers",
        default=True,
        dock=True,
        has_in=True,
        info="Whether the first row contains headers"
    )

    data: list = NodeVariableSettings(
        label="Data",
        has_out=True,
        info="Parsed CSV data as list of dicts (with headers) or list of lists (without headers)"
    )

    headers: list = NodeVariableSettings(
        label="Headers",
        has_out=True,
        info="Column headers (empty list if has_headers is False)"
    )

    row_count: int = NodeVariableSettings(
        label="Row Count",
        has_out=True,
        info="Number of data rows parsed"
    )

    true_path: bool | list = PathSettings(
        label="Success",
        info="Returns the parsed data"
    )
    false_path: bool | dict = PathSettings(
        label="Error",
        info="Triggered if parsing fails"
    )

    def execute(self):
        try:
            if not isinstance(self.csv_string, str):
                raise ValueError("CSV input must be a string")

            if not self.csv_string.strip():
                raise ValueError("CSV string is empty")

            # Create a StringIO object to read CSV from string
            csv_file = io.StringIO(self.csv_string)

            if self.has_headers:
                # Parse as dict with headers
                reader = csv.DictReader(csv_file, delimiter=self.delimiter)
                self.data = list(reader)
                self.headers = reader.fieldnames if reader.fieldnames else []
            else:
                # Parse as list of lists
                reader = csv.reader(csv_file, delimiter=self.delimiter)
                self.data = list(reader)
                self.headers = []

            self.row_count = len(self.data)
            self.true_path = self.data
            self.false_path = False

        except Exception as e:
            self.false_path = {"error": str(e)}
            self.true_path = False
            self.data = []
            self.headers = []
            self.row_count = 0
