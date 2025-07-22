from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="Loop End",
    category="flow"
)
class LoopEnd(Node):

    to: str = NodeVariableSettings(dock=True)

    true_path: bool | list | str | int | float | dict = PathSettings(label="Pass Result", info="When the loop is done, it will pass the result of the node connected to this one")

    def execute(self):
        connections = self.get_driving_connections()

        sources = []
        for connection in connections:
            source_node = self.state.get_node_by_id(connection.source_node_id)
            if hasattr(source_node, "true_path"):
                sources.append(source_node)

        if not sources:
            self.true_path = True
            return

        if len(sources) == 1:
            self.true_path = sources[0].true_path
            return

        self.true_path = []
        for source in sources:
            self.true_path.append(source.true_path)

