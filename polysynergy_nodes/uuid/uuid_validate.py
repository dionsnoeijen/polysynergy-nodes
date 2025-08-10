import uuid

from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings

@node(
    name="UUID Validate",
    category="uuid",
    icon="hash.svg",
    version=1.0
)
class UUIDValidate(Node):
    """
    Validate if a string is a valid UUID and optionally check its version.
    """
    
    uuid_string: str = NodeVariableSettings(
        label="UUID String",
        has_in=True,
        required=True,
        info="String to validate as UUID"
    )
    
    check_version: int = NodeVariableSettings(
        label="Check Version",
        has_in=True,
        default=0,
        info="Specific UUID version to check (0 for any version, 1-5 for specific)"
    )
    
    true_path: bool = PathSettings(
        label="Is Valid",
        info="True if valid UUID"
    )
    
    version: int = PathSettings(
        label="Version",
        info="UUID version (1-5) or 0 if invalid"
    )
    
    false_path: dict | bool = PathSettings(
        label="Error",
        info="Error information if validation fails"
    )

    async def execute(self):
        if not isinstance(self.uuid_string, str):
            self.false_path = NodeError.format(ValueError("UUID must be a string"))
            self.true_path = False
            self.version = 0
            return
            
        try:
            # Try to parse the UUID
            parsed_uuid = uuid.UUID(self.uuid_string)
            
            # Get the version
            self.version = parsed_uuid.version if parsed_uuid.version else 0
            
            # Check if it matches the requested version
            if self.check_version > 0:
                self.true_path = (self.version == self.check_version)
            else:
                self.true_path = True
                
            self.false_path = False
            
        except (ValueError, AttributeError) as e:
            # Not a valid UUID
            self.true_path = False
            self.version = 0
            self.false_path = False  # This is expected, not an error
        except Exception as e:
            self.true_path = False
            self.version = 0
            self.false_path = NodeError.format(e)