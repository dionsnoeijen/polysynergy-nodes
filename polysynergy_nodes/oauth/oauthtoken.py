import requests
import time
import os
import boto3

from polysynergy_nodes.base.setup_context.node import Node
from polysynergy_nodes.base.setup_context.node_decorator import node
from polysynergy_nodes.base.setup_context.node_variable_settings import NodeVariableSettings

dynamodb = boto3.resource(
    "dynamodb",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION", "eu-central-1"),
)
table = dynamodb.Table("OAuthTokens")

@node(name="OAuth 2.0 Token", category="auth")
class OAuthToken(Node):
    service_name: str = NodeVariableSettings(label="Service Name", dock=True, has_in=True, has_out=True)
    client_id: str = NodeVariableSettings(label="Client ID", dock=True, has_in=True, has_out=True)
    client_secret: str = NodeVariableSettings(label="Client Secret", dock=True, has_in=True, has_out=True)
    token_url: str = NodeVariableSettings(label="Token URL", dock=True, has_in=True, has_out=True)

    access_token: str = NodeVariableSettings(label="Access Token", dock=True, has_out=True)

    _refresh_token: str | None = None
    _expires_at: float | None = None

    true_path: bool = False
    false_path: bool = False

    def get_token_from_dynamodb(self):
        response = table.get_item(Key={"service_name": self.service_name})
        return response.get("Item", {})

    def save_token_to_dynamodb(self):
        table.put_item(Item={
            "service_name": self.service_name,
            "access_token": self.access_token,
            "refresh_token": self._refresh_token,
            "expires_at": self._expires_at
        })

    def execute(self):
        token_data = self.get_token_from_dynamodb()

        self.access_token = token_data.get("access_token")
        self._refresh_token = token_data.get("refresh_token")
        self._expires_at = token_data.get("expires_at")

        if self.access_token and self._expires_at and self._expires_at > time.time():
            return self

        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "refresh_token",
            "refresh_token": self._refresh_token
        }

        response = requests.post(self.token_url, data=data)
        if response.status_code == 200:
            new_token = response.json()
            self.access_token = new_token["access_token"]
            self._expires_at = time.time() + new_token["expires_in"]

            self.save_token_to_dynamodb()

            self.true_path = True
        else:
            self.false_path = True
            self._exception = Exception(f"Failed to refresh token: {response.text}")
            return response.text

        return self.access_token