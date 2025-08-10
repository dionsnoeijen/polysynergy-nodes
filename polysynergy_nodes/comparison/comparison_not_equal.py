from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings

@node(
    name="Not Equal",
    category="comparison",
    type="not_equal",
    icon="comparison.svg"
)
class ComparisonNotEqual(Node):
    a: bool | str | int | float = NodeVariableSettings(default=0, dock=True, has_in=True, has_out=True)
    b: bool | str | int | float = NodeVariableSettings(default=0, dock=True, has_in=True, has_out=True)

    true_path: bool | str | int | float = False
    false_path: bool | str | int | float = False

    def execute(self):
        def to_primitive(value):
            if isinstance(value, (int, float, bool)):
                return value
            if isinstance(value, str):
                val = value.strip().lower()
                if val in ["true", "yes"]:
                    return True
                if val in ["false", "no"]:
                    return False
                try:
                    return float(value) if "." in value else int(value)
                except ValueError:
                    return value
            return value

        a = to_primitive(self.a)
        b = to_primitive(self.b)

        if a != b:
            self.true_path = self.a
            self.false_path = False
        else:
            self.false_path = self.b
            self.true_path = False