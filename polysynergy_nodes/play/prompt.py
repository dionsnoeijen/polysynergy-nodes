from polysynergy_node_runner.setup_context.dock_property import dock_text_area
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings


@node(
    name="Prompt",
    category="flow",
    has_enabled_switch=False,
    icon='play.svg'
)
class Prompt(Node):

    name: str = NodeVariableSettings(
        label="Name",
        dock=True,
        info="Name for this prompt node."
    )

    prompt: str = NodeVariableSettings(
        label="Prompt",
        dock=dock_text_area(rich=True),
        has_in=True,
        has_out=True,
        info="The prompt text to be used by agents or teams."
    )

    session: dict | None = NodeVariableSettings(
        label="Session",
        dock=True,
        has_in=True,
        info="Session data associated with this prompt."
    )

    user: list | None = NodeVariableSettings(
        label="User",
        dock=True,
        has_in=True,
        info="List of user IDs associated with this prompt."
    )

    active_session: str = NodeVariableSettings(
        label="Active Session",
        info="Currently selected session ID."
    )

    active_user: str = NodeVariableSettings(
        label="Active User",
        info="Currently selected user ID."
    )

    def execute(self):
        pass