from polysynergy_nodes.base.execution_context.flow_state import FlowState
from polysynergy_nodes.base.setup_context.dock_property import dock_dict, dock_text_area
from polysynergy_nodes.base.setup_context.node import Node
from polysynergy_nodes.base.setup_context.node_decorator import node
from polysynergy_nodes.base.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_nodes.base.setup_context.path_settings import PathSettings


@node(
    name='Tool',
    category='ai',
    icon='hammer.svg',
    has_enabled_switch=False,
    flow_state=FlowState.PENDING,
)
class AgentTool(Node):
    agent: str = NodeVariableSettings(
        label="Agent",
        has_in=True
    )

    instructions: str = NodeVariableSettings(
        label="Instructions",
        dock=dock_text_area()
    )

    arguments: dict = NodeVariableSettings(
        label="Arguments",
        dock=dock_dict(
            key_label="Argument name",
            value_label="Argument instructions",
            in_switch=False,
            out_switch_default=True
        ))

    true_path: bool = PathSettings(default=True, label="On Call")

    def execute(self):
        pass