from http import HTTPMethod
from polysynergy_nodes.base.setup_context.dock_property import dock_property, dock_json
from polysynergy_nodes.base.setup_context.node import Node
from polysynergy_nodes.base.setup_context.node_decorator import node
from polysynergy_nodes.base.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_nodes.base.setup_context.path_settings import PathSettings


@node(
    name="Route",
    category="mock",
    has_play_button=True,
    has_enabled_switch=False
)
class MockRouteRequest(Node):
    url: str = NodeVariableSettings(label="URL", has_out=True, dock=True)
    method: str = NodeVariableSettings(
        label="Method",
        default=HTTPMethod.GET,
        dock=dock_property(select_values={method.upper(): method.upper() for method in HTTPMethod}),
        has_out=True
    )
    headers: dict[str, str] = NodeVariableSettings(has_out=True, dock=True)
    body: str = NodeVariableSettings(label="Request Body", has_out=True, dock=dock_json())
    query: dict[str, str] = NodeVariableSettings(has_out=True, dock=True)
    cookies: dict[str, str] = NodeVariableSettings(has_out=True, dock=True)
    route_variables: dict[str, str] = NodeVariableSettings(label="Route Variables", dock=True, has_out=True)

    true_path: bool = PathSettings(default=True, label="Play")

    def execute(self):
        pass

