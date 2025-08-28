from http import HTTPStatus
import logging

from polysynergy_node_runner.execution_context.replace_placeholders import replace_placeholders
from polysynergy_node_runner.setup_context.dock_property import dock_property, dock_text_area
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings

logger = logging.getLogger(__name__)


@node(
    name="HTTP Response",
    category="http",
    version=1.01
)
class HttpResponse(Node):
    headers: dict[str, str] = NodeVariableSettings(
        label="Headers", dock=True, has_in=True
    )

    body: bytes | str | int | float | bool = NodeVariableSettings(
        label="Body", dock=dock_text_area(), has_in=True
    )

    http_status: int = NodeVariableSettings(
        label="HTTP Status",
        dock=dock_property(
            select_values={
                str(status.value): f"{status.value} – {status.phrase}"
                for status in HTTPStatus
            }
        ),
        default=HTTPStatus.OK.value,
        has_in=True,
    )

    content_type: str = NodeVariableSettings(
        label="Content-Type",
        dock=dock_property(select_values={
            "application/json": "JSON (application/json)",
            "text/plain": "Plain text (text/plain)",
            "text/html": "HTML (text/html)",
            "application/xml": "XML (application/xml)",
            "application/octet-stream": "Binary (octet-stream)",
        }),
        default="application/json",
        has_in=True,
    )

    response: dict | None = None

    async def execute(self):
        try:
            # Replace placeholders in headers
            self.headers = replace_placeholders(
                data=self.headers or {},
                values={},
                state=self.state
            )

            # Replace placeholders in content_type
            self.content_type = replace_placeholders(
                data=self.content_type,
                values={},
                state=self.state
            )

            # Replace placeholders in body (only if it's not bytes)
            if not isinstance(self.body, bytes):
                self.body = replace_placeholders(
                    data=self.body,
                    values={},
                    state=self.state
                )

            merged_headers: dict[str, str] = dict(self.headers)
            if self.content_type:
                merged_headers["Content-Type"] = self.content_type

            self.response = {
                "status": self.http_status,
                "headers": merged_headers,
                "body": self.body,
            }
        except Exception as e:
            logger.error("Error creating HTTP response: %s", e, exc_info=True)
            self.response = None
