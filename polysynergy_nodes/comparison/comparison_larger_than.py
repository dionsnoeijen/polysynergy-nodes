from polysynergy_nodes.base.setup_context.node import Node
from polysynergy_nodes.base.setup_context.node_decorator import node
from polysynergy_nodes.base.setup_context.node_variable_settings import NodeVariableSettings

@node(name="Larger than", category="comparison", type="larger_than")
class ComparisonLargerThan(Node):
    a: int | float | str = NodeVariableSettings(default=0, has_in=True, dock=True, has_out=True)
    b: int | float | str = NodeVariableSettings(default=0, has_in=True, dock=True, has_out=True)

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
            self.false_path = True
            self.true_path = False
        elif a > b:
            self.true_path = self.a
            self.false_path = False
        else:
            self.false_path = self.b
            self.true_path = False