import uuid
import hashlib

from polysynergy_node_runner.setup_context.dock_property import dock_select_values
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings

@node(
    name="UUID From String",
    category="uuid",
    icon="hash.svg",
    version=1.0
)
class UUIDFromString(Node):
    """
    Generate a UUID from any string using various methods.
    """
    
    input_string: str = NodeVariableSettings(
        label="Input String",
        has_in=True,
        required=True,
        info="String to convert to UUID"
    )
    
    method: str = NodeVariableSettings(
        label="Method",
        dock=dock_select_values({
            "md5": "MD5 Hash (UUID v3)",
            "sha1": "SHA-1 Hash (UUID v5)",
            "truncate": "Truncate/Pad to UUID format"
        }),
        default="sha1",
        has_in=True
    )
    
    namespace: str = NodeVariableSettings(
        label="Namespace (for v3/v5)",
        default="DNS",
        has_in=True,
        info="Namespace for UUID v3/v5 (DNS, URL, OID, X500)"
    )
    
    true_path: str | bool = PathSettings(
        label="UUID",
        info="Generated UUID from string"
    )
    
    false_path: dict | bool = PathSettings(
        label="Error",
        info="Error information if generation fails"
    )

    async def execute(self):
        if not isinstance(self.input_string, str):
            self.false_path = NodeError.format(ValueError("Input must be a string"))
            self.true_path = False
            return
            
        try:
            if self.method == "md5":
                # UUID v3 using MD5
                ns = {
                    "DNS": uuid.NAMESPACE_DNS,
                    "URL": uuid.NAMESPACE_URL,
                    "OID": uuid.NAMESPACE_OID,
                    "X500": uuid.NAMESPACE_X500
                }.get(self.namespace.upper(), uuid.NAMESPACE_DNS)
                
                self.true_path = str(uuid.uuid3(ns, self.input_string))
                
            elif self.method == "sha1":
                # UUID v5 using SHA-1
                ns = {
                    "DNS": uuid.NAMESPACE_DNS,
                    "URL": uuid.NAMESPACE_URL,
                    "OID": uuid.NAMESPACE_OID,
                    "X500": uuid.NAMESPACE_X500
                }.get(self.namespace.upper(), uuid.NAMESPACE_DNS)
                
                self.true_path = str(uuid.uuid5(ns, self.input_string))
                
            elif self.method == "truncate":
                # Create a UUID by hashing and formatting
                # This creates a consistent UUID-like string from any input
                hash_bytes = hashlib.md5(self.input_string.encode()).hexdigest()
                # Format as UUID (8-4-4-4-12)
                formatted = f"{hash_bytes[:8]}-{hash_bytes[8:12]}-{hash_bytes[12:16]}-{hash_bytes[16:20]}-{hash_bytes[20:32]}"
                self.true_path = formatted
                
            else:
                self.false_path = NodeError.format(ValueError(f"Invalid method: {self.method}"))
                self.true_path = False
                return
                
            self.false_path = False
            
        except Exception as e:
            self.true_path = False
            self.false_path = NodeError.format(e)