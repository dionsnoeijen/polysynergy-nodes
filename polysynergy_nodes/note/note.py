from polysynergy_node_runner.setup_context.dock_property import dock_property
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings


@node(name="Note", category="note", has_enabled_switch=False)
class Note(Node):
    note: str = NodeVariableSettings(dock=dock_property(rich_text_area=True))
