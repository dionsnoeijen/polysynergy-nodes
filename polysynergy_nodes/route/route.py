from http import HTTPMethod
from polysynergy_nodes.base.setup_context.node import Node
from polysynergy_nodes.base.setup_context.node_decorator import node
from polysynergy_nodes.base.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_nodes.base.setup_context.path_settings import PathSettings


@node(name="Route", category="hidden")
class Route(Node):
    method: str = NodeVariableSettings(
        label="Method",
        default=HTTPMethod.GET,
        has_out=True
    )
    headers: dict[str, str] = NodeVariableSettings(label="Headers", has_out=True)
    body: bytes|str = NodeVariableSettings(label="Body", has_out=True)
    query: dict[str, str] = NodeVariableSettings(label="Query", has_out=True)
    cookies: dict[str, str] = NodeVariableSettings(label="Cookies", has_out=True)
    route_variables: dict[str, str] = NodeVariableSettings(label="Route Variables", has_out=True)

    true_path: bool = PathSettings(default=True, label="Flow")

    def execute(self):
        pass
