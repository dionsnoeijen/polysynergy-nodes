import json
import csv
from io import StringIO
import traceback

from polysynergy_node_runner.setup_context.dock_property import dock_table_editor
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="Variable Table",
    category="variable",
    icon='table.svg',
    version=1.0
)
class VariableTable(Node):
    """
    Define and manage tabular data.

    Accepts CSV, JSON array, or Table object as input.
    Outputs a structured Table object with columns and rows.

    Example Table structure:
    {
        "columns": [
            {"key": "name", "label": "Name", "type": "string", "sortable": true},
            {"key": "age", "label": "Age", "type": "number", "sortable": true}
        ],
        "rows": [
            {"name": "John", "age": 30},
            {"name": "Jane", "age": 25}
        ]
    }
    """

    value: str = NodeVariableSettings(
        label="Table Data",
        dock=dock_table_editor(info="Define table columns and data"),
        has_in=True,
        default="",
        info="Table data (JSON Table object, JSON array, or CSV)"
    )

    true_path: dict | bool | "table" = PathSettings(
        label="Table",
        info="The Table object with columns and rows"
    )

    false_path: dict | bool = PathSettings(
        label="Error",
        info="Error if parsing fails"
    )

    async def execute(self):
        try:
            table = self._parse_input(self.value)
            self.true_path = table
            self.false_path = False
        except Exception as e:
            self.false_path = {
                'error': str(e),
                'traceback': traceback.format_exc(),
                'value_input': self.value,
                'node': self.handle,
                'node_type': self.path
            }
            self.true_path = False

    def _parse_input(self, value) -> dict:
        """Parse CSV, JSON array, or Table object."""
        # Already a Table object
        if isinstance(value, dict) and 'columns' in value and 'rows' in value:
            return value

        if isinstance(value, str):
            if not value.strip():
                return {"columns": [], "rows": []}

            # Try JSON first
            try:
                parsed = json.loads(value)
                if isinstance(parsed, list):
                    return self._list_to_table(parsed)
                if isinstance(parsed, dict) and 'columns' in parsed and 'rows' in parsed:
                    return parsed
                if isinstance(parsed, dict):
                    # Single dict - make it a single-row table
                    return self._list_to_table([parsed])
            except json.JSONDecodeError:
                pass

            # Try CSV
            if ',' in value or '\n' in value:
                return self._csv_to_table(value)

            raise ValueError(f"Cannot parse input as table: {type(value).__name__}")

        if isinstance(value, list):
            return self._list_to_table(value)

        raise ValueError(f"Cannot parse input as table: {type(value).__name__}")

    def _list_to_table(self, data: list) -> dict:
        """Convert list of dicts to Table object."""
        if not data:
            return {"columns": [], "rows": []}

        # Auto-detect columns from first row
        first_row = data[0]
        if not isinstance(first_row, dict):
            raise ValueError("List items must be dictionaries")

        columns = []
        for k, v in first_row.items():
            columns.append({
                "key": k,
                "label": k.replace('_', ' ').title(),
                "type": self._detect_type(v),
                "sortable": True,
                "filterable": True
            })

        return {"columns": columns, "rows": data}

    def _csv_to_table(self, csv_str: str) -> dict:
        """Parse CSV string to Table object."""
        reader = csv.DictReader(StringIO(csv_str))
        rows = list(reader)

        if not rows:
            return {"columns": [], "rows": []}

        columns = []
        for k in rows[0].keys():
            columns.append({
                "key": k,
                "label": k.replace('_', ' ').title(),
                "type": "string",
                "sortable": True,
                "filterable": True
            })

        return {"columns": columns, "rows": rows}

    def _detect_type(self, value) -> str:
        if isinstance(value, bool):
            return "boolean"
        if isinstance(value, (int, float)):
            return "number"
        return "string"
