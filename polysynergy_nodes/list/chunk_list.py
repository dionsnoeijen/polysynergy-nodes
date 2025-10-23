from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="Chunk/Batch List",
    category="list",
    icon="list.svg",
    version=1.0
)
class ChunkList(Node):
    input_list: list = NodeVariableSettings(
        label="Input List",
        has_in=True,
        dock=True,
        info="The list to divide into chunks"
    )

    chunk_size: int = NodeVariableSettings(
        label="Chunk Size",
        default=10,
        dock=True,
        has_in=True,
        info="Number of items per chunk"
    )

    chunked_list: list = NodeVariableSettings(
        label="Chunked List",
        has_out=True,
        info="List of chunks (list of lists)"
    )

    chunk_count: int = NodeVariableSettings(
        label="Chunk Count",
        has_out=True,
        info="Number of chunks created"
    )

    original_length: int = NodeVariableSettings(
        label="Original Length",
        has_out=True,
        info="Length of the original list"
    )

    true_path: bool | list = PathSettings(
        label="Chunked List",
        info="Returns list of chunks"
    )
    false_path: bool | dict = PathSettings(
        label="Error",
        info="Triggered if chunking fails"
    )

    def execute(self):
        try:
            if not isinstance(self.input_list, list):
                raise ValueError("Input is not a list")

            if self.chunk_size <= 0:
                raise ValueError("Chunk size must be greater than 0")

            self.original_length = len(self.input_list)

            # Create chunks
            chunks = []
            for i in range(0, len(self.input_list), self.chunk_size):
                chunk = self.input_list[i:i + self.chunk_size]
                chunks.append(chunk)

            self.chunked_list = chunks
            self.chunk_count = len(chunks)
            self.true_path = chunks
            self.false_path = False

        except Exception as e:
            self.false_path = {"error": str(e)}
            self.true_path = False
            self.chunked_list = []
            self.chunk_count = 0
            self.original_length = 0
