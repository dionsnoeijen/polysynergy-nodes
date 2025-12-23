import json

from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.service_node import ServiceNode
from polysynergy_node_runner.setup_context.dock_property import dock_table_editor


@node(
    name="Table Component",
    category="layout",
    icon='layout.svg',
    version=1.0
)
class TableComponent(ServiceNode):
    """
    A table component for displaying tabular data in layouts.

    Connect this to a Layout node's components input.
    The table will render the provided data as an HTML table.

    Expects a Table object with 'columns' and 'rows' properties (from Variable Table node).
    """

    handle: str = NodeVariableSettings(
        label="Handle",
        dock=True,
        required=True,
        default="",
        info="Unique identifier used in template: {{ component('handle') }}"
    )

    table: str = NodeVariableSettings(
        label="Table",
        has_in=True,
        dock=dock_table_editor(info="Table object with 'columns' and 'rows'"),
        required=True,
        default="",
        in_type_override="table",
        info="Table object with 'columns' and 'rows' (from Variable Table node)"
    )

    css_class: str = NodeVariableSettings(
        label="CSS Class",
        dock=True,
        required=False,
        default="",
        info="CSS class(es) to apply to the table"
    )

    instance: "polysynergy_nodes.layout.component_node.ComponentNode" = NodeVariableSettings(
        info="Component instance for Layout node",
        has_out=True,
        type="polysynergy_nodes.layout.component_node.ComponentNode"
    )

    async def provide_instance(self) -> "TableComponent":
        return self

    def render(self) -> str:
        """Render the table to HTML."""
        # Parse table data - can be JSON string or dict
        table_data = self.table
        if isinstance(table_data, str):
            if not table_data.strip():
                return "<!-- Table: no data -->"
            try:
                table_data = json.loads(table_data)
            except json.JSONDecodeError:
                return "<!-- Table: invalid JSON -->"

        if not table_data or not isinstance(table_data, dict):
            return "<!-- Table: no data -->"

        table_columns = table_data.get('columns', [])
        table_rows = table_data.get('rows', [])

        if not table_columns:
            return "<!-- Table: no columns -->"

        # Build table HTML
        class_attr = f' class="{self.css_class}"' if self.css_class else ""

        # Header - use column labels
        header_cells = "".join(
            f"<th>{col.get('label', col.get('key', ''))}</th>"
            for col in table_columns
        )
        header = f"<thead><tr>{header_cells}</tr></thead>"

        # Body - use column keys to get row values
        rows_html = []
        for row in table_rows:
            if isinstance(row, dict):
                cells = "".join(
                    f"<td>{row.get(col.get('key', ''), '')}</td>"
                    for col in table_columns
                )
            else:
                cells = f"<td>{row}</td>"
            rows_html.append(f"<tr>{cells}</tr>")
        body = f"<tbody>{''.join(rows_html)}</tbody>"

        return f"<table{class_attr}>{header}{body}</table>"
