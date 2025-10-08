import os
import tempfile
import uuid
from pathlib import Path

from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.execution_context.replace_placeholders import replace_placeholders


@node(name="Blob to Tmp", category="file", icon="download.svg")
class BlobToTmp(Node):

    # Inputs
    blob: bytes = NodeVariableSettings(
        label="File Data",
        has_in=True,
        required=True,
        info="Binary file data to save to temporary directory"
    )

    filename: str | None = NodeVariableSettings(
        label="Filename",
        dock=True,
        has_in=True,
        info="Optional filename (with or without extension)"
    )

    extension: str | None = NodeVariableSettings(
        label="Extension",
        dock=True,
        has_in=True,
        info="Optional file extension (.pdf, .docx, etc.)"
    )

    # Outputs
    tmp_path: str | None = NodeVariableSettings(
        label="Tmp Path",
        has_out=True,
        info="Full path to the created temporary file"
    )

    file_size: int | None = NodeVariableSettings(
        label="File Size",
        has_out=True,
        info="Size of the file in bytes"
    )

    file_extension: str | None = NodeVariableSettings(
        label="Extension",
        has_out=True,
        info="Final file extension used"
    )

    original_filename: str | None = NodeVariableSettings(
        label="Original Name",
        has_out=True,
        info="Original filename that was provided"
    )

    # Paths
    true_path: str = PathSettings(
        label="File Path",
        info="Path to the created temporary file"
    )

    false_path: bool = PathSettings(
        label="Error",
        info="Triggered when file writing fails"
    )

    async def execute(self):
        try:
            if not self.blob:
                self.false_path = NodeError.format("No blob data provided")
                return

            # Convert string to bytes if necessary
            if isinstance(self.blob, str):
                # Encode string to bytes (for text content that was incorrectly passed as string)
                blob_data = self.blob.encode('utf-8')
            elif isinstance(self.blob, bytes):
                blob_data = self.blob
            else:
                self.false_path = NodeError.format(f"Unsupported blob type: {type(self.blob)}")
                return

            # Resolve placeholders in inputs
            resolved_filename = replace_placeholders(
                data=self.filename,
                values={},
                state=self.state,
                current_node=self
            ) if self.filename else None

            resolved_extension = replace_placeholders(
                data=self.extension,
                values={},
                state=self.state,
                current_node=self
            ) if self.extension else None

            # Generate filename
            if resolved_filename:
                base_name = Path(resolved_filename).stem
                original_ext = Path(resolved_filename).suffix
            else:
                base_name = "download"
                original_ext = ""

            # Determine extension
            if resolved_extension:
                ext = resolved_extension if resolved_extension.startswith('.') else f'.{resolved_extension}'
            elif original_ext:
                ext = original_ext
            else:
                ext = '.bin'  # fallback

            # Create unique filename to avoid collisions
            unique_id = str(uuid.uuid4())[:8]
            final_filename = f"{unique_id}_{base_name}{ext}"

            # Write to tmp directory
            tmp_path = os.path.join(tempfile.gettempdir(), final_filename)

            with open(tmp_path, 'wb') as f:
                f.write(blob_data)

            # Set outputs
            self.tmp_path = tmp_path
            self.file_size = len(blob_data)
            self.file_extension = ext
            self.original_filename = resolved_filename
            self.true_path = tmp_path  # Return the file path for easy chaining

        except Exception as e:
            self.false_path = NodeError.format(f"Failed to write blob to tmp: {str(e)}")