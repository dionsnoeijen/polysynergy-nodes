from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="File Selection",
    category="file",
    icon="file.svg",
)
class FileSelection(Node):
    selected_files: list = NodeVariableSettings(
        label="Selected Files", 
        has_in=True, 
        has_out=True,
        dock=True,
        info="List of file locations selected from the file manager"
    )
    
    file_count: int = NodeVariableSettings(
        label="File Count", 
        has_out=True,
        info="Number of selected files"
    )

    true_path: bool | list = PathSettings(label="Files", info="List of selected file locations")
    false_path: bool | dict = PathSettings(label="Error", info="Triggered if no files were selected")

    def execute(self):
        if not self.selected_files or len(self.selected_files) == 0:
            self.false_path = {"error": "No files selected from file manager."}
            self.file_count = 0
        else:
            self.true_path = self.selected_files
            self.file_count = len(self.selected_files)