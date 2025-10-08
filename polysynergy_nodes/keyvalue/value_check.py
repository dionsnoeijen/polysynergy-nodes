import os

from polysynergy_node_runner.execution_context.replace_placeholders import replace_placeholders
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings
from polysynergy_nodes.keyvalue.services.client import DynamoDBClient


@node(
    name="KeyValue - Check Value",
    category="persistent",
    icon="key.svg",
)
class KeyValueValueCheck(Node):
    key: str = NodeVariableSettings(
        has_in=True,
        dock=True,
        required=True,
        info="The key to check for (e.g. 'theme', 'username', 'last_login')"
    )

    true_path: bool = PathSettings(label="Found", info="Key exists in storage")
    false_path: bool = PathSettings(label="Not Found", info="Key does not exist in storage")

    def execute(self):
        db_client = DynamoDBClient()
        try:
            tenant_id = os.getenv('TENANT_ID')
            project_id = os.getenv('PROJECT_ID')

            if not tenant_id or not project_id:
                self.false_path = False
                return

            # Replace placeholders in key
            processed_key = replace_placeholders(
                data=self.key,
                values={},
                state=self.state,
                current_node=self
            )

            # Use fixed collection for simple key-value pairs
            collection = "simple"
            pk = f"{tenant_id}#{project_id}#{collection}"
            sk = processed_key

            table = db_client.get_table()
            response = table.get_item(
                Key={"PK": pk, "SK": sk},
                ProjectionExpression="PK, SK, tenant_id, project_id"
            )

            item = response.get("Item")

            if item:
                # Security check - verify tenant/project ownership
                if (item.get("tenant_id") == tenant_id and
                    item.get("project_id") == project_id):
                    self.true_path = True
                else:
                    self.false_path = False
            else:
                self.false_path = False

        except Exception as e:
            # On any error, return false rather than exposing error details
            self.false_path = False