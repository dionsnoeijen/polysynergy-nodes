import uuid

from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="Deterministic UUID",
    category="uuid",
    icon="hash.svg",
    version=1.0
)
class DeterministicUUID(Node):

    input_string: str = NodeVariableSettings(
        label="Input Text", 
        has_in=True,
        required=True,
        info="String to generate UUID from"
    )
    namespace: str = NodeVariableSettings(
        label="Namespace", 
        default="DNS", 
        has_in=True,
        info="Namespace for UUID v5 (DNS, URL, OID, X500)"
    )

    true_path: str | bool = PathSettings(label="UUID", info="Deterministic UUID v5")
    false_path: dict | bool = PathSettings(label="Error", info="Error information if generation fails")

    async def execute(self):
        if not isinstance(self.input_string, str):
            self.false_path = NodeError.format(ValueError("Input must be a string"))
            self.true_path = False
            return
            
        try:
            ns = {
                "DNS": uuid.NAMESPACE_DNS,
                "URL": uuid.NAMESPACE_URL,
                "OID": uuid.NAMESPACE_OID,
                "X500": uuid.NAMESPACE_X500
            }.get(self.namespace.upper(), uuid.NAMESPACE_DNS)

            self.true_path = str(uuid.uuid5(ns, self.input_string))
            self.false_path = False
        except Exception as e:
            self.true_path = False
            self.false_path = NodeError.format(e)