import base64

from polysynergy_node_runner.setup_context.dock_property import dock_property
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="Bytes to Email Attachment",
    category="email",
    icon="email.svg"
)
class BytesToAttachment(Node):
    """Convert bytes to email attachment format."""

    bytes_input: bytes = NodeVariableSettings(
        label="Bytes",
        has_in=True,
        required=True,
        info="File content as bytes (e.g., from PDF, image, document node)"
    )

    filename: str = NodeVariableSettings(
        label="Filename",
        dock=True,
        has_in=True,
        required=True,
        info="Name for the file (e.g., 'invoice-12345.pdf', 'logo.png')"
    )

    mimetype: str = NodeVariableSettings(
        label="MIME Type",
        dock=dock_property(select_values={
            # Documents
            "application/pdf": "PDF (application/pdf)",
            "application/msword": "Word (DOC)",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "Word (DOCX)",
            "application/vnd.ms-excel": "Excel (XLS)",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "Excel (XLSX)",
            "application/vnd.ms-powerpoint": "PowerPoint (PPT)",
            "application/vnd.openxmlformats-officedocument.presentationml.presentation": "PowerPoint (PPTX)",
            "application/rtf": "Rich Text Format (RTF)",
            "text/plain": "Tekstbestand (TXT)",
            "text/csv": "CSV (Comma Separated Values)",

            # Images
            "image/png": "Afbeelding (PNG)",
            "image/jpeg": "Afbeelding (JPEG)",
            "image/gif": "Afbeelding (GIF)",
            "image/webp": "Afbeelding (WebP)",
            "image/svg+xml": "Vectorafbeelding (SVG)",

            # Archives
            "application/zip": "ZIP Archief",
            "application/x-tar": "TAR Archief",
            "application/gzip": "GZIP Archief",

            # Formats
            "application/json": "JSON-bestand",
            "application/xml": "XML-bestand",
            "text/html": "HTML-bestand",
            "application/yaml": "YAML-bestand",

            # Other
            "application/octet-stream": "Overig (binary)"
        }),
        has_in=True,
        default="application/pdf",
        info="MIME type of the file"
    )

    attachment: dict = NodeVariableSettings(
        label="Attachment",
        has_out=True,
        info="Ready to connect to email node attachments input"
    )

    true_path: dict | bool = PathSettings(
        label="Attachment Dict",
        info="Dict with filename, content (base64), and mimetype"
    )

    false_path: dict | bool = PathSettings(
        label="Error",
        info="Error information if conversion fails"
    )

    async def execute(self):
        try:
            if not isinstance(self.bytes_input, bytes):
                raise ValueError("bytes_input must be bytes type")

            if not self.filename:
                raise ValueError("filename is required")

            if not self.mimetype:
                raise ValueError("mimetype is required")

            # Convert bytes to base64
            content_b64 = base64.b64encode(self.bytes_input).decode('utf-8')

            # Create attachment dict
            attachment_dict = {
                "filename": self.filename,
                "content": content_b64,
                "mimetype": self.mimetype
            }

            self.attachment = attachment_dict
            self.true_path = attachment_dict
            self.false_path = False

        except Exception as e:
            self.false_path = NodeError.format(e)
            self.true_path = False
