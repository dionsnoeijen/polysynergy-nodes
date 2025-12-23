from jinja2 import TemplateSyntaxError, UndefinedError
from polysynergy_node_runner.setup_context.dock_property import dock_code_editor, dock_components
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings
from polysynergy_node_runner.execution_context.replace_placeholders import replace_placeholders
from polysynergy_nodes.layout.utils.find_connected_components import find_connected_components


@node(
    name="String Template",
    category="string",
    icon='string.svg',
    version=1.0
)
class StringTemplate(Node):
    """
    Render a Jinja2 template with variables.

    Perfect for generating HTML, emails, or any formatted text with dynamic content.

    Example template:
    ```html
    <div class="card">
      <h2>{{ title }}</h2>
      <img src="{{ image_url }}" alt="{{ title }}" />
      <p>{{ description }}</p>
    </div>
    ```

    Variables dict:
    ```json
    {
      "title": "My Card",
      "image_url": "https://example.com/image.jpg",
      "description": "This is a description"
    }
    ```
    """

    template: str = NodeVariableSettings(
        label="Template",
        dock=dock_code_editor(metadata={"language": "html"}),
        has_in=True,
        required=True,
        default="",
        info="Jinja2 template string (supports {{ variable }}, {% if %}, {% for %}, etc.)"
    )

    variables: dict = NodeVariableSettings(
        label="Variables",
        has_in=True,
        dock=True,
        required=False,
        default={},
        info="Dictionary of variables to render in the template"
    )

    components: dict = NodeVariableSettings(
        label="Components",
        has_in=True,
        dock=dock_components(info="Add component handles and connect component nodes"),
        required=False,
        default={},
        info="Connected component nodes (tables, charts, forms) - use {{ component('key') }}"
    )

    true_path: str | bool = PathSettings(
        label="Result",
        info="The rendered template"
    )

    false_path: dict | bool = PathSettings(
        label="Error",
        info="Error information if rendering fails"
    )

    async def execute(self):
        if not isinstance(self.template, str):
            self.false_path = NodeError.format(ValueError("Template must be a string"))
            self.true_path = False
            return

        # If variables is None, empty list, or not provided, use empty dict
        if self.variables is None or self.variables == [] or self.variables == "":
            self.variables = {}
        elif not isinstance(self.variables, dict):
            print(f"[StringTemplate] ERROR: variables is type {type(self.variables)}, value: {self.variables}")
            self.false_path = NodeError.format(ValueError(f"Variables must be a dictionary, got {type(self.variables).__name__}"))
            self.true_path = False
            return

        try:
            # Find all connected components for component() function
            components = await find_connected_components(self)

            # Get state and executable node for backwards traversal
            state = self._state if hasattr(self, '_state') else None
            current_node = self._executable_node if hasattr(self, '_executable_node') else None

            # Render template with replace_placeholders which provides:
            # - backwards traversal for node handles
            # - component() function for rendering connected components
            # - flow() function (stub for now)
            self.true_path = replace_placeholders(
                self.template,
                values=self.variables,
                state=state,
                current_node=current_node,
                components=components
            )
            self.false_path = False

        except TemplateSyntaxError as e:
            self.false_path = NodeError.format(
                ValueError(f"Template syntax error at line {e.lineno}: {e.message}")
            )
            self.true_path = False

        except UndefinedError as e:
            self.false_path = NodeError.format(
                ValueError(f"Undefined variable in template: {str(e)}")
            )
            self.true_path = False

        except Exception as e:
            self.false_path = NodeError.format(e, True)
            self.true_path = False
