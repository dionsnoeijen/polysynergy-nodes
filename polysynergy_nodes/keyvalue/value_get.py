import os

from polysynergy_node_runner.execution_context.replace_placeholders import replace_placeholders
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings
from polysynergy_nodes.keyvalue.services.client import DynamoDBClient


@node(
    name="KeyValue - Get Value",
    category="persistent",
    icon="key.svg",
)
class KeyValueValueGet(Node):
    key: str = NodeVariableSettings(
        has_in=True,
        dock=True,
        required=True,
        info="The key to retrieve (e.g. 'theme', 'username', 'last_login')"
    )

    true_path: bool | str = PathSettings(label="Value", info="The value retrieved from storage")
    false_path: bool | dict = PathSettings(label="Error", info="The error message if the key does not exist")

    def execute(self):
        db_client = DynamoDBClient()
        try:
            # Replace placeholders in key
            processed_key = replace_placeholders(
                data=self.key,
                values={},
                state=self.state,
                current_node=self
            )

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
            sk = processed_key

            table = db_client.get_table()
            response = table.get_item(Key={"PK": pk, "SK": sk})

            item = response.get("Item")

            if item:
                # Security check - verify tenant/project ownership
                if (item.get("tenant_id") != tenant_id or
                    item.get("project_id") != project_id):
                    self.false_path = {
                        "error": "Access denied - item belongs to different tenant/project"
                    }
                    self.true_path = False
                    return

                value = item.get("Value")
                if value is not None:
                    self.true_path = value
                    self.false_path = False
                    print(f"GET SUCCESS: key={sk}, value={value}, true_path={self.true_path}, false_path={self.false_path}")
                else:
                    self.false_path = {
                        "error": f"Key '{sk}' found but has no value"
                    }
                    self.true_path = False
            else:
                self.false_path = {
                    "error": f"Key '{sk}' not found"
                }
                self.true_path = False
                print(f"GET FAIL: key={sk} not found, true_path={self.true_path}, false_path={self.false_path}")

        except Exception as e:
            self.false_path = NodeError.format(e)
            self.true_path = False