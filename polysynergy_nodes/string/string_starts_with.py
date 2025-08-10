from polysynergy_node_runner.setup_context.dock_property import dock_text_area
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="String Starts With",
    category="string",
    icon='string.svg',
    version=1.0
)
class StringStartsWith(Node):
    text: str = NodeVariableSettings(
        label="Text",
        dock=dock_text_area(),
        has_in=True,
        required=True
    )
    
    prefix: str = NodeVariableSettings(
        label="Prefix",
        dock=dock_text_area(),
        has_in=True,
        required=True,
        info="String to check at the beginning"
    )
    
    case_sensitive: bool = NodeVariableSettings(
        label="Case Sensitive",
        default=True,
        has_in=True
    )

    true_path: bool = PathSettings(
        label="Starts With",
        info="True if text starts with prefix"
    )
    
    false_path: dict | bool = PathSettings(
        label="Error",
        info="Error information if inputs are invalid"
    )

    async def execute(self):
        if not isinstance(self.text, str):
            self.false_path = NodeError.format(ValueError("Text must be a string"))
            self.true_path = False
            return
            
        if not isinstance(self.prefix, str):
            self.false_path = NodeError.format(ValueError("Prefix must be a string"))
            self.true_path = False
            return
            
        try:
            if self.case_sensitive:
                self.true_path = self.text.startswith(self.prefix)
            else:
                self.true_path = self.text.lower().startswith(self.prefix.lower())
            
            self.false_path = False
        except Exception as e:
            self.false_path = NodeError.format(e)
            self.true_path = False