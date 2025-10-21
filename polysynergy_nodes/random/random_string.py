import random
import string

from polysynergy_node_runner.setup_context.dock_property import dock_property, dock_select_values
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="Random String",
    category="random",
    icon='dice.svg',
    version=1.0
)
class RandomString(Node):
    """Generate a random string with configurable length and case."""

    length: int = NodeVariableSettings(
        label="Length",
        dock=True,
        has_in=True,
        default=8,
        required=True,
        info="Number of characters in the random string"
    )

    case_type: str = NodeVariableSettings(
        label="Case Type",
        dock=dock_select_values({
            "upper": "UPPERCASE",
            "lower": "lowercase",
            "mixed": "Mixed Case"
        }),
        default="mixed",
        has_in=True,
        info="Character case for the random string"
    )

    include_digits: bool = NodeVariableSettings(
        label="Include Digits",
        dock=dock_property(switch=True),
        has_in=True,
        default=False,
        info="Include numbers (0-9) in the random string"
    )

    true_path: str | bool = PathSettings(
        label="Result",
        info="The generated random string"
    )

    false_path: dict | bool = PathSettings(
        label="Error",
        info="Error information if generation fails"
    )

    async def execute(self):
        try:
            # Validate length
            if not isinstance(self.length, int) or self.length <= 0:
                raise ValueError("Length must be a positive integer")

            # Build character set based on case type
            if self.case_type == "upper":
                chars = string.ascii_uppercase
            elif self.case_type == "lower":
                chars = string.ascii_lowercase
            elif self.case_type == "mixed":
                chars = string.ascii_letters  # Both upper and lower
            else:
                raise ValueError(f"Invalid case type: {self.case_type}")

            # Add digits if requested
            if self.include_digits:
                chars += string.digits

            # Generate random string
            random_string = ''.join(random.choice(chars) for _ in range(self.length))

            self.true_path = random_string
            self.false_path = False

        except Exception as e:
            self.false_path = NodeError.format(e)
            self.true_path = False
