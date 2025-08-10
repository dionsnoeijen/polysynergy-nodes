from polysynergy_node_runner.setup_context.dock_property import dock_text_area
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="String Format",
    category="string",
    icon='string.svg',
    version=1.0
)
class StringFormat(Node):
    template: str = NodeVariableSettings(
        label="Template",
        dock=dock_text_area(),
        has_in=True,
        required=True,
        info="Template string with {} or {key} placeholders"
    )
    
    values: dict | list = NodeVariableSettings(
        label="Values",
        has_in=True,
        required=True,
        info="Dictionary for {key} or list for {} placeholders"
    )

    true_path: str | bool = PathSettings(
        label="Result",
        info="The formatted string"
    )
    
    false_path: dict | bool = PathSettings(
        label="Error",
        info="Error information if formatting fails"
    )

    async def execute(self):
        if not isinstance(self.template, str):
            self.false_path = NodeError.format(ValueError("Template must be a string"))
            self.true_path = False
            return
            
        try:
            if isinstance(self.values, dict):
                # Use dictionary for named placeholders
                self.true_path = self.template.format(**self.values)
            elif isinstance(self.values, list):
                # Use list for positional placeholders
                self.true_path = self.template.format(*self.values)
            else:
                self.false_path = NodeError.format(ValueError("Values must be a dictionary or list"))
                self.true_path = False
        except (KeyError, IndexError, ValueError) as e:
            self.false_path = NodeError.format(e)
            self.true_path = False
        except Exception as e:
            self.false_path = NodeError.format(e)
            self.true_path = False