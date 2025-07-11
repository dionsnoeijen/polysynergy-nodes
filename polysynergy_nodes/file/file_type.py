from polysynergy_nodes.base.setup_context.node import Node
from polysynergy_nodes.base.setup_context.node_decorator import node
from polysynergy_nodes.base.setup_context.node_error import NodeError
from polysynergy_nodes.base.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_nodes.base.setup_context.path_settings import PathSettings


@node(
    name="File Type",
    category="file",
    icon="filetype.svg"
)
class FileType(Node):
    filename: str = NodeVariableSettings(label="Filename", dock=True, has_in=True)

    true_path: bool | str = PathSettings(label="File Type", info="The file type based on the file extension")
    false_path: bool | dict = PathSettings(label="Error", info="Triggered if no valid extension could be found")

    def execute(self):
        try:
            if not self.filename or "." not in self.filename:
                raise ValueError("Filename does not contain an extension.")
            self.true_path = self.filename.split(".")[-1]
        except Exception as e:
            self.false_path = NodeError.format(e)