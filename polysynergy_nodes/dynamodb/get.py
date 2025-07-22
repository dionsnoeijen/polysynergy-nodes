import os

from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings
from polysynergy_nodes.dynamodb.services.client import DynamoDBClient


@node(
    name="KeyValueStore - Get",
    category="persistent",
    icon="key.svg",
)
class KeyValueStoreGet(Node):
    key: str = NodeVariableSettings(has_in=True, dock=True, required=True)

    true_path: bool | str = PathSettings(label="Result", info="The value retrieved from the key-value store")
    false_path: bool | dict = PathSettings(label="Error", info="The error message if the key does not exist or if there is an error retrieving the value")

    def execute(self):
        db_client = DynamoDBClient()

        try:
            tenant_id = os.getenv('TENANT_ID')
            project_id = os.getenv('PROJECT_ID')

            pk = f"{tenant_id}#{project_id}"
            sk = self.key

            table = db_client.get_table()
            response = table.get_item(Key={"PK": pk, "SK": sk})

            item = response.get("Item")
            value = item.get("Value") if item else None

            if value is not None:
                self.true_path = value
            else:
                self.false_path = {"error": f"Key '{sk}' not found or has no value."}

        except Exception as e:
            import traceback
            self.false_path = {
                "error": str(e),
                "details": traceback.format_exc()
            }