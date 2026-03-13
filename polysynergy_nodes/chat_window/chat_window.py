from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(name="ChatWindow", category="hidden")
class ChatWindow(Node):
    session_id: str = NodeVariableSettings(label="Session ID", has_out=True)
    user_id: str = NodeVariableSettings(label="User ID", has_out=True)
    data: dict = NodeVariableSettings(label="Data", has_out=True)

    true_path: bool = PathSettings(default=True, label="Flow")

    def execute(self):
        pass
