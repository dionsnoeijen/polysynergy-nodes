import json
from polysynergy_node_runner.setup_context.dock_property import dock_property
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="CSV to JSON",
    category="csv",
    icon="csv.svg",
    version=1.0
)
class CsvToJson(Node):
    data: list = NodeVariableSettings(
        label="Data",
        has_in=True,
        dock=True,
        info="List of dicts (CSV data with headers)"
    )

    indent: int = NodeVariableSettings(
        label="Indent",
        default=2,
        dock=True,
        has_in=True,
        info="Number of spaces for indentation (0 for compact JSON)"
    )

    json_string: str = NodeVariableSettings(
        label="JSON String",
        has_out=True,
        info="The resulting JSON string"
    )

    json_object: list = NodeVariableSettings(
        label="JSON Object",
        has_out=True,
        info="The data as Python object (for further processing)"
    )

    row_count: int = NodeVariableSettings(
        label="Row Count",
        has_out=True,
        info="Number of rows converted"
    )

    true_path: bool | str = PathSettings(
        label="Success",
        info="Returns the JSON string"
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
                self.json_string = "[]"
                self.json_object = []
                self.row_count = 0
                self.true_path = "[]"
                self.false_path = False
                return

            # Convert to JSON string
            indent_value = self.indent if self.indent > 0 else None
            self.json_string = json.dumps(self.data, indent=indent_value, ensure_ascii=False)
            self.json_object = self.data
            self.row_count = len(self.data)
            self.true_path = self.json_string
            self.false_path = False

        except Exception as e:
            self.false_path = {"error": str(e)}
            self.true_path = False
            self.json_string = ""
            self.json_object = []
            self.row_count = 0
