from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings

from polysynergy_nodes.image.types import Image


@node(
    name="Image",
    category="image",
    icon="image.svg",
    version=1.0
)
class ImageNode(Node):
    """
    Image input node.

    Select a single image from the file manager.
    Outputs the image object for use in other image processing nodes.
    """

    selected_image: Image = NodeVariableSettings(
        label="Selected Image",
        info="Select an image from the file manager",
        has_in=True,
        has_out=True
    )

    image_url: str = NodeVariableSettings(
        label="Image URL",
        info="Direct URL to the image",
        has_out=True
    )

    true_path: Image = PathSettings(
        label="Image",
        info="The selected image"
    )

    false_path: dict = PathSettings(
        label="Error",
        info="No image selected"
    )

    def execute(self):
        if not self.selected_image:
            self.false_path = {"error": "No image selected from file manager."}
            self.image_url = ''
            return

        # Extract URL from image object
        if isinstance(self.selected_image, dict):
            self.image_url = self.selected_image.get('url') or self.selected_image.get('image_url', '')
        elif isinstance(self.selected_image, str):
            self.image_url = self.selected_image
            self.selected_image = {"url": self.selected_image}

        self.true_path = self.selected_image
