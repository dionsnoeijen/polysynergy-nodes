from polysynergy_nodes import base64

from polysynergy_nodes.base.setup_context.dock_property import dock_property
from polysynergy_nodes.base.setup_context.node import Node
from polysynergy_nodes.base.setup_context.node_decorator import node
from polysynergy_nodes.base.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_nodes.base.setup_context.path_settings import PathSettings


@node(
    name="Create Attachment",
    category="email",
    icon="file.svg"
)
class EmailAttachment(Node):
    filepath: str = NodeVariableSettings(
        label="File Path",
        has_in=True,
        required=True,
        info="Path to the file to attach (e.g., /tmp/report.pdf)"
    )

    filename: str = NodeVariableSettings(
        label="Attachment Filename",
        dock=True,
        has_in=True,
        required=True,
        info="The name the file will have in the email (e.g., report.pdf)"
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
        default="application/octet-stream",
        info="Selecteer MIME type for attachment."
    )

    true_path: dict | None = PathSettings(
        label="Attachment Dict",
        info="Dict with filename, content (base64), and mimetype"
    )

    false_path: dict | None = PathSettings(
        label="Error",
        info="Error if file could not be read or encoded"
    )

    def execute(self):
        try:
            with open(self.filepath, "rb") as f:
                encoded = base64.b64encode(f.read()).decode("utf-8")

            self.true_path = {
                "filename": self.filename,
                "content": encoded,
                "mimetype": self.mimetype
            }

        except Exception as e:
            self.false_path = {"error": str(e)}