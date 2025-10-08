from datetime import datetime, timezone, timedelta
import re

from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="Now",
    category="datetime",
    icon="time.svg"
)
class Now(Node):
    format: str = NodeVariableSettings(
        label="Output Format",
        dock=True,
        has_in=True,
        default="%Y-%m-%d %H:%M:%S"
    )

    offset: str = NodeVariableSettings(
        label="Offset (e.g. -5s, +2m, -1h, +3d)",
        dock=True,
        has_in=True,
        default=""
    )

    timestamp_output: int = NodeVariableSettings(
        label="UNIX Timestamp",
        has_out=True
    )

    true_path: bool | str = PathSettings(label="Formatted Date", info="The current date and time in the specified format")
    false_path: bool | dict = PathSettings(label="Error", info="An error occurred while getting the date and time")

    def parse_offset(self, offset_str: str) -> timedelta:
        """
        Parse offset string like '-5s', '+2m', '-1h', '+3d'
        """
        if not offset_str:
            return timedelta(0)

        match = re.match(r'^([+-]?)(\d+)([smhd])$', offset_str.strip())
        if not match:
            raise ValueError(f"Invalid offset format: {offset_str}")

        sign, value, unit = match.groups()
        value = int(value)
        if sign == "-":
            value *= -1

        if unit == "s":
            return timedelta(seconds=value)
        elif unit == "m":
            return timedelta(minutes=value)
        elif unit == "h":
            return timedelta(hours=value)
        elif unit == "d":
            return timedelta(days=value)
        else:
            raise ValueError(f"Unsupported offset unit: {unit}")

    def execute(self):
        try:
            now = datetime.now(timezone.utc)
            offset_delta = self.parse_offset(self.offset)
            adjusted_time = now + offset_delta

            if self.format.lower() == "iso8601":
                self.true_path = adjusted_time.isoformat().replace("+00:00", "Z")
            else:
                self.true_path = adjusted_time.strftime(self.format)

            self.timestamp_output = int(adjusted_time.timestamp())

        except Exception as e:
            self.false_path = NodeError.format(e)
            self.timestamp_output = None