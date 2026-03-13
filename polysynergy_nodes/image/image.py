from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings

from polysynergy_nodes.image.types import Image


@node(
    name="Image",
    category="image",
    icon="image.svg",
    version=1.1
)
class ImageNode(Node):
    """
    Image input node.

    Accepts an image from the file manager, a URL, or base64-encoded data.
    When base64_data is provided, it takes priority over selected_image.
    Outputs the image object for use in other image processing nodes.
    """

    selected_image: Image = NodeVariableSettings(
        label="Selected Image",
        info="Select an image from the file manager or provide a URL",
        has_in=True,
        has_out=True
    )

    base64_data: str = NodeVariableSettings(
        label="Base64 Data",
        info="Base64-encoded image data (takes priority over Selected Image)",
        dock=True,
        has_in=True
    )

    image_url: str = NodeVariableSettings(
        label="Image URL",
        info="Direct URL to the image (empty when base64 input)",
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
        # Base64 input takes priority
        if self.base64_data:
            self.selected_image = {"base64": self.base64_data}
            self.image_url = ''
            self.true_path = self.selected_image
            return

        if not self.selected_image:
            self.false_path = {"error": "No image provided."}
            self.image_url = ''
            return

        # Handle URL string input
        if isinstance(self.selected_image, str):
            self.image_url = self.selected_image
            self.selected_image = {"url": self.selected_image}
            self.true_path = self.selected_image
            return

        # Handle dict input (file manager / image object)
        if isinstance(self.selected_image, dict):
            self.image_url = self.selected_image.get('url') or self.selected_image.get('image_url', '')
            self.true_path = self.selected_image
            return

        self.false_path = {"error": f"Unsupported image input type: {type(self.selected_image).__name__}"}
