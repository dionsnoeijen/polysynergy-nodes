from polysynergy_node_runner.setup_context.dock_property import dock_text_area
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="String Contains",
    category="string",
    icon='string.svg',
    version=1.0
)
class StringContains(Node):
    text: str = NodeVariableSettings(
        label="Text",
        dock=dock_text_area(),
        has_in=True,
        required=True
    )
    
    search: str = NodeVariableSettings(
        label="Search For",
        dock=dock_text_area(),
        has_in=True,
        required=True
    )
    
    case_sensitive: bool = NodeVariableSettings(
        label="Case Sensitive",
        default=True,
        has_in=True
    )

    true_path: bool = PathSettings(
        label="Contains",
        info="True if text contains the search string"
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
            
        if not isinstance(self.search, str):
            self.false_path = NodeError.format(ValueError("Search value must be a string"))
            self.true_path = False
            return
            
        if self.case_sensitive:
            self.true_path = self.search in self.text
        else:
            self.true_path = self.search.lower() in self.text.lower()