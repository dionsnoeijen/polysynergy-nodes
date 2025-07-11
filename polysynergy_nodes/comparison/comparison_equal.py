from polysynergy_nodes.base.setup_context.node import Node
from polysynergy_nodes.base.setup_context.node_decorator import node
from polysynergy_nodes.base.setup_context.node_variable_settings import NodeVariableSettings

@node(name="Equal", category="comparison", type="equal")
class ComparisonEqual(Node):
    a: bool | str | int | float = NodeVariableSettings(default=0, dock=True, has_in=True, has_out=True)
    b: bool | str | int | float = NodeVariableSettings(default=0, dock=True, has_in=True, has_out=True)

    true_path: bool | str | int | float = False
    false_path: bool | str | int | float = False

    def coerce(self, value):
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return value
        if isinstance(value, str):
            stripped = value.strip().lower()
            if stripped == "true":
                return True
            if stripped == "false":
                return False
            try:
                return int(stripped) if stripped.isdigit() else float(stripped)
            except ValueError:
                return value
        return value

    def execute(self):
        a = self.coerce(self.a)
        b = self.coerce(self.b)

        if a == b:
            self.true_path = self.a
            self.false_path = False
        else:
            self.false_path = self.b
            self.true_path = False