from xhtml2pdf import pisa
from tempfile import NamedTemporaryFile

from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="HTML to PDF (Save to File)",
    category="pdf",
    icon="file.svg"
)
class HtmlToPdfFile(Node):

    html_input: str = NodeVariableSettings(
        label="HTML Input",
        has_in=True,
        required=True,
        info="Raw HTML to convert into a PDF file."
    )

    true_path: bool | str | None = PathSettings(
        label="PDF File Path",
        info="Path to the generated PDF file."
    )

    false_path: bool | str | dict | None = PathSettings(
        label="Error",
        info="Triggered if PDF generation fails."
    )

    async def execute(self):
        try:
            with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
                result = pisa.CreatePDF(self.html_input, dest=temp_pdf)
                if result.err:
                    raise Exception("PDF generation failed.")
                self.true_path = temp_pdf.name
        except Exception as e:
            self.false_path = NodeError.format(e)