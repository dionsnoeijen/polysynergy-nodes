from xhtml2pdf import pisa
from io import BytesIO

from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings
from polysynergy_node_runner.setup_context.node_error import NodeError


@node(
    name="HTML to PDF (Bytes)",
    category="pdf",
    icon="file.svg"
)
class HtmlToPdfBytes(Node):

    html_input: str = NodeVariableSettings(
        label="HTML Input",
        has_in=True,
        required=True,
        info="Raw HTML to convert into a PDF file."
    )

    true_path: bytes | None = PathSettings(
        label="PDF Bytes",
        info="The binary PDF output, ready to be attached to an email."
    )

    false_path: str | dict | None = PathSettings(
        label="Error",
        info="Triggered if PDF conversion fails."
    )

    async def execute(self):
        try:
            buffer = BytesIO()
            result = pisa.CreatePDF(self.html_input, dest=buffer)
            if result.err:
                raise Exception("PDF generation failed.")
            self.true_path = buffer.getvalue()
        except Exception as e:
            self.false_path = NodeError.format(e)