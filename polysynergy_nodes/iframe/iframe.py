from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.dock_property import dock_iframe_viewer, dock_property


@node(
    name="Iframe",
    category="utility",
    icon='iframe.svg',
    version=1.0,
    has_enabled_switch=False
)
class Iframe(Node):
    """
    Display an external URL in an iframe.

    Use this node to preview websites, SPAs, or any web content
    directly in the editor. The iframe is displayed on the node itself.
    Use the zoom level to fit wide websites in the node viewport.
    """

    url: str = NodeVariableSettings(
        label="URL",
        dock=dock_iframe_viewer(info="Enter a URL to display in the iframe"),
        default="",
        info="The URL to display in the iframe"
    )

    zoom: float = NodeVariableSettings(
        label="Zoom",
        dock=dock_property(info="Zoom level for the iframe content (0.25 - 2.0)"),
        default=1.0,
        node=False,
        info="Zoom level for the iframe content"
    )

    async def execute(self):
        # This node is purely visual - no execution needed
        pass
