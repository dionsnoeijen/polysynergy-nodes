import time
from polysynergy_nodes import jwt
import requests
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings

@node(name="JWT Generator", category="auth")
class JWTGenerator(Node):
    jwt_claims: dict = NodeVariableSettings(
        label="JWT Claims",
        dock=True,
        has_in=True,
        info="Claims used in the JWT payload. Must include 'iss' and 'aud'. Optional: 'sub', 'scope', etc."
    )
    exchange_config: dict = NodeVariableSettings(
        label="Exchange Config",
        dock=True,
        has_in=True,
        info="Required keys: 'private_key', 'token_uri'. Optional: 'grant_type' (default: 'urn:ietf:params:oauth:grant-type:jwt-bearer')"
    )
    access_token: str | None = NodeVariableSettings(label="Access Token", has_out=True)
    expires_at: int | None = NodeVariableSettings(label="Expires At", has_out=True)

    true_path: bool | str = PathSettings(label="Access Token", info="The generated access token")
    false_path: bool | dict = PathSettings(label="Error", info="The error message if the token generation fails")

    def execute(self):
        try:
            if not self.jwt_claims or not isinstance(self.jwt_claims, dict):
                raise ValueError("Invalid or missing JWT claims")
            if not self.exchange_config or not isinstance(self.exchange_config, dict):
                raise ValueError("Invalid or missing exchange config")

            private_key = self.exchange_config.get("private_key")
            token_uri = self.exchange_config.get("token_uri")
            grant_type = self.exchange_config.get("grant_type", "urn:ietf:params:oauth:grant-type:jwt-bearer")
            exp_time = self.jwt_claims.get("exp_time", 3600)

            if not private_key or not token_uri:
                raise ValueError("Missing required exchange config: 'private_key' or 'token_uri'")

            now = int(time.time())
            payload = {
                **self.jwt_claims,
                "iat": now,
                "exp": now + exp_time,
            }

            signed_jwt = jwt.encode(payload, private_key, algorithm="RS256")

            token_request = {
                "grant_type": grant_type,
                "assertion": signed_jwt,
            }

            response = requests.post(token_uri, data=token_request)
            if response.status_code != 200:
                raise ValueError(f"Token exchange failed: {response.status_code} - {response.text}")

            token_data = response.json()
            self.access_token = token_data.get("access_token")
            self.expires_at = now + token_data.get("expires_in", exp_time)

            if not self.access_token:
                raise ValueError("Token exchange did not return an access_token")

            self.true_path = self.access_token
        except Exception as e:
            self.false_path = {"error": str(e)}
