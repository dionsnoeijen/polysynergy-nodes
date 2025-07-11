import uuid

from polysynergy_nodes.base.setup_context.node import Node
from polysynergy_nodes.base.setup_context.node_decorator import node
from polysynergy_nodes.base.setup_context.node_error import NodeError
from polysynergy_nodes.base.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_nodes.base.setup_context.path_settings import PathSettings


@node(
    name="Deterministic UUID",
    category="uuid",
    icon="hash.svg",
)
class DeterministicUUID(Node):

    input_string: str = NodeVariableSettings(label="Input Text", has_in=True)
    namespace: str = NodeVariableSettings(label="Namespace (optional)", default="DNS", has_in=True)

    true_path: bool | str = PathSettings(label="UUID")
    false_path: bool | dict = PathSettings(label="Error")

    def execute(self):
        try:
            ns = {
                "DNS": uuid.NAMESPACE_DNS,
                "URL": uuid.NAMESPACE_URL,
                "OID": uuid.NAMESPACE_OID,
                "X500": uuid.NAMESPACE_X500
            }.get(self.namespace.upper(), uuid.NAMESPACE_DNS)

            self.true_path = str(uuid.uuid5(ns, self.input_string))
        except Exception as e:
            self.true_path = None
            self.false_path = NodeError.format(e)