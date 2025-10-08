import os

from polysynergy_node_runner.execution_context.replace_placeholders import replace_placeholders
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings
from polysynergy_nodes.keyvalue.services.client import DynamoDBClient


@node(
    name="KeyValue - Check Collection",
    category="persistent",
    icon="key.svg",
)
class KeyValueCollectionCheck(Node):

    collection: str = NodeVariableSettings(
        has_in=True,
        dock=True,
        required=True,
        info="The category/collection name to check in"
    )

    key: str = NodeVariableSettings(
        has_in=True,
        dock=True,
        required=True,
        info="The key to check for"
    )

    true_path: bool = PathSettings(label="Found", info="Item exists in the collection")
    false_path: bool = PathSettings(label="Not Found", info="Item does not exist in the collection or there was an error")

    def execute(self):
        db_client = DynamoDBClient()
        try:
            tenant_id = os.getenv('TENANT_ID')
            project_id = os.getenv('PROJECT_ID')

            if not tenant_id or not project_id:
                self.false_path = False
                return

            # Use composite key pattern for security isolation
            pk = f"{tenant_id}#{project_id}#{self.collection}"
            sk = self.key

            table = db_client.get_table()
            response = table.get_item(
                Key={"PK": pk, "SK": sk},
                ProjectionExpression="PK, SK, tenant_id, project_id"  # Only get what we need for efficiency
            )

            item = response.get("Item")

            if item:
                # Additional security check - verify tenant/project ownership
                if (item.get("tenant_id") == tenant_id and
                    item.get("project_id") == project_id):
                    self.true_path = True
                else:
                    # Exists but belongs to different tenant/project
                    self.false_path = False
            else:
                self.false_path = False

        except Exception as e:
            # On any error, return false rather than exposing error details
            # This prevents information leakage about other tenants' data
            self.false_path = False