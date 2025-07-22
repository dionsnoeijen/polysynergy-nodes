from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings


@node(name="Loop", category="flow", type="loop", has_enabled_switch=False)
class Loop(Node):
    repeats: int = NodeVariableSettings(has_in=True, dock=True, required=False, default=1)

    counter: int = 0
    true_path: bool = False

    def execute(self):
        if self.counter >= self.repeats:
            print(f"Loop completed ({self.repeats} times). Stop.")
            self.true_path = True
            return {
                "status": "loop_completed",
                "counter": self.counter
            }

        self.counter += 1
        return {
            "status": "repeat",
            "counter": self.counter
        }