from jinja2 import Template, TemplateSyntaxError, UndefinedError
from polysynergy_node_runner.setup_context.dock_property import dock_code_editor
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


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
            # Create Jinja2 template
            jinja_template = Template(self.template)

            # Render with variables
            self.true_path = jinja_template.render(**self.variables)
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
