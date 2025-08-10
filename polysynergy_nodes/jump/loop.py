from polysynergy_node_runner.execution_context.connection import Connection
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="Loop", 
    category="flow", 
    type="loop", 
    icon='loop.svg',
    has_enabled_switch=False
)
class Loop(Node):
    out_connections: list[Connection] = []
    _started: bool = False
    _flag: str | None = None

    repeats: int = NodeVariableSettings(label="Repeats", has_in=True, dock=True, required=False, default=1)
    counter: int = NodeVariableSettings(label="Counter", has_out=True, default=0)

    true_path: bool | int = PathSettings(
        label="Counter",
        info="Current iteration counter",
    )

    def break_loop(self):
        self._flag = "break"

    def continue_loop(self):
        self._flag = "continue"

    async def execute(self):
        if self.repeats <= 0:
            raise ValueError("Loop: Number of repeats must be greater than 0")

        if self._started is False:
            self._started = True

            nodes_in_loop, loop_end_node = self.find_nodes_in_loop()

            if loop_end_node:
                loop_end_node.make_blocking()

            for iteration in range(self.repeats):
                
                self.counter = iteration + 1  # 1-based counter for user friendliness
                self.true_path = self.counter

                for node_in_loop in nodes_in_loop:
                    node_in_loop.resurrect()

                self.resurrect()

                await self.flow.execute_node(self)

                # Check flags after execution
                if self._flag == "break":
                    if loop_end_node:
                        loop_end_node.unblock()
                        await self.flow.execute_node(loop_end_node)
                    self._flag = None
                    break

                if self._flag == "continue":
                    self._flag = None
                    # Skip to next iteration but continue the loop
                    continue

                # Handle loop end for final iteration (only if no break/continue)
                if iteration == self.repeats - 1 and loop_end_node:
                    loop_end_node.unblock()
                    await self.flow.execute_node(loop_end_node)