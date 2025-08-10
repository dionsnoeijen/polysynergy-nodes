from polysynergy_node_runner.setup_context.dock_property import dock_text_area
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="String Length",
    category="string",
    icon='string.svg',
    version=1.0
)
class StringLength(Node):
    text: str = NodeVariableSettings(
        label="Text",
        dock=dock_text_area(),
        has_in=True,
        required=True
    )

    true_path: int | bool = PathSettings(
        label="Length",
        info="The length of the string"
    )
    
    false_path: dict | bool = PathSettings(
        label="Error",
        info="Error information if input is invalid"
    )

    async def execute(self):
        if not isinstance(self.text, str):
            self.false_path = NodeError.format(ValueError("Input must be a string"))
            self.true_path = False
            return
            
        self.true_path = len(self.text)