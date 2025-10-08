from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="Chat Window",
    category="mock",
    has_play_button=True,
    has_enabled_switch=False
)
class MockChatWindow(Node):
    # User identity (from auth/SSO) - for testing
    user_id: str = NodeVariableSettings(label="User ID", has_out=True, dock=True, default="test-user-123")
    user_email: str = NodeVariableSettings(label="User Email", has_out=True, dock=True, default="test@example.com")
    user_name: str = NodeVariableSettings(label="User Name", has_out=True, dock=True, default="Test")

    # Chat window permissions (from ChatWindowAccess) - for testing
    can_view_flow: bool = NodeVariableSettings(label="Can View Flow", has_out=True, dock=True, default=True)
    can_edit_flow: bool = NodeVariableSettings(label="Can Edit Flow", has_out=True, dock=True, default=False)
    can_view_output: bool = NodeVariableSettings(label="Can View Output", has_out=True, dock=True, default=True)
    show_response_transparency: bool = NodeVariableSettings(
        label="Show Response Transparency", has_out=True, dock=True, default=True
    )

    true_path: bool = PathSettings(default=True, label="Play")

    def execute(self):
        pass
