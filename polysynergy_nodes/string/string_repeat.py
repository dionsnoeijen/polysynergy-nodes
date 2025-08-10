from polysynergy_node_runner.setup_context.dock_property import dock_text_area
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="String Repeat",
    category="string",
    icon='string.svg',
    version=1.0
)
class StringRepeat(Node):
    text: str = NodeVariableSettings(
        label="Text",
        dock=dock_text_area(),
        has_in=True,
        required=True
    )
    
    count: int = NodeVariableSettings(
        label="Count",
        has_in=True,
        required=True,
        default=1,
        info="Number of times to repeat"
    )
    
    separator: str = NodeVariableSettings(
        label="Separator",
        dock=dock_text_area(),
        has_in=True,
        default="",
        info="String to insert between repetitions"
    )

    true_path: str | bool = PathSettings(
        label="Result",
        info="The repeated string"
    )
    
    false_path: dict | bool = PathSettings(
        label="Error",
        info="Error information if repeat fails"
    )

    async def execute(self):
        if not isinstance(self.text, str):
            self.false_path = NodeError.format(ValueError("Text must be a string"))
            self.true_path = False
            return
            
        if not isinstance(self.count, int) or self.count < 0:
            self.false_path = NodeError.format(ValueError("Count must be a non-negative integer"))
            self.true_path = False
            return
            
        if not isinstance(self.separator, str):
            self.false_path = NodeError.format(ValueError("Separator must be a string"))
            self.true_path = False
            return
            
        try:
            if self.count == 0:
                self.true_path = ""
            elif self.separator:
                # Use separator between repetitions
                self.true_path = self.separator.join([self.text] * self.count)
            else:
                # Simple repetition without separator
                self.true_path = self.text * self.count
            
            self.false_path = False
        except Exception as e:
            self.false_path = NodeError.format(e)
            self.true_path = False