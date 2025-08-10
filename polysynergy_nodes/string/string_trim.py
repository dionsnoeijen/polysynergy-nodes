from polysynergy_node_runner.setup_context.dock_property import dock_text_area
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="String Trim",
    category="string",
    icon='string.svg',
    version=1.0
)
class StringTrim(Node):
    text: str = NodeVariableSettings(
        label="Text",
        dock=dock_text_area(),
        has_in=True,
        required=True
    )
    
    characters: str = NodeVariableSettings(
        label="Characters to Trim",
        info="Characters to remove from start and end (default: whitespace)",
        has_in=True,
        default=""
    )

    true_path: str | bool = PathSettings(
        label="Result",
        info="The trimmed string"
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
            
        try:
            if self.characters == "":
                # Default whitespace trimming
                self.true_path = self.text.strip()
            else:
                # Trim specific characters
                self.true_path = self.text.strip(self.characters)
        except Exception as e:
            self.false_path = NodeError.format(e)
            self.true_path = False