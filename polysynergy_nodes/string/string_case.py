from polysynergy_node_runner.setup_context.dock_property import dock_text_area, dock_select
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="String Case",
    category="string",
    icon='string.svg'
)
class StringCase(Node):
    text: str = NodeVariableSettings(
        label="Text",
        dock=dock_text_area(),
        has_in=True,
        required=True
    )
    
    case_type: str = NodeVariableSettings(
        label="Case Type",
        dock=dock_select(options=[
            {"value": "upper", "label": "UPPERCASE"},
            {"value": "lower", "label": "lowercase"},
            {"value": "title", "label": "Title Case"},
            {"value": "capitalize", "label": "Capitalize First"}
        ]),
        default="lower",
        has_in=True
    )

    true_path: str | bool = PathSettings(
        label="Result",
        info="The text with case changed"
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
            
        try:
            if self.case_type == "upper":
                self.true_path = self.text.upper()
            elif self.case_type == "lower":
                self.true_path = self.text.lower()
            elif self.case_type == "title":
                self.true_path = self.text.title()
            elif self.case_type == "capitalize":
                self.true_path = self.text.capitalize()
            else:
                self.false_path = NodeError.format(ValueError(f"Invalid case type: {self.case_type}"))
                self.true_path = False
        except Exception as e:
            self.false_path = NodeError.format(e)
            self.true_path = False