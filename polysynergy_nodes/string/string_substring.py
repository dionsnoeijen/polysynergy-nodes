from polysynergy_node_runner.setup_context.dock_property import dock_text_area
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="String Substring",
    category="string",
    icon='string.svg',
    version=1.0
)
class StringSubstring(Node):
    text: str = NodeVariableSettings(
        label="Text",
        dock=dock_text_area(),
        has_in=True,
        required=True
    )
    
    start: int = NodeVariableSettings(
        label="Start Index",
        has_in=True,
        default=0,
        info="Starting position (negative for from end)"
    )
    
    end: int | None = NodeVariableSettings(
        label="End Index",
        has_in=True,
        default=None,
        info="Ending position (None for end of string, negative for from end)"
    )

    true_path: str | bool = PathSettings(
        label="Substring",
        info="The extracted substring"
    )
    
    false_path: dict | bool = PathSettings(
        label="Error",
        info="Error information if extraction fails"
    )

    async def execute(self):
        if not isinstance(self.text, str):
            self.false_path = NodeError.format(ValueError("Text must be a string"))
            self.true_path = False
            return
            
        try:
            if self.end is None:
                self.true_path = self.text[self.start:]
            else:
                self.true_path = self.text[self.start:self.end]
            
            self.false_path = False
        except (IndexError, TypeError) as e:
            self.false_path = NodeError.format(e)
            self.true_path = False
        except Exception as e:
            self.false_path = NodeError.format(e)
            self.true_path = False