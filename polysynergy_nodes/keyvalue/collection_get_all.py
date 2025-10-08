import os
import json

from boto3.dynamodb.conditions import Key
from polysynergy_node_runner.execution_context.replace_placeholders import replace_placeholders
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings
from polysynergy_nodes.keyvalue.services.client import DynamoDBClient


@node(
    name="KeyValue - Get All Collection",
    category="persistent",
    icon="key.svg",
)
class KeyValueCollectionGetAll(Node):
    collection: str = NodeVariableSettings(
        has_in=True,
        dock=True,
        required=True,
        info="The category/collection name to retrieve all items from"
    )

    true_path: bool | str = PathSettings(label="Collection Data", info="All items from the collection as JSON")
    false_path: bool | dict = PathSettings(label="Error", info="Error retrieving collection or collection is empty")

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

            # Query all items with this PK (collection)
            response = table.query(
                KeyConditionExpression=Key("PK").eq(pk),
                ProjectionExpression="SK, #value, tenant_id, project_id",
                ExpressionAttributeNames={"#value": "Value"}
            )

            items = response.get("Items", [])

            if not items:
                self.false_path = {
                    "error": f"Collection '{self.collection}' is empty or does not exist"
                }
                return

            # Build result dictionary and verify security
            result = {}
            for item in items:
                # Security check - verify ownership
                if (item.get("tenant_id") == tenant_id and
                    item.get("project_id") == project_id):
                    result[item["SK"]] = item.get("Value", "")

            if result:
                # Return as JSON string for compatibility with other nodes
                self.true_path = json.dumps(result, indent=2)
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