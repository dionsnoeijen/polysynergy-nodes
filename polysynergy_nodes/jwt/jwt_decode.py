import json
import base64

from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(name="JWT Decode", category="auth")
class JWTDecode(Node):
    """
    Decode a JWT token without signature verification.

    Extracts the header and payload from a JWT string.
    Does NOT verify the signature - use this for reading claims only.
    """

    token: str = NodeVariableSettings(
        label="Token",
        dock=True,
        has_in=True,
        required=True,
        info="JWT token string to decode"
    )

    header: dict = NodeVariableSettings(
        label="Header",
        has_out=True,
        info="Decoded JWT header (algorithm, type, etc.)"
    )

    payload: dict = NodeVariableSettings(
        label="Payload",
        has_out=True,
        info="Decoded JWT payload (claims: sub, iat, exp, etc.)"
    )

    true_path: dict = PathSettings(label="Payload", info="Decoded payload on success")
    false_path: dict = PathSettings(label="Error", info="Error details on failure")

    @staticmethod
    def _decode_part(part: str) -> dict:
        """Decode a base64url-encoded JWT part to a dict."""
        # Add padding if needed
        padding = 4 - len(part) % 4
        if padding != 4:
            part += "=" * padding
        decoded = base64.urlsafe_b64decode(part)
        return json.loads(decoded)

    def execute(self):
        try:
            token = (self.token or "").strip()
            if not token:
                raise ValueError("Token is empty")

            parts = token.split(".")
            if len(parts) != 3:
                raise ValueError(f"Invalid JWT: expected 3 parts separated by dots, got {len(parts)}")

            self.header = self._decode_part(parts[0])
            self.payload = self._decode_part(parts[1])

            self.true_path = self.payload
            self.false_path = False
        except Exception as e:
            self.header = {}
            self.payload = {}
            self.false_path = {"error": str(e)}
            self.true_path = False
