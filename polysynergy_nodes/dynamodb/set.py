import os

from polysynergy_node_runner.setup_context.dock_property import dock_property
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings
from polysynergy_nodes.dynamodb.services.client import DynamoDBClient

@node(
    name="KeyValueStore - Set",
    category="persistent",
    icon="key.svg",
)
class KeyValueStoreSet(Node):
    key: str = NodeVariableSettings(has_in=True, dock=True, required=True)
    value: str = NodeVariableSettings(has_in=True, dock=dock_property(text_area=True), required=True)

    true_path: bool | str = PathSettings(label="Stored Value")
    false_path: bool | dict = PathSettings(label="Error")

    def execute(self):
        db_client = DynamoDBClient()
        try:
            tenant_id = os.getenv('TENANT_ID')
            project_id = os.getenv('PROJECT_ID')

            table = db_client.get_table()

            pk = f"{tenant_id}#{project_id}"
            sk = self.key

            table.put_item(Item={
                "PK": pk,
                "SK": sk,
                "Value": self.value
            })
            self.true_path = self.value

        except Exception as e:
            import traceback
            self.false_path = {
                "error": str(e),
                "details": traceback.format_exc()
            }