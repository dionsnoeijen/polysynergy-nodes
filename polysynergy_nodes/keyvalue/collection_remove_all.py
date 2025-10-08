import os

from boto3.dynamodb.conditions import Key
from polysynergy_node_runner.execution_context.replace_placeholders import replace_placeholders
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings
from polysynergy_nodes.keyvalue.services.client import DynamoDBClient


@node(
    name="KeyValue - Clear Collection",
    category="persistent",
    icon="key.svg",
)
class KeyValueCollectionRemoveAll(Node):
    collection: str = NodeVariableSettings(
        has_in=True,
        dock=True,
        required=True,
        info="The category/collection name to completely clear"
    )

    true_path: bool | str = PathSettings(label="Removed All", info="All items in the collection were successfully removed")
    false_path: bool | dict = PathSettings(label="Error", info="Error removing collection or collection was already empty")

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

            # Use composite key pattern for security isolation
            pk = f"{tenant_id}#{project_id}#{self.collection}"

            table = db_client.get_table()

            # First query all items to verify ownership and get keys for deletion
            response = table.query(
                KeyConditionExpression=Key("PK").eq(pk),
                ProjectionExpression="PK, SK, tenant_id, project_id"
            )

            items = response.get("Items", [])

            if not items:
                self.false_path = {
                    "error": f"Collection '{self.collection}' is empty or does not exist"
                }
                return

            # Security check and collect keys for deletion
            keys_to_delete = []
            for item in items:
                # Verify ownership
                if (item.get("tenant_id") == tenant_id and
                    item.get("project_id") == project_id):
                    keys_to_delete.append({
                        "PK": item["PK"],
                        "SK": item["SK"]
                    })

            if not keys_to_delete:
                self.false_path = {
                    "error": f"No accessible items found in collection '{self.collection}'"
                }
                return

            # Delete items in batches (DynamoDB batch_writer handles batching automatically)
            with table.batch_writer() as batch:
                for key in keys_to_delete:
                    batch.delete_item(Key=key)

            self.true_path = f"Removed all {len(keys_to_delete)} items from collection '{self.collection}'"

        except Exception as e:
            import traceback
            self.false_path = {
                "error": str(e),
                "details": traceback.format_exc()
            }