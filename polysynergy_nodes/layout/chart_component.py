from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.dock_property import dock_select_values
from polysynergy_node_runner.setup_context.service_node import ServiceNode
import json


@node(
    name="Chart Component",
    category="layout",
    icon='layout.svg',
    version=1.0
)
class ChartComponent(ServiceNode):
    """
    A chart component for displaying data visualizations in layouts.

    Uses Chart.js for rendering. Connect to a Layout node's components input.
    """

    handle: str = NodeVariableSettings(
        label="Handle",
        dock=True,
        required=True,
        default="",
        info="Unique identifier used in template: {{ chart('handle') }}"
    )

    chart_type: str = NodeVariableSettings(
        label="Chart Type",
        dock=dock_select_values({
            "bar": "Bar Chart",
            "line": "Line Chart",
            "pie": "Pie Chart",
            "doughnut": "Doughnut Chart",
            "radar": "Radar Chart",
        }),
        required=True,
        default="bar",
        info="Type of chart to render"
    )

    labels: list = NodeVariableSettings(
        label="Labels",
        has_in=True,
        dock=True,
        required=False,
        default=[],
        info="Labels for the X-axis or segments"
    )

    data: list = NodeVariableSettings(
        label="Data",
        has_in=True,
        dock=True,
        required=False,
        default=[],
        info="Data values to display"
    )

    label: str = NodeVariableSettings(
        label="Dataset Label",
        dock=True,
        required=False,
        default="",
        info="Label for the dataset (shown in legend)"
    )

    width: str = NodeVariableSettings(
        label="Width",
        dock=True,
        required=False,
        default="400",
        info="Canvas width in pixels"
    )

    height: str = NodeVariableSettings(
        label="Height",
        dock=True,
        required=False,
        default="300",
        info="Canvas height in pixels"
    )

    css_class: str = NodeVariableSettings(
        label="CSS Class",
        dock=True,
        required=False,
        default="",
        info="CSS class(es) to apply to the container"
    )

    instance: "polysynergy_nodes.layout.component_node.ComponentNode" = NodeVariableSettings(
        info="Component instance for Layout node",
        has_out=True,
        type="polysynergy_nodes.layout.component_node.ComponentNode"
    )

    async def provide_instance(self) -> "ChartComponent":
        return self

    def render(self) -> str:
        """Render the chart to HTML with Chart.js."""
        canvas_id = f"chart-{self.handle}"
        class_attr = f' class="{self.css_class}"' if self.css_class else ""

        chart_config = {
            "type": self.chart_type,
            "data": {
                "labels": self.labels or [],
                "datasets": [{
                    "label": self.label or self.handle,
                    "data": self.data or [],
                    "borderWidth": 1
                }]
            },
            "options": {
                "responsive": False,
                "maintainAspectRatio": False
            }
        }

        config_json = json.dumps(chart_config)

        return f'''<div{class_attr}>
    <canvas id="{canvas_id}" width="{self.width}" height="{self.height}"></canvas>
    <script>
        (function() {{
            const ctx = document.getElementById('{canvas_id}').getContext('2d');
            new Chart(ctx, {config_json});
        }})();
    </script>
</div>'''
