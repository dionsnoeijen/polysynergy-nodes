from polysynergy_nodes.base.execution_context.connection import Connection
from polysynergy_nodes.base.setup_context.node import Node
from polysynergy_nodes.base.setup_context.node_decorator import node
from polysynergy_nodes.base.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_nodes.base.setup_context.path_settings import PathSettings


@node(
    name="List Loop",
    category="flow",
    type="loop",
    icon='loop.svg',
)
class ListLoop(Node):
    out_connections: list[Connection] = []
    _started: bool = False
    _flag: str | None = None

    input_list: list = NodeVariableSettings(has_in=True, required=True, default=[])
    index: int = NodeVariableSettings(label="Index", has_out=True, default=0)

    true_path: bool | list | str | int | float | dict = PathSettings(
        label="Item",
        info="Current Item",
    )

    def break_loop(self):
        self._flag = "break"

    def continue_loop(self):
        self._flag = "continue"

    def execute(self):
        if not self.input_list:
            raise ValueError("List Loop: No valid list provided")

        if self._started is False:
            self._started = True

            nodes_in_loop, loop_end_node = self.find_nodes_in_loop()

            if loop_end_node:
                loop_end_node.make_blocking()

            for index, item in enumerate(self.input_list):

                if self._flag == "break":
                    loop_end_node.unblock()
                    self.flow.execute_node(loop_end_node)
                    self._flag = None
                    break

                if self._flag == "continue":
                    self._flag = None
                    continue

                self.true_path = item
                self.index = index

                for node_in_loop in nodes_in_loop:
                    node_in_loop.resurrect()

                self.resurrect()
                self.flow.execute_node(self)

                if index == len(self.input_list) - 1 and loop_end_node:
                    loop_end_node.unblock()
                    self.flow.execute_node(loop_end_node)

