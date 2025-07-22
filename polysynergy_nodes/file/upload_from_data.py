import base64
import os

from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings
from polysynergy_nodes.file.services.s3 import S3Service
from polysynergy_node_runner.setup_context.node_error import NodeError


@node(
    name="Upload From Data",
    category="file",
    icon="file.svg",
)
class UploadFromData(Node):
    file_base64: str = NodeVariableSettings(label="File (Base64)", has_in=True)
    file_bytes: bytes = NodeVariableSettings(label="File (Binary)", has_in=True)
    file_name: str = NodeVariableSettings(label="Filename", has_in=True, required=True)
    directory: str = NodeVariableSettings(label="Directory", has_in=True, default="")
    is_public: bool = NodeVariableSettings(label="Public?", has_in=True, has_out=True, default=False)

    url: str = NodeVariableSettings(label="File URL", has_out=True)

    true_path: bool | str = PathSettings(label="Uploaded File", info="Uploaded file key")
    false_path: bool | dict = PathSettings(label="Error", info="Triggered on upload failure")

    tenant_id: str = os.getenv('TENANT_ID')
    project_id: str = os.getenv('PROJECT_ID')

    def execute(self):
        try:
            s3_client = S3Service(public=self.is_public)
            decoded_content = None

            if self.file_base64:
                decoded_content = base64.b64decode(self.file_base64)
            elif self.file_bytes:
                decoded_content = self.file_bytes
            else:
                raise ValueError("No file content provided.")

            if not self.tenant_id:
                raise ValueError("Missing tenant_id.")
            if not self.project_id:
                raise ValueError("Missing project_id.")
            if not self.file_name:
                raise ValueError("Missing file_name.")

            scope = "public" if self.is_public else "private"
            prefix = f"{self.tenant_id}/{self.project_id}/{scope}"
            if self.directory:
                prefix += f"/{self.directory.strip('/')}"

            file_key = f"{prefix}/{self.file_name}"
            url = s3_client.upload_file(decoded_content, file_key)

            if not url:
                raise ValueError("Failed to upload file to S3.")

            self.url = url

            self.true_path = file_key
        except Exception as e:
            self.false_path = NodeError.format(e)