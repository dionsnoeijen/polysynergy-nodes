from polysynergy_nodes.base.setup_context.dock_property import dock_text_area
from polysynergy_nodes.base.setup_context.node import Node
from polysynergy_nodes.base.setup_context.node_decorator import node
from polysynergy_nodes.base.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_nodes.base.setup_context.path_settings import PathSettings


@node(
    name="Play",
    category="flow",
    has_play_button=True,
    has_enabled_switch=False,
    icon='play.svg'
)
class Play(Node):

    title: str = NodeVariableSettings(label="Title", dock=True)

    info: str = NodeVariableSettings(label="Info", dock=dock_text_area(rich=True))

    true_path: bool = PathSettings(default=True, label="Play")

    def execute(self):
        pass