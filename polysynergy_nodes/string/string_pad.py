from polysynergy_node_runner.setup_context.dock_property import dock_text_area, dock_select_values
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="String Pad",
    category="string",
    icon='string.svg',
    version=1.0
)
class StringPad(Node):
    text: str = NodeVariableSettings(
        label="Text",
        dock=dock_text_area(),
        has_in=True,
        required=True
    )
    
    width: int = NodeVariableSettings(
        label="Width",
        has_in=True,
        required=True,
        info="Total width of the padded string"
    )
    
    fill_char: str = NodeVariableSettings(
        label="Fill Character",
        has_in=True,
        default=" ",
        info="Character to use for padding (default: space)"
    )
    
    pad_type: str = NodeVariableSettings(
        label="Pad Type",
        dock=dock_select_values({
            "left": "Left (rjust)",
            "right": "Right (ljust)",
            "center": "Center"
        }),
        default="left",
        has_in=True
    )

    true_path: str | bool = PathSettings(
        label="Result",
        info="The padded string"
    )
    
    false_path: dict | bool = PathSettings(
        label="Error",
        info="Error information if padding fails"
    )

    async def execute(self):
        if not isinstance(self.text, str):
            self.false_path = NodeError.format(ValueError("Text must be a string"))
            self.true_path = False
            return
            
        if not isinstance(self.fill_char, str) or len(self.fill_char) != 1:
            self.false_path = NodeError.format(ValueError("Fill character must be a single character"))
            self.true_path = False
            return
            
        try:
            if self.pad_type == "left":
                self.true_path = self.text.rjust(self.width, self.fill_char)
            elif self.pad_type == "right":
                self.true_path = self.text.ljust(self.width, self.fill_char)
            elif self.pad_type == "center":
                self.true_path = self.text.center(self.width, self.fill_char)
            else:
                self.false_path = NodeError.format(ValueError(f"Invalid pad type: {self.pad_type}"))
                self.true_path = False
                return
            
            self.false_path = False
        except Exception as e:
            self.false_path = NodeError.format(e)
            self.true_path = False