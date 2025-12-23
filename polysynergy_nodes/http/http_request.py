import base64
import json
import httpx
import urllib.parse
from http import HTTPMethod

from polysynergy_node_runner.execution_context.replace_placeholders import replace_placeholders
from polysynergy_node_runner.setup_context.dock_property import dock_property, dock_text_area
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="HTTP Request",
    category="http",
    icon='request.svg',
    version=1.01,
)
class HttpRequest(Node):
    url: str = NodeVariableSettings(label="URL", dock=True, has_in=True)
    url_variables: dict[str, str] = NodeVariableSettings(label="URL Variables", dock=True, has_in=True)
    method: str = NodeVariableSettings(
        label="Method",
        default=HTTPMethod.GET,
        dock=dock_property(select_values={method.upper(): method.upper() for method in HTTPMethod}),
        has_in=True
    )
    headers: dict[str, str] = NodeVariableSettings(label="Headers", dock=True, has_in=True)
    body: bytes | str = NodeVariableSettings(label="Body", dock=dock_text_area(), has_in=True)
    query: dict[str, str] = NodeVariableSettings(label="Query", dock=True, has_in=True)
    cookies: dict[str, str] = NodeVariableSettings(label="Cookies", dock=True, has_in=True)
    timeout: float = NodeVariableSettings(label="Timeout", dock=True, has_in=True, default=10.0)
    follow_redirects: bool = NodeVariableSettings(
        label="Follow Redirects", 
        dock=True, 
        has_in=True, 
        default=True,
        info="When enabled, automatically follows HTTP redirect responses (3xx status codes). When disabled, redirect responses are returned as-is without following them."
    )
    verify_ssl: bool = NodeVariableSettings(label="Verify SSL", dock=True, has_in=True, default=True)
    proxies: dict | None = NodeVariableSettings(label="Proxies", dock=True, has_in=True, default=None)
    files: list = NodeVariableSettings(
        label="Files",
        dock=True,
        has_in=True,
        default=[],
        info='List of files: [{"filename": "test.pdf", "content": bytes/base64, "content_type": "application/pdf", "field_name": "file"}]'
    )

    response_http_status: int = NodeVariableSettings(label="Response HTTP Status", has_out=True)
    response_body: str = NodeVariableSettings(label="Response Body", has_out=True)
    response_headers: dict[str, str] = NodeVariableSettings(label="Response Headers", has_out=True)
    response_cookies: dict[str, str] = NodeVariableSettings(label="Response Cookies", has_out=True)
    response_elapsed: float = NodeVariableSettings(label="Response Elapsed", has_out=True)

    true_path: bool | str | bytes = PathSettings(label="Success")
    false_path: bool | dict = PathSettings(label="Error")

    def is_url_encoded(self, url: str) -> bool:
        """Check if a URL appears to be already encoded"""
        # Check for common signs of URL encoding
        # If we see %20, %2F, %3A etc, it's likely already encoded
        import re
        return bool(re.search(r'%[0-9A-Fa-f]{2}', url))

    def smart_url_encode(self, url: str) -> str:
        """Encode URL only if not already encoded"""
        if self.is_url_encoded(url):
            print(f"[HTTP] URL appears already encoded, using as-is: {url}")
            return url

        # Parse the URL
        parsed = urllib.parse.urlparse(url)

        # Encode the path component if needed
        encoded_path = urllib.parse.quote(parsed.path, safe='/:@!$&\'()*+,;=')

        # Reconstruct the URL
        encoded_url = urllib.parse.urlunparse((
            parsed.scheme,
            parsed.netloc,
            encoded_path,
            parsed.params,
            parsed.query,  # Query will be handled separately via params
            parsed.fragment
        ))

        if encoded_url != url:
            print(f"[HTTP] URL encoded: {url} -> {encoded_url}")

        return encoded_url

    async def execute(self):
        try:
            # Log the incoming request details
            print(f"\n[HTTP] ========== HTTP Request Starting ==========")
            print(f"[HTTP] Method: {self.method}")
            print(f"[HTTP] URL (raw): {self.url}")
            replaced_url_vars = replace_placeholders(
                data=self.url_variables,
                values=self.url_variables,
                state=self.state,
                current_node=self
            )

            replaced_url = replace_placeholders(data=self.url, values=replaced_url_vars, state=self.state, current_node=self)

            # Apply smart URL encoding
            replaced_url = self.smart_url_encode(replaced_url)

            print(f"[HTTP] URL (final): {replaced_url}")

            # Replace placeholders in headers, query, cookies, and body
            # Note: we pass state and current_node so that node handles like {{ other_node.true_path }} work
            replaced_headers = replace_placeholders(data=self.headers, values=None, state=self.state, current_node=self)
            replaced_query = replace_placeholders(data=self.query, values=replaced_url_vars, state=self.state, current_node=self)
            replaced_cookies = replace_placeholders(data=self.cookies, values=replaced_url_vars, state=self.state, current_node=self)
            replaced_body = replace_placeholders(data=self.body, values=replaced_url_vars, state=self.state, current_node=self)

            # Log headers - BEFORE and AFTER replacement
            print(f"[HTTP] Headers (ORIGINAL): {json.dumps(self.headers, indent=2) if self.headers else 'None'}")
            print(f"[HTTP] Headers (REPLACED): {json.dumps(replaced_headers, indent=2) if replaced_headers else 'None'}")

            # Check for unreplaced placeholders in headers
            if replaced_headers:
                for key, value in replaced_headers.items():
                    if '{{' in str(value) or '}}' in str(value):
                        print(f"[HTTP] ⚠️  WARNING: Unreplaced placeholder in header '{key}': {value}")

            # Log query params if present
            if replaced_query:
                print(f"[HTTP] Query params: {json.dumps(replaced_query, indent=2)}")

            # Log body preview if present
            if replaced_body:
                body_preview = str(replaced_body)[:500] if len(str(replaced_body)) > 500 else str(replaced_body)
                print(f"[HTTP] Body (first 500 chars): {body_preview}")

            print(f"[HTTP] Timeout: {self.timeout}s")
            print(f"[HTTP] Follow redirects: {self.follow_redirects}")
            print(f"[HTTP] Verify SSL: {self.verify_ssl}")

            # Check if we have files to upload
            has_files = self.files and isinstance(self.files, list) and len(self.files) > 0

            is_json = (
                isinstance(replaced_headers, dict)
                and replaced_headers.get("Content-Type") == "application/json"
                and not has_files  # Don't use JSON if we have files
            )

            # Prepare headers - remove Content-Type for multipart (httpx sets it automatically with boundary)
            request_headers = replaced_headers.copy() if replaced_headers else {}
            if has_files and "Content-Type" in request_headers:
                print(f"[HTTP] Removing Content-Type header for multipart request (was: {request_headers['Content-Type']})")
                del request_headers["Content-Type"]

            kwargs = {
                "method": self.method,
                "url": replaced_url,
                "headers": request_headers,
                "params": replaced_query,
                "cookies": replaced_cookies,
                "timeout": self.timeout,
                "follow_redirects": self.follow_redirects,
            }

            # Create client with SSL verification setting
            client_kwargs = {
                "verify": self.verify_ssl,
            }
            if self.proxies:
                client_kwargs["proxies"] = self.proxies

            # Handle file uploads
            if has_files:
                httpx_files = {}
                for file_item in self.files:
                    if not isinstance(file_item, dict):
                        continue

                    field_name = file_item.get("field_name", "file")
                    filename = file_item.get("filename", "upload")
                    content = file_item.get("content")
                    content_type = file_item.get("content_type", "application/octet-stream")

                    if content is None:
                        continue

                    # Handle base64 encoded content
                    if isinstance(content, str):
                        try:
                            content = base64.b64decode(content)
                        except Exception:
                            # Not base64, use as-is (encode to bytes)
                            content = content.encode('utf-8')

                    httpx_files[field_name] = (filename, content, content_type)
                    print(f"[HTTP] Adding file: field_name={field_name}, filename={filename}, content_type={content_type}, size={len(content)} bytes")

                kwargs["files"] = httpx_files

                # If body is present with files, treat it as form data
                if replaced_body and isinstance(replaced_body, str):
                    try:
                        form_data = json.loads(replaced_body)
                        if isinstance(form_data, dict):
                            kwargs["data"] = form_data
                            print(f"[HTTP] Adding form data: {list(form_data.keys())}")
                    except json.JSONDecodeError:
                        pass  # Not JSON, ignore body for multipart

            elif is_json:
                try:
                    kwargs["json"] = json.loads(replaced_body) if isinstance(replaced_body, str) else replaced_body
                except Exception:
                    kwargs["content"] = replaced_body  # fallback
            else:
                kwargs["content"] = replaced_body

            async with httpx.AsyncClient(**client_kwargs) as client:
                print(f"[HTTP] Sending {self.method} request...")
                response = await client.request(**kwargs)
                print(f"[HTTP] Response received: Status {response.status_code}")

            self.response_http_status = response.status_code
            self.response_body = response.text
            self.response_headers = dict(response.headers)
            self.response_cookies = dict(response.cookies)
            self.response_elapsed = response.elapsed.total_seconds()

            # Log response details
            print(f"[HTTP] Response time: {self.response_elapsed:.3f}s")
            print(f"[HTTP] Response headers: {json.dumps(dict(response.headers), indent=2)}")
            if response.text and len(response.text) < 1000:
                print(f"[HTTP] Response body: {response.text}")
            elif response.text:
                print(f"[HTTP] Response body (first 1000 chars): {response.text[:1000]}...")

            # Auto-detect binary content based on multiple criteria
            content_type = response.headers.get('content-type', '').lower()
            content_disposition = response.headers.get('content-disposition', '').lower()

            is_binary = (
                # Common binary MIME types
                content_type.startswith(('application/', 'image/', 'video/', 'audio/')) or
                # File download indication
                'attachment' in content_disposition or
                # Binary content detection (null bytes in first 512 bytes)
                b'\x00' in response.content[:512]
            )

            if response.status_code < 400:
                print(f"[HTTP] ✓ Request successful (status {response.status_code})")
                self.true_path = response.content if is_binary else response.text
            else:
                print(f"[HTTP] ✗ Request failed with HTTP error {response.status_code}")
                self.false_path = {"error": f"{response.status_code}: {response.text}"}

        except Exception as e:
            error_msg = f"{type(e).__name__}: {str(e)}"
            print(f"[HTTP] ✗ Request failed with exception: {error_msg}")
            self.false_path = {
                "error": error_msg,
                "error_type": type(e).__name__,
                "details": str(e)
            }
        finally:
            print(f"[HTTP] ========== HTTP Request Complete ==========")
