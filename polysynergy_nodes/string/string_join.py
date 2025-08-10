from polysynergy_node_runner.setup_context.dock_property import dock_text_area
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="String Join",
    category="string",
    icon='string.svg',
    version=1.0
)
class StringJoin(Node):
    items: list = NodeVariableSettings(
        label="Items",
        info="List of items to join",
        has_in=True,
        required=True
    )
    
    separator: str = NodeVariableSettings(
        label="Separator",
        info="String to join with",
        dock=dock_text_area(),
        has_in=True,
        default=""
    )

    true_path: str | bool = PathSettings(
        label="Result",
        info="The joined string"
    )
    
    false_path: dict | bool = PathSettings(
        label="Error",
        info="Error information if inputs are invalid"
    )

    async def execute(self):
        if not isinstance(self.items, list):
            self.false_path = NodeError.format(ValueError("Items must be a list"))
            self.true_path = False
            return
            
        if not isinstance(self.separator, str):
            self.false_path = NodeError.format(ValueError("Separator must be a string"))
            self.true_path = False
            return
            
        try:
            # Convert all items to strings
            string_items = [str(item) for item in self.items]
            self.true_path = self.separator.join(string_items)
        except Exception as e:
            self.false_path = NodeError.format(e)
            self.true_path = False