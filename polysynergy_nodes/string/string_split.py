from polysynergy_node_runner.setup_context.dock_property import dock_text_area
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="String Split",
    category="string",
    icon='string.svg'
)
class StringSplit(Node):
    text: str = NodeVariableSettings(
        label="Text",
        dock=dock_text_area(),
        has_in=True,
        required=True
    )
    
    separator: str = NodeVariableSettings(
        label="Separator",
        info="String to split on (default: whitespace)",
        has_in=True,
        default=" "
    )
    
    max_split: int = NodeVariableSettings(
        label="Max Splits",
        info="Maximum number of splits to make (-1 for unlimited)",
        default=-1,
        has_in=True
    )

    true_path: list | bool = PathSettings(
        label="Result",
        info="List of split strings"
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
            
        if not isinstance(self.separator, str):
            self.false_path = NodeError.format(ValueError("Separator must be a string"))
            self.true_path = False
            return
            
        try:
            if self.max_split == -1:
                self.true_path = self.text.split(self.separator)
            else:
                self.true_path = self.text.split(self.separator, self.max_split)
        except Exception as e:
            self.false_path = NodeError.format(e)
            self.true_path = False