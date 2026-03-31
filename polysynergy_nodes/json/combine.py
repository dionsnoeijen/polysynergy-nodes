from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="Json Combine",
    category="json",
    icon="json.svg"
)
class JsonCombine(Node):
    combine: dict = NodeVariableSettings(label="Combine", has_in=True, dock=True)

    true_path: bool | dict = PathSettings(label="Combined")
    false_path: bool | dict = PathSettings(label="Error")

    async def execute(self):
        try:
            combined = {}
            for key, value in (self.combine or {}).items():
                if isinstance(value, dict):
                    combined.update(value)
                elif isinstance(value, list):
                    combined[key] = value
                else:
                    combined[key] = value

            self.true_path = combined

        except Exception as e:
            self.false_path = {"error": str(e)}
