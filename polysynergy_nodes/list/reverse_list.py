from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="Reverse List",
    category="list",
    icon="list.svg",
    version=1.0
)
class ReverseList(Node):
    input_list: list = NodeVariableSettings(
        label="Input List",
        has_in=True,
        dock=True,
        info="The list to reverse"
    )

    reversed_list: list = NodeVariableSettings(
        label="Reversed List",
        has_out=True,
        info="The reversed list"
    )

    true_path: bool | list = PathSettings(
        label="Reversed List",
        info="Returns the reversed list"
    )
    false_path: bool | dict = PathSettings(
        label="Error",
        info="Triggered if reversing fails"
    )

    def execute(self):
        try:
            if not isinstance(self.input_list, list):
                raise ValueError("Input is not a list")

            self.reversed_list = list(reversed(self.input_list))
            self.true_path = self.reversed_list
            self.false_path = False

        except Exception as e:
            self.false_path = {"error": str(e)}
            self.true_path = False
            self.reversed_list = []
