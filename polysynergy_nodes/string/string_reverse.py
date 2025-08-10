from polysynergy_node_runner.setup_context.dock_property import dock_text_area
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="String Reverse",
    category="string",
    icon='string.svg',
    version=1.0
)
class StringReverse(Node):
    text: str = NodeVariableSettings(
        label="Text",
        dock=dock_text_area(),
        has_in=True,
        required=True
    )

    true_path: str | bool = PathSettings(
        label="Result",
        info="The reversed string"
    )
    
    false_path: dict | bool = PathSettings(
        label="Error",
        info="Error information if reversal fails"
    )

    async def execute(self):
        if not isinstance(self.text, str):
            self.false_path = NodeError.format(ValueError("Text must be a string"))
            self.true_path = False
            return
            
        try:
            self.true_path = self.text[::-1]
            self.false_path = False
        except Exception as e:
            self.false_path = NodeError.format(e)
            self.true_path = False