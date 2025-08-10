import random
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings, dock_property
from polysynergy_node_runner.setup_context.path_settings import PathSettings
from polysynergy_node_runner.setup_context.node_error import NodeError


@node(
    name="Random Color",
    category="random",
    icon="dice.svg",
    version=1.0
)
class RandomColor(Node):
    format: str = NodeVariableSettings(
        label="Format",
        dock=dock_property(
            select_values={
                "hex": "Hex (#FFFFFF)",
                "rgb": "RGB (255, 255, 255)",
                "hsl": "HSL (360, 100%, 50%)",
                "name": "Color Name"
            }
        ),
        default="hex",
        has_in=True
    )

    true_path: str = PathSettings(label="Random Color")
    false_path: dict = PathSettings(label="Error")

    def _generate_hex_color(self) -> str:
        """Generate a random hex color."""
        return f"#{random.randint(0, 0xFFFFFF):06x}"

    def _generate_rgb_color(self) -> str:
        """Generate a random RGB color."""
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return f"rgb({r}, {g}, {b})"

    def _generate_hsl_color(self) -> str:
        """Generate a random HSL color."""
        h = random.randint(0, 360)
        s = random.randint(0, 100)
        l = random.randint(0, 100)
        return f"hsl({h}, {s}%, {l}%)"

    def _generate_color_name(self) -> str:
        """Generate a random color name."""
        color_names = [
            "red", "blue", "green", "yellow", "orange", "purple", "pink", "brown",
            "black", "white", "gray", "cyan", "magenta", "lime", "navy", "teal",
            "silver", "gold", "crimson", "indigo", "violet", "turquoise", "coral",
            "salmon", "khaki", "plum", "orchid", "tan", "beige", "maroon"
        ]
        return random.choice(color_names)

    async def execute(self):
        try:
            if self.format == "hex":
                self.true_path = self._generate_hex_color()
            elif self.format == "rgb":
                self.true_path = self._generate_rgb_color()
            elif self.format == "hsl":
                self.true_path = self._generate_hsl_color()
            elif self.format == "name":
                self.true_path = self._generate_color_name()
            else:
                self.false_path = NodeError.format(f"Unsupported color format: {self.format}")
        except Exception as e:
            self.false_path = NodeError.format(e)