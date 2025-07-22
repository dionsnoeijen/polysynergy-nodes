from polysynergy_node_runner.setup_context.dock_property import dock_files
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="Upload File(s) From UI",
    category="file",
    icon="file.svg",
)
class UploadFromUI(Node):
    files: list = NodeVariableSettings(label="Uploaded Files", dock=dock_files())
    directory: str = NodeVariableSettings(label="Directory", dock=True, default="")
    is_public: bool = NodeVariableSettings(label="Public?", dock=True, default=False)

    true_path: bool | list = PathSettings(label="Files", info="List of uploaded files")
    false_path: bool | dict = PathSettings(label="Error", info="Triggered if no files were found")

    def execute(self):
        if not self.files:
            self.false_path = {"error": "No files received from UI."}
        else:
            self.true_path = self.files