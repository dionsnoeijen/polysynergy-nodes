import json
import markdown
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings
from polysynergy_node_runner.setup_context.dock_property import dock_layout_editor, dock_components
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.execution_context.replace_placeholders import replace_placeholders
from polysynergy_nodes.layout.utils.find_connected_components import find_connected_components


@node(
    name="Layout",
    category="layout",
    icon='layout.svg',
    version=1.0
)
class Layout(Node):
    """
    Visual layout builder for creating front-end pages.

    The layout editor produces a JSON structure that this node
    renders to HTML. Components are referenced by componentKey
    and connected via the components input.
    """

    layout: str = NodeVariableSettings(
        label="Layout",
        dock=dock_layout_editor(),
        has_in=True,
        required=True,
        default="",
        info="Layout JSON from the visual editor"
    )

    components: dict = NodeVariableSettings(
        label="Components",
        has_in=True,
        dock=dock_components(info="Add component handles and connect component nodes"),
        required=False,
        default={},
        info="Connected component nodes (tables, charts, forms)"
    )

    data: dict = NodeVariableSettings(
        label="Data",
        has_in=True,
        dock=True,
        required=False,
        default={},
        info="Additional data available for rendering"
    )

    true_path: str | bool = PathSettings(
        label="HTML Output",
        info="The rendered HTML page"
    )

    false_path: dict | bool = PathSettings(
        label="Error",
        info="Error information if rendering fails"
    )

    async def execute(self):
        try:
            # Parse layout JSON
            if isinstance(self.layout, str):
                layout_data = json.loads(self.layout)
            elif isinstance(self.layout, dict):
                layout_data = self.layout
            else:
                self.false_path = NodeError.format(ValueError("Layout must be a JSON string or dict"))
                self.true_path = False
                return

            # Find all connected components
            components = await find_connected_components(self)

            # Render the layout tree to HTML
            root = layout_data.get("root", layout_data)
            html = self._render_node(root, components)

            self.true_path = html
            self.false_path = False

        except json.JSONDecodeError as e:
            self.false_path = NodeError.format(ValueError(f"Invalid layout JSON: {e}"))
            self.true_path = False
        except Exception as e:
            self.false_path = NodeError.format(e, True)
            self.true_path = False

    def _render_node(self, node_data: dict, components: dict) -> str:
        """Recursively render a layout node to HTML."""
        if not node_data:
            return ""

        node_type = node_data.get("type", "block")
        styles = node_data.get("styles", {})
        children = node_data.get("children", [])
        content = node_data.get("content", {})

        # Build style string from styles dict
        style_str = self._build_style_string(styles)
        style_attr = f' style="{style_str}"' if style_str else ""

        # Render based on type
        if node_type == "block":
            children_html = "".join(self._render_node(child, components) for child in children)
            return f"<div{style_attr}>{children_html}</div>"

        elif node_type == "columns":
            children_html = "".join(self._render_node(child, components) for child in children)
            return f"<div{style_attr}>{children_html}</div>"

        elif node_type == "text":
            text_data = content.get("data", {})
            text = text_data.get("text", "")
            # Convert markdown to HTML
            html_content = markdown.markdown(text)
            return f"<div{style_attr}>{html_content}</div>"

        elif node_type == "component":
            component_data = content.get("data", {})
            component_key = component_data.get("componentKey", "")
            comp = components.get(component_key)
            if comp and hasattr(comp, "render"):
                component_html = comp.render()
                return f"<div{style_attr}>{component_html}</div>"
            return f"<div{style_attr}><!-- Component '{component_key}' not found --></div>"

        else:
            # Unknown type, render children anyway
            children_html = "".join(self._render_node(child, components) for child in children)
            return f"<div{style_attr}>{children_html}</div>"

    def _build_style_string(self, styles: dict) -> str:
        """Convert styles dict to CSS style string."""
        css_parts = []

        # Sizing
        sizing = styles.get("sizing", {})
        if sizing.get("width"):
            css_parts.append(f"width: {sizing['width']}")
        if sizing.get("minHeight"):
            css_parts.append(f"min-height: {sizing['minHeight']}px")
        if sizing.get("maxWidth"):
            css_parts.append(f"max-width: {sizing['maxWidth']}px")

        # Padding
        padding = styles.get("padding", {})
        if padding:
            top = padding.get("top", 0)
            right = padding.get("right", 0)
            bottom = padding.get("bottom", 0)
            left = padding.get("left", 0)
            if top or right or bottom or left:
                css_parts.append(f"padding: {top}px {right}px {bottom}px {left}px")

        # Margin
        margin = styles.get("margin", {})
        if margin:
            top = margin.get("top", 0)
            right = margin.get("right", 0)
            bottom = margin.get("bottom", 0)
            left = margin.get("left", 0)
            if top or right or bottom or left:
                css_parts.append(f"margin: {top}px {right}px {bottom}px {left}px")

        # Background
        background = styles.get("background", {})
        if background.get("color"):
            css_parts.append(f"background-color: {background['color']}")

        # Typography
        typography = styles.get("typography", {})
        if typography.get("fontSize"):
            css_parts.append(f"font-size: {typography['fontSize']}px")
        if typography.get("fontWeight"):
            css_parts.append(f"font-weight: {typography['fontWeight']}")
        if typography.get("color"):
            css_parts.append(f"color: {typography['color']}")

        # Display (for grid/flex)
        if styles.get("display"):
            css_parts.append(f"display: {styles['display']}")

        # Grid
        grid = styles.get("grid", {})
        if grid.get("columns"):
            css_parts.append(f"grid-template-columns: {grid['columns']}")
        if grid.get("gap") is not None:
            css_parts.append(f"gap: {grid['gap']}px")

        return "; ".join(css_parts)
