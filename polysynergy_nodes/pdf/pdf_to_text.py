import io
from pypdf import PdfReader

from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="PDF to Text",
    category="pdf",
    icon="file.svg"
)
class PdfToText(Node):
    """Extract text content from PDF bytes or file."""

    pdf_input: bytes | str = NodeVariableSettings(
        label="PDF Input",
        has_in=True,
        required=True,
        info="PDF as bytes or file path to extract text from"
    )

    text: str = NodeVariableSettings(
        label="Text",
        has_out=True,
        info="Extracted text content from the PDF"
    )

    page_count: int = NodeVariableSettings(
        label="Page Count",
        has_out=True,
        info="Number of pages in the PDF"
    )

    true_path: str | bool = PathSettings(
        label="Text Content",
        info="Extracted text from PDF"
    )

    false_path: dict | bool = PathSettings(
        label="Error",
        info="Error information if extraction fails"
    )

    async def execute(self):
        try:
            # Handle bytes input
            if isinstance(self.pdf_input, bytes):
                pdf_file = io.BytesIO(self.pdf_input)
            # Handle file path input
            elif isinstance(self.pdf_input, str):
                pdf_file = open(self.pdf_input, 'rb')
            else:
                raise ValueError(f"pdf_input must be bytes or str, got {type(self.pdf_input)}")

            # Read PDF
            reader = PdfReader(pdf_file)

            # Extract text from all pages
            text_content = []
            for page_num, page in enumerate(reader.pages, 1):
                page_text = page.extract_text()
                if page_text.strip():
                    text_content.append(f"--- Page {page_num} ---\n{page_text}")

            # Combine all pages
            full_text = "\n\n".join(text_content)

            # Close file if we opened it
            if isinstance(self.pdf_input, str):
                pdf_file.close()

            self.text = full_text
            self.page_count = len(reader.pages)
            self.true_path = full_text
            self.false_path = False

        except Exception as e:
            self.false_path = NodeError.format(e, True)
            self.true_path = False
            self.text = ""
            self.page_count = 0
