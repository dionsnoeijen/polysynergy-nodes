import json
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(name="Dict to String", category="cast", icon="cast.svg")
class DictToString(Node):
    input_value: dict = NodeVariableSettings(label="Dictionary", dock=True, has_in=True)
    
    true_path: bool | str = PathSettings(label="JSON String", info="Successfully converted to JSON string")
    false_path: bool | dict = PathSettings(label="Error", info="JSON serialization failed")

    def execute(self):
        try:
            self.true_path = json.dumps(self.input_value, ensure_ascii=False)
        except TypeError as e:
            self.false_path = NodeError.format(f"Object not JSON serializable: {e}")
            self.true_path = False
        except Exception as e:
            self.false_path = NodeError.format(e)
            self.true_path = False