from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="Join List to String",
    category="list",
    icon="list.svg",
    version=1.0
)
class JoinList(Node):
    input_list: list = NodeVariableSettings(
        label="Input List",
        has_in=True,
        dock=True,
        info="The list to join into a string"
    )

    separator: str = NodeVariableSettings(
        label="Separator",
        default=", ",
        dock=True,
        has_in=True,
        info="String to insert between items (e.g., ', ', '\\n', ';')"
    )

    field: str = NodeVariableSettings(
        label="Field",
        default="",
        dock=True,
        has_in=True,
        info="If list contains dicts, extract this field before joining (leave empty for direct join)"
    )

    joined_string: str = NodeVariableSettings(
        label="Joined String",
        has_out=True,
        info="The resulting joined string"
    )

    item_count: int = NodeVariableSettings(
        label="Item Count",
        has_out=True,
        info="Number of items that were joined"
    )

    true_path: bool | str = PathSettings(
        label="Joined String",
        info="Returns the joined string"
    )
    false_path: bool | dict = PathSettings(
        label="Error",
        info="Triggered if joining fails"
    )

    def execute(self):
        try:
            if not isinstance(self.input_list, list):
                raise ValueError("Input is not a list")

            items_to_join = []

            for item in self.input_list:
                # If field is specified and item is a dict, extract the field
                if self.field and isinstance(item, dict):
                    value = item.get(self.field, "")
                else:
                    value = item

                # Convert to string
                items_to_join.append(str(value) if value is not None else "")

            self.joined_string = self.separator.join(items_to_join)
            self.item_count = len(items_to_join)
            self.true_path = self.joined_string
            self.false_path = False

        except Exception as e:
            self.false_path = {"error": str(e)}
            self.true_path = False
            self.joined_string = ""
            self.item_count = 0
