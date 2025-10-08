from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(name="ChatWindow", category="hidden")
class ChatWindow(Node):
    # User identity (from auth/SSO)
    user_id: str = NodeVariableSettings(label="User ID", has_out=True)
    user_email: str = NodeVariableSettings(label="User Email", has_out=True)
    user_name: str = NodeVariableSettings(label="User Name", has_out=True)

    # Chat window permissions (from ChatWindowAccess)
    can_view_flow: bool = NodeVariableSettings(label="Can View Flow", has_out=True)
    can_edit_flow: bool = NodeVariableSettings(label="Can Edit Flow", has_out=True)
    can_view_output: bool = NodeVariableSettings(label="Can View Output", has_out=True)
    show_response_transparency: bool = NodeVariableSettings(
        label="Show Response Transparency", has_out=True
    )

    true_path: bool = PathSettings(default=True, label="Flow")

    def execute(self):
        pass
