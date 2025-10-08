import os

from polysynergy_node_runner.execution_context.replace_placeholders import replace_placeholders
from polysynergy_node_runner.setup_context.dock_property import dock_property
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings
from polysynergy_nodes.keyvalue.services.client import DynamoDBClient


@node(
    name="KeyValue - Set Collection",
    category="persistent",
    icon="key.svg",
)
class KeyValueCollectionSet(Node):
    collection: str = NodeVariableSettings(
        has_in=True,
        dock=True,
        required=True,
        info="The category/collection name (e.g. 'google_drive_files', 'user_settings')"
    )
    key: str = NodeVariableSettings(
        has_in=True,
        dock=True,
        required=True,
        info="The unique key within this collection"
    )
    value: str = NodeVariableSettings(
        has_in=True,
        dock=dock_property(text_area=True),
        required=True,
        info="The value to store"
    )

    true_path: bool | str = PathSettings(label="Stored Value")
    false_path: bool | dict = PathSettings(label="Error")

    def execute(self):
        db_client = DynamoDBClient()
        try:
            # Replace placeholders in collection, key, and value
            processed_collection = replace_placeholders(
                data=self.collection,
                values={},
                state=self.state,
                current_node=self
            )

            processed_key = replace_placeholders(
                data=self.key,
                values={},
                state=self.state,
                current_node=self
            )

            processed_value = replace_placeholders(
                data=self.value,
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

            table = db_client.get_table()

            # Use composite key pattern: PK includes collection name for isolation
            pk = f"{tenant_id}#{project_id}#{processed_collection}"
            sk = processed_key

            table.put_item(Item={
                "PK": pk,
                "SK": sk,
                "Value": processed_value,
                "tenant_id": tenant_id,
                "project_id": project_id,
                "collection_name": processed_collection
            })

            self.true_path = processed_value

        except Exception as e:
            self.false_path = NodeError.format(e)