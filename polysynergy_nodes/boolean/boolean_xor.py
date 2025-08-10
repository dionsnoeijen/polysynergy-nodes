from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings
from polysynergy_node_runner.setup_context.node_error import NodeError

@node(name="Boolean XOR", category="boolean", version=1.0)
class BooleanXor(Node):
    a: bool = NodeVariableSettings(label="A", dock=True, has_in=True, has_out=False)
    b: bool = NodeVariableSettings(label="B", dock=True, has_in=True, has_out=False)
    
    true_path: bool = PathSettings(label="Result", info="True if A and B are different")
    false_path: bool = PathSettings(label="Error", info="Error or false result")

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
            bool_b = self.coerce_to_bool(self.b)
            
            result = bool_a != bool_b  # XOR is true when values differ
            
            if result:
                self.true_path = True
                self.false_path = False
            else:
                self.true_path = False
                self.false_path = False
                
        except Exception as e:
            self.true_path = False
            self.false_path = NodeError.format(str(e))