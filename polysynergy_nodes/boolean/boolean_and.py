from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="Boolean AND",
    category="boolean",
    icon='boolean.svg'
)
class BooleanAnd(Node):
    a: bool = NodeVariableSettings(
        label="Value A",
        has_in=True,
        required=True
    )
    
    b: bool = NodeVariableSettings(
        label="Value B",
        has_in=True,
        required=True
    )

    true_path: bool = PathSettings(
        label="Result",
        info="True if both A and B are true"
    )
    
    false_path: dict | bool = PathSettings(
        label="Error",
        info="Error information if inputs are invalid"
    )

    def execute(self):
        try:
            # Convert inputs to boolean values
            bool_a = bool(self.a)
            bool_b = bool(self.b)
            
            self.true_path = bool_a and bool_b
        except Exception as e:
            self.false_path = NodeError.format(e)
            self.true_path = False