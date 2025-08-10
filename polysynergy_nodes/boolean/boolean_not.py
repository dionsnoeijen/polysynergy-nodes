from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings
from polysynergy_node_runner.setup_context.node_error import NodeError

@node(name="Boolean NOT", category="boolean", version=1.0)
class BooleanNot(Node):
    a: bool = NodeVariableSettings(label="A", dock=True, has_in=True, has_out=False)
    
    true_path: bool = PathSettings(label="Result", info="True if A is false")
    false_path: bool = PathSettings(label="Error", info="Error information")

    def coerce_to_bool(self, value):
        """Convert value to boolean following common conventions."""
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower().strip() not in ('', 'false', '0', 'null', 'none', 'undefined')
        if isinstance(value, (int, float)):
            return value != 0
        if value is None:
            return False
        return bool(value)

    async def execute(self):
        try:
            bool_a = self.coerce_to_bool(self.a)
            
            result = not bool_a
            
            if result:
                self.true_path = True
                self.false_path = False
            else:
                self.true_path = False
                self.false_path = False
                
        except Exception as e:
            self.true_path = False
            self.false_path = NodeError.format(str(e))