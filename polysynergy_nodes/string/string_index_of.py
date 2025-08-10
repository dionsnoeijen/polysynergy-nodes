from polysynergy_node_runner.setup_context.dock_property import dock_text_area
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="String Index Of",
    category="string",
    icon='string.svg',
    version=1.0
)
class StringIndexOf(Node):
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
    
    start: int = NodeVariableSettings(
        label="Start Position",
        has_in=True,
        default=0,
        info="Position to start searching from"
    )
    
    find_last: bool = NodeVariableSettings(
        label="Find Last",
        has_in=True,
        default=False,
        info="Find last occurrence instead of first"
    )

    true_path: int = PathSettings(
        label="Index",
        info="Position of substring (-1 if not found)"
    )
    
    false_path: dict | bool = PathSettings(
        label="Error",
        info="Error information if search fails"
    )

    async def execute(self):
        if not isinstance(self.text, str):
            self.false_path = NodeError.format(ValueError("Text must be a string"))
            self.true_path = -1
            return
            
        if not isinstance(self.search, str):
            self.false_path = NodeError.format(ValueError("Search value must be a string"))
            self.true_path = -1
            return
            
        try:
            if self.find_last:
                # Find last occurrence
                if self.start > 0:
                    self.true_path = self.text.rfind(self.search, self.start)
                else:
                    self.true_path = self.text.rfind(self.search)
            else:
                # Find first occurrence
                self.true_path = self.text.find(self.search, self.start)
            
            self.false_path = False
        except Exception as e:
            self.false_path = NodeError.format(e)
            self.true_path = -1