import json
import re
from typing import Any

from bson import ObjectId
from polysynergy_node_runner.setup_context.dock_property import dock_property, dock_code_editor
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings
from polysynergy_node_runner.setup_context.node_error import NodeError

from polysynergy_nodes.mongodb.mongodb_connection import MongoDBConnection
from polysynergy_nodes.mongodb.utils.find_connected_mongodb import find_connected_mongodb

# Regex for 24-character hex strings (MongoDB ObjectId format)
_OBJECTID_RE = re.compile(r'^[0-9a-fA-F]{24}$')

_OBJECTID_OPERATORS = {"$gt", "$gte", "$lt", "$lte", "$eq", "$ne", "$in", "$nin"}

def _convert_objectids(obj, parent_key=None):
    """Recursively convert 24-char hex strings in _id fields to ObjectId,
    and handle {\"$oid\": \"...\"} extended JSON syntax."""
    if isinstance(obj, dict):
        result = {}
        for key, value in obj.items():
            if isinstance(value, dict) and "$oid" in value:
                result[key] = ObjectId(value["$oid"])
            elif key == "_id" and isinstance(value, str) and _OBJECTID_RE.match(value):
                result[key] = ObjectId(value)
            elif key == "_id" and isinstance(value, dict):
                # Operators under _id: convert their values to ObjectId
                result[key] = _convert_objectids(value, parent_key="_id")
            elif parent_key == "_id" and key in _OBJECTID_OPERATORS:
                if isinstance(value, str) and _OBJECTID_RE.match(value):
                    result[key] = ObjectId(value)
                elif isinstance(value, list):
                    result[key] = [ObjectId(v) if isinstance(v, str) and _OBJECTID_RE.match(v) else v for v in value]
                else:
                    result[key] = value
            else:
                result[key] = _convert_objectids(value)
        return result
    elif isinstance(obj, list):
        return [_convert_objectids(item) for item in obj]
    return obj


_VALID_OPERATIONS = {
    "list_collections",
    "find",
    "aggregate",
    "insert_one",
    "insert_many",
    "update_one",
    "update_many",
    "delete_one",
    "delete_many",
    "count",
}


@node(
    name="MongoDB Query",
    category="mongodb",
    icon="mongodb.svg",
    version=1.0
)
class MongoDBQuery(Node):
    """
    Execute queries and operations against a MongoDB database.

    Connect a **MongoDB Connection** node to the *connection* input, then
    choose an operation and supply the required JSON parameters.

    **Supported operations:**
    - **find** – Query documents (uses query, projection, sort, limit)
    - **aggregate** – Run an aggregation pipeline (uses query as the pipeline array)
    - **insert_one** – Insert a single document (uses query as the document)
    - **insert_many** – Insert multiple documents (uses documents as a JSON array)
    - **update_one** – Update the first matching document (uses query as filter, update as the update doc)
    - **update_many** – Update all matching documents (uses query as filter, update as the update doc)
    - **delete_one** – Delete the first matching document (uses query as filter)
    - **delete_many** – Delete all matching documents (uses query as filter)
    - **count** – Count matching documents (uses query as filter)

    All JSON fields must contain valid JSON strings.
    """

    connection: MongoDBConnection | None = NodeVariableSettings(
        label="Connection",
        dock=True,
        has_in=True,
        required=True,
        info="MongoDB connection from a MongoDB Connection service node"
    )

    collection: str = NodeVariableSettings(
        label="Collection",
        dock=dock_property(placeholder="my_collection"),
        has_in=True,
        required=True,
        info="Name of the MongoDB collection to operate on"
    )

    operation: str = NodeVariableSettings(
        label="Operation",
        dock=dock_property(
            select_values={
                "list_collections": "List Collections",
                "find": "Find",
                "aggregate": "Aggregate",
                "insert_one": "Insert One",
                "insert_many": "Insert Many",
                "update_one": "Update One",
                "update_many": "Update Many",
                "delete_one": "Delete One",
                "delete_many": "Delete Many",
                "count": "Count",
            }
        ),
        has_in=True,
        default="find",
        info="MongoDB operation to perform"
    )

    query: str = NodeVariableSettings(
        label="Query / Filter / Document",
        dock=dock_code_editor(metadata={"language": "json"}),
        has_in=True,
        required=False,
        default="{}",
        info=(
            "JSON query filter for find/delete/count/update operations, "
            "aggregation pipeline array for aggregate, "
            "or document object for insert_one"
        )
    )

    projection: str = NodeVariableSettings(
        label="Projection",
        dock=dock_code_editor(metadata={"language": "json"}),
        has_in=True,
        required=False,
        default="{}",
        info="JSON projection document for find operations (fields to include/exclude)"
    )

    sort: str = NodeVariableSettings(
        label="Sort",
        dock=dock_code_editor(metadata={"language": "json"}),
        has_in=True,
        required=False,
        default="{}",
        info='JSON sort specification for find operations, e.g. {"field": 1} for ascending, {"field": -1} for descending'
    )

    limit: int = NodeVariableSettings(
        label="Limit",
        dock=True,
        has_in=True,
        required=False,
        default=0,
        info="Maximum number of documents to return (0 = no limit, applies to find only)"
    )

    update: str = NodeVariableSettings(
        label="Update Document",
        dock=dock_code_editor(metadata={"language": "json"}),
        has_in=True,
        required=False,
        default="{}",
        info="JSON update document for update_one/update_many operations, e.g. {\"$set\": {\"field\": \"value\"}}"
    )

    documents: str = NodeVariableSettings(
        label="Documents (JSON Array)",
        dock=dock_code_editor(metadata={"language": "json"}),
        has_in=True,
        required=False,
        default="[]",
        info="JSON array of documents for insert_many operations"
    )

    # Outputs
    result: list | dict = NodeVariableSettings(
        label="Result",
        has_out=True,
        info="Query results (list of documents for find/aggregate, dict for write operations)"
    )

    count: int = NodeVariableSettings(
        label="Count",
        has_out=True,
        info="Number of documents returned or affected by the operation"
    )

    true_path: list | dict = PathSettings(
        label="Success",
        info="Operation completed successfully"
    )

    false_path: dict = PathSettings(
        label="Error",
        info="Operation failed"
    )

    @staticmethod
    def _parse_json(value: str, field_name: str) -> Any:
        """Parse a JSON string, raising a descriptive error on failure.

        Args:
            value: JSON string to parse
            field_name: Name of the field (used in error messages)

        Returns:
            Parsed Python object
        """
        if not value or not value.strip():
            return {}
        try:
            return json.loads(value)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON in '{field_name}': {exc}") from exc

    @staticmethod
    def _sort_dict_to_list(sort_dict: dict) -> list:
        """Convert a sort dict like {"field": 1} to a list of (field, direction) tuples.

        pymongo's cursor.sort() expects a list of tuples, not a plain dict.

        Args:
            sort_dict: Dict mapping field names to sort direction (1 or -1)

        Returns:
            List of (field, direction) tuples
        """
        return list(sort_dict.items())

    async def execute(self):
        try:
            connection = await find_connected_mongodb(self, "connection")

            if not connection:
                raise ValueError(
                    "No MongoDB connection found. "
                    "Connect a MongoDB Connection node to the 'connection' input."
                )

            operation = (self.operation or "find").strip()

            if operation != "list_collections" and (not self.collection or not self.collection.strip()):
                raise ValueError("Collection name is required")
            if operation not in _VALID_OPERATIONS:
                raise ValueError(
                    f"Unknown operation '{operation}'. "
                    f"Valid operations: {', '.join(sorted(_VALID_OPERATIONS))}"
                )

            # Parse all JSON inputs upfront so errors surface early
            query_parsed = _convert_objectids(self._parse_json(self.query or "{}", "query"))
            projection_parsed = self._parse_json(self.projection or "{}", "projection")
            sort_parsed = self._parse_json(self.sort or "{}", "sort")
            update_parsed = _convert_objectids(self._parse_json(self.update or "{}", "update"))
            documents_parsed = _convert_objectids(self._parse_json(self.documents or "[]", "documents"))

            result: list | dict = []
            affected_count: int = 0

            if operation == "list_collections":
                result = await connection.list_collections()
                affected_count = len(result)

            elif operation == "find":
                sort_list = self._sort_dict_to_list(sort_parsed) if sort_parsed else None
                result = await connection.find(
                    collection=self.collection,
                    query=query_parsed,
                    projection=projection_parsed if projection_parsed else None,
                    limit=self.limit or 0,
                    sort=sort_list,
                )
                affected_count = len(result)

            elif operation == "aggregate":
                # For aggregate the query field holds the pipeline (must be a list)
                pipeline = query_parsed
                if not isinstance(pipeline, list):
                    raise ValueError(
                        "The 'query' field must contain a JSON array (pipeline) for the aggregate operation"
                    )
                result = await connection.aggregate(
                    collection=self.collection,
                    pipeline=pipeline,
                )
                affected_count = len(result)

            elif operation == "insert_one":
                result = await connection.insert_one(
                    collection=self.collection,
                    document=query_parsed,
                )
                affected_count = 1

            elif operation == "insert_many":
                docs = documents_parsed
                if not isinstance(docs, list):
                    raise ValueError(
                        "The 'documents' field must contain a JSON array for the insert_many operation"
                    )
                result = await connection.insert_many(
                    collection=self.collection,
                    documents=docs,
                )
                affected_count = result.get("inserted_count", 0)

            elif operation == "update_one":
                result = await connection.update_one(
                    collection=self.collection,
                    filter=query_parsed,
                    update=update_parsed,
                )
                affected_count = result.get("modified_count", 0)

            elif operation == "update_many":
                result = await connection.update_many(
                    collection=self.collection,
                    filter=query_parsed,
                    update=update_parsed,
                )
                affected_count = result.get("modified_count", 0)

            elif operation == "delete_one":
                result = await connection.delete_one(
                    collection=self.collection,
                    filter=query_parsed,
                )
                affected_count = result.get("deleted_count", 0)

            elif operation == "delete_many":
                result = await connection.delete_many(
                    collection=self.collection,
                    filter=query_parsed,
                )
                affected_count = result.get("deleted_count", 0)

            elif operation == "count":
                count_val = await connection.count_documents(
                    collection=self.collection,
                    filter=query_parsed,
                )
                result = {"count": count_val}
                affected_count = count_val

            self.result = result
            self.count = affected_count
            self.true_path = result
            self.false_path = False

        except Exception as e:
            self.false_path = NodeError.format(e)
            self.true_path = False
            self.result = []
            self.count = 0
