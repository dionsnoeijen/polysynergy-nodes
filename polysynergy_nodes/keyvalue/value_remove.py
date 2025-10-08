import os

from polysynergy_node_runner.execution_context.replace_placeholders import replace_placeholders
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings
from polysynergy_nodes.keyvalue.services.client import DynamoDBClient


@node(
    name="KeyValue - Remove Value",
    category="persistent",
    icon="key.svg",
)
class KeyValueValueRemove(Node):
    key: str = NodeVariableSettings(
        has_in=True,
        dock=True,
        required=True,
        info="The key to remove (e.g. 'theme', 'username', 'last_login')"
    )

    true_path: bool | str = PathSettings(label="Removed", info="Key was successfully removed")
    false_path: bool | dict = PathSettings(label="Error", info="Key was not found or error occurred")

    def execute(self):
        db_client = DynamoDBClient()
        try:
            tenant_id = os.getenv('TENANT_ID')
            project_id = os.getenv('PROJECT_ID')

            if not tenant_id or not project_id:
                self.false_path = {
                    "error": "Missing tenant_id or project_id in environment"
                }
                return

            # Use fixed collection for simple key-value pairs
            collection = "simple"
            pk = f"{tenant_id}#{project_id}#{collection}"
            sk = self.key

            table = db_client.get_table()

            # First check if the item exists and belongs to this tenant/project
            response = table.get_item(
                Key={"PK": pk, "SK": sk},
                ProjectionExpression="PK, SK, tenant_id, project_id, #value",
                ExpressionAttributeNames={"#value": "Value"}
            )

            item = response.get("Item")

            if not item:
                self.false_path = {
                    "error": f"Key '{sk}' not found"
                }
                return

            # Security check - verify ownership
            if (item.get("tenant_id") != tenant_id or
                item.get("project_id") != project_id):
                self.false_path = {
                    "error": "Access denied - item belongs to different tenant/project"
                }
                return

            # Remove the item
            table.delete_item(Key={"PK": pk, "SK": sk})

            self.true_path = f"Removed key '{sk}'"

        except Exception as e:
            import traceback
            self.false_path = {
                "error": str(e),
                "details": traceback.format_exc()
            }