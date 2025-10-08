import os
import json

from boto3.dynamodb.conditions import Key
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings
from polysynergy_nodes.keyvalue.services.client import DynamoDBClient


@node(
    name="KeyValue - Get All Keys",
    category="persistent",
    icon="key.svg",
)
class KeyValueGetAllKeys(Node):
    collection: str = NodeVariableSettings(
        has_in=True,
        dock=True,
        required=True,
        info="The category/collection name to retrieve all keys from"
    )

    true_path: bool | str = PathSettings(label="Keys List", info="All keys from the collection as JSON array")
    false_path: bool | dict = PathSettings(label="Error", info="Error retrieving keys or collection is empty")

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

            # Query all items with this PK (collection), only get keys
            response = table.query(
                KeyConditionExpression=Key("PK").eq(pk),
                ProjectionExpression="SK, tenant_id, project_id"
            )

            items = response.get("Items", [])

            if not items:
                self.false_path = {
                    "error": f"Collection '{self.collection}' is empty or does not exist"
                }
                return

            # Build result list and verify security
            keys = []
            for item in items:
                # Security check - verify ownership
                if (item.get("tenant_id") == tenant_id and
                    item.get("project_id") == project_id):
                    keys.append(item["SK"])

            if keys:
                # Return as JSON array for list-like usage
                self.true_path = json.dumps(keys)
            else:
                self.false_path = {
                    "error": f"No accessible items found in collection '{self.collection}'"
                }

        except Exception as e:
            import traceback
            self.false_path = {
                "error": str(e),
                "details": traceback.format_exc()
            }