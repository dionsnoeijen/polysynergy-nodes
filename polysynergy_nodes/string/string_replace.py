from polysynergy_node_runner.setup_context.dock_property import dock_text_area
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="String Replace",
    category="string",
    icon='string.svg'
)
class StringReplace(Node):
    text: str = NodeVariableSettings(
        label="Text",
        dock=dock_text_area(),
        has_in=True,
        required=True
    )
    
    old: str = NodeVariableSettings(
        label="Find",
        dock=dock_text_area(),
        has_in=True,
        required=True
    )
    
    new: str = NodeVariableSettings(
        label="Replace With",
        dock=dock_text_area(),
        has_in=True,
        default=""
    )
    
    count: int = NodeVariableSettings(
        label="Max Replacements",
        info="Maximum number of replacements to make (-1 for all)",
        default=-1,
        has_in=True
    )

    true_path: str | bool = PathSettings(
        label="Result",
        info="The text with replacements made"
    )
    
    false_path: dict | bool = PathSettings(
        label="Error",
        info="Error information if inputs are invalid"
    )

    def execute(self):
        if not isinstance(self.text, str):
            self.false_path = NodeError.format(ValueError("Text must be a string"))
            self.true_path = False
            return
            
        if not isinstance(self.old, str):
            self.false_path = NodeError.format(ValueError("Find value must be a string"))
            self.true_path = False
            return
            
        if not isinstance(self.new, str):
            self.false_path = NodeError.format(ValueError("Replace value must be a string"))
            self.true_path = False
            return
            
        try:
            if self.count == -1:
                self.true_path = self.text.replace(self.old, self.new)
            else:
                self.true_path = self.text.replace(self.old, self.new, self.count)
        except Exception as e:
            self.false_path = NodeError.format(e)
            self.true_path = False