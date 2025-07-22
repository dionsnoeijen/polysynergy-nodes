from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings


@node(name="Smaller than", category="comparison", type="smaller_than")
class ComparisonSmallerThan(Node):

    a: int | float | str = NodeVariableSettings(default=0, has_in=True, has_out=True, dock=True)
    b: int | float | str = NodeVariableSettings(default=0, has_in=True, has_out=True, dock=True)

    true_path: bool | int | float = False
    false_path: bool | int | float = False

    def execute(self):
        def to_number(value):
            if isinstance(value, (int, float)):
                return value
            if isinstance(value, str):
                try:
                    return float(value) if "." in value else int(value)
                except ValueError:
                    pass
            return None

        a = to_number(self.a)
        b = to_number(self.b)

        if a is None or b is None:
            self.true_path = False
            self.false_path = True
        elif a < b:
            self.true_path = self.a
            self.false_path = False
        else:
            self.true_path = False
            self.false_path = self.b