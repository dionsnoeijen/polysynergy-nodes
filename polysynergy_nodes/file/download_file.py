import os
import tempfile
import hashlib
import boto3
import requests
from urllib.parse import urlparse
from botocore.exceptions import ClientError
from polysynergy_node_runner.setup_context.dock_property import dock_property
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings
from polysynergy_node_runner.utils.tenant_project_naming import get_prefixed_name


@node(
    name="Download File",
    category="file",
    icon="file.svg",
    version=1.0
)
class DownloadFile(Node):
    file_path: str = NodeVariableSettings(
        label="File Path or URL",
        has_in=True,
        dock=True,
        info="File Manager path (e.g., 'folder/file.csv') or URL (e.g., 'https://example.com/data.csv')"
    )

    timeout: int = NodeVariableSettings(
        label="Timeout",
        default=30,
        dock=True,
        has_in=True,
        info="Timeout in seconds for URL downloads (only for HTTP/HTTPS)"
    )

    decode_as_text: bool = NodeVariableSettings(
        label="Decode as Text",
        default=True,
        dock=True,
        has_in=True,
        info="If True, decode file content as UTF-8 text. If False, return raw bytes."
    )

    file_content: str | bytes = NodeVariableSettings(
        label="File Content",
        has_out=True,
        info="The file content (text or bytes depending on decode_as_text setting)"
    )

    file_name: str = NodeVariableSettings(
        label="File Name",
        has_out=True,
        info="Name of the downloaded file"
    )

    file_size: int = NodeVariableSettings(
        label="File Size",
        has_out=True,
        info="Size of the file in bytes"
    )

    local_path: str = NodeVariableSettings(
        label="Local Path",
        has_out=True,
        info="Path to downloaded file in /tmp/ directory"
    )

    true_path: bool | str | bytes = PathSettings(
        label="Success",
        info="Returns the file content"
    )
    false_path: bool | dict = PathSettings(
        label="Error",
        info="Triggered if download fails"
    )

    async def execute(self):
        try:
            if not self.file_path:
                raise ValueError("File path or URL is required")

            # Determine if it's a URL or S3 key
            is_url = self.file_path.startswith(('http://', 'https://'))

            if is_url:
                # Download from URL
                print(f"[Download File] Downloading from URL: {self.file_path}")
                tmp_path, file_size = await self._download_from_url()
            else:
                # Download from S3 (File Manager)
                print(f"[Download File] Downloading from File Manager: {self.file_path}")
                tmp_path, file_size = await self._download_from_s3()

            # Extract filename
            file_name = os.path.basename(tmp_path)

            # Read file content
            if self.decode_as_text:
                with open(tmp_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            else:
                with open(tmp_path, 'rb') as f:
                    content = f.read()

            # Set outputs
            self.file_content = content
            self.file_name = file_name
            self.file_size = file_size
            self.local_path = tmp_path
            self.true_path = content
            self.false_path = False

            print(f"[Download File] Success: {file_name} ({file_size} bytes)")

        except Exception as e:
            error_msg = f"Failed to download file: {str(e)}"
            print(f"[Download File] Error: {error_msg}")
            self.false_path = {"error": error_msg}
            self.true_path = False
            self.file_content = None
            self.file_name = None
            self.file_size = 0
            self.local_path = None

    async def _download_from_url(self):
        """Download file from HTTP/HTTPS URL"""
        # Parse URL to extract filename
        parsed = urlparse(self.file_path)
        filename = os.path.basename(parsed.path)

        if not filename or "." not in filename:
            # Generate filename from URL hash
            url_hash = hashlib.md5(self.file_path.encode()).hexdigest()[:8]
            filename = f"download_{url_hash}.dat"

        tmp_path = os.path.join(tempfile.gettempdir(), filename)

        # Download with streaming
        response = requests.get(self.file_path, timeout=self.timeout, stream=True)
        response.raise_for_status()

        # Get file size from headers
        file_size = int(response.headers.get('content-length', 0))

        # Download to temp file
        with open(tmp_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        # Get actual file size if not in headers
        if file_size == 0:
            file_size = os.path.getsize(tmp_path)

        print(f"[Download File] Downloaded from URL to: {tmp_path}")
        return tmp_path, file_size

    async def _download_from_s3(self):
        """Download file from S3 (File Manager)"""
        # Get S3 bucket name using same logic as file manager
        bucket = get_prefixed_name(prefix="polysynergy", suffix="media", max_length=63)
        print(f"[Download File] S3 Bucket: {bucket}, Key: {self.file_path}")

        # Initialize S3 client
        s3_client = boto3.client('s3')

        # Check if file exists and get metadata
        try:
            response = s3_client.head_object(Bucket=bucket, Key=self.file_path)
            file_size = response['ContentLength']
            print(f"[Download File] Found in S3: {file_size} bytes")
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                raise ValueError(f"File not found in File Manager: {self.file_path}")
            else:
                raise ValueError(f"S3 error: {e}")

        # Generate local filename
        file_name = os.path.basename(self.file_path)
        if not file_name:
            file_name = "downloaded_file"

        # Download to /tmp/
        tmp_path = os.path.join(tempfile.gettempdir(), file_name)
        s3_client.download_file(bucket, self.file_path, tmp_path)

        print(f"[Download File] Downloaded from S3 to: {tmp_path}")
        return tmp_path, file_size
