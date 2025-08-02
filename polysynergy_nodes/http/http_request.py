# PACKAGE RECOMMENDATION: Move to @polysynergy/web
# This node provides HTTP client functionality with external network dependencies.
# It would be better suited in a dedicated web/network package rather than core basic nodes.

import json
import requests
from http import HTTPMethod

from polysynergy_node_runner.execution_context.replace_placeholders import replace_placeholders
from polysynergy_node_runner.setup_context.dock_property import dock_property, dock_text_area
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
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
    allow_redirects: bool = NodeVariableSettings(label="Allow Redirects", dock=True, has_in=True, default=True)
    verify_ssl: bool = NodeVariableSettings(label="Verify SSL", dock=True, has_in=True, default=True)
    proxies: dict | None = NodeVariableSettings(label="Proxies", dock=True, has_in=True, default=None)

    response_http_status: int = NodeVariableSettings(label="Response HTTP Status", has_out=True)
    response_body: str = NodeVariableSettings(label="Response Body", has_out=True)
    response_headers: dict[str, str] = NodeVariableSettings(label="Response Headers", has_out=True)
    response_cookies: dict[str, str] = NodeVariableSettings(label="Response Cookies", has_out=True)
    response_elapsed: float = NodeVariableSettings(label="Response Elapsed", has_out=True)

    true_path: bool | str = PathSettings(label="Success (Response Body)")
    false_path: bool | dict = PathSettings(label="Error (Exception or HTTP Error)")

    def execute(self):
        try:
            print(f"URL Variables: {self.url_variables}")

            replaced_url_vars = replace_placeholders(
                data=self.url_variables,
                values=self.url_variables,
                state=self.state
            )

            print(f"Replaced URL Variables: {replaced_url_vars}")

            replaced_url = replace_placeholders(data=self.url, values=replaced_url_vars, state=self.state)

            print(f"URL: {self.url}")
            print(f"Replaced URL: {replaced_url}")

            replaced_headers = replace_placeholders(data=self.headers, values=replaced_url_vars, state=self.state)
            replaced_query = replace_placeholders(data=self.query, values=replaced_url_vars, state=self.state)
            replaced_cookies = replace_placeholders(data=self.cookies, values=replaced_url_vars, state=self.state)
            replaced_body = replace_placeholders(data=self.body, values=replaced_url_vars, state=self.state)

            is_json = (
                isinstance(replaced_headers, dict)
                and replaced_headers.get("Content-Type") == "application/json"
            )
            kwargs = {
                "method": self.method,
                "url": replaced_url,
                "headers": replaced_headers,
                "params": replaced_query,
                "cookies": replaced_cookies,
                "timeout": self.timeout,
                "allow_redirects": self.allow_redirects,
                "verify": self.verify_ssl,
                "proxies": self.proxies,
            }

            if is_json:
                try:
                    kwargs["json"] = json.loads(replaced_body) if isinstance(replaced_body, str) else replaced_body
                except Exception:
                    kwargs["data"] = replaced_body  # fallback
            else:
                kwargs["data"] = replaced_body

            response = requests.request(**kwargs)

            self.response_http_status = response.status_code
            self.response_body = response.text
            self.response_headers = dict(response.headers)
            self.response_cookies = requests.utils.dict_from_cookiejar(response.cookies)
            self.response_elapsed = response.elapsed.total_seconds()

            if response.status_code < 400:
                self.true_path = response.text
            else:
                self.false_path = {"error": f"{response.status_code}: {response.text}"}

        except requests.RequestException as e:
            self.false_path = NodeError.format(e)
