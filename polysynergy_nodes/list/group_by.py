from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="Group By",
    category="list",
    icon="list.svg",
    version=1.0
)
class GroupBy(Node):
    input_list: list = NodeVariableSettings(
        label="Input List",
        has_in=True,
        dock=True,
        info="List of dicts to group by a field"
    )

    field: str = NodeVariableSettings(
        label="Field",
        default="",
        dock=True,
        has_in=True,
        info="The field/key to group by"
    )

    grouped_dict: dict = NodeVariableSettings(
        label="Grouped Dict",
        has_out=True,
        info="Dictionary with field values as keys and lists of items as values"
    )

    group_count: int = NodeVariableSettings(
        label="Group Count",
        has_out=True,
        info="Number of distinct groups created"
    )

    original_length: int = NodeVariableSettings(
        label="Original Length",
        has_out=True,
        info="Total number of items in original list"
    )

    true_path: bool | dict = PathSettings(
        label="Grouped Data",
        info="Returns dictionary with grouped items"
    )
    false_path: bool | dict = PathSettings(
        label="Error",
        info="Triggered if grouping fails"
    )

    def execute(self):
        try:
            if not isinstance(self.input_list, list):
                raise ValueError("Input is not a list")

            if not self.field:
                raise ValueError("Field parameter is required for grouping")

            self.original_length = len(self.input_list)

            # Group items by field value
            grouped = {}
            for item in self.input_list:
                # Handle dicts
                if isinstance(item, dict):
                    group_key = item.get(self.field)
                else:
                    # For non-dict items, try to get attribute
                    group_key = getattr(item, self.field, None)

                # Convert group_key to string for consistent dict keys
                if group_key is None:
                    group_key_str = "None"
                else:
                    group_key_str = str(group_key)

                if group_key_str not in grouped:
                    grouped[group_key_str] = []

                grouped[group_key_str].append(item)

            self.grouped_dict = grouped
            self.group_count = len(grouped)
            self.true_path = grouped
            self.false_path = False

        except Exception as e:
            self.false_path = {"error": str(e)}
            self.true_path = False
            self.grouped_dict = {}
            self.group_count = 0
            self.original_length = 0
