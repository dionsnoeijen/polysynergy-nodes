from datetime import datetime, timedelta, timezone
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings, dock_property
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="Fixed Time Window",
    category="datetime",
    icon="time.svg"
)
class FixedWindow(Node):
    reference_time: str = NodeVariableSettings(
        label="Reference Time (ISO)",
        dock=True,
        has_in=True,
        default=""
    )

    unit: str = NodeVariableSettings(
        label="Unit",
        default="minutes",
        dock=dock_property(
            select_values={
                "seconds": "Seconds",
                "minutes": "Minutes",
                "hours": "Hours"
            }
        ),
        has_in=True
    )

    interval: int = NodeVariableSettings(
        label="Interval",
        default=5,
        dock=True,
        has_in=True
    )

    format: str = NodeVariableSettings(
        label="Output Format",
        default="iso8601",
        dock=True,
        has_in=True
    )

    window_start: str = NodeVariableSettings(label="Window Start", has_out=True)
    window_end: str = NodeVariableSettings(label="Window End", has_out=True)

    false_path: bool | dict = PathSettings(label="Error")

    def format_time(self, dt: datetime) -> str:
        if self.format.lower() == "iso8601":
            return dt.isoformat().replace("+00:00", "Z")
        return dt.strftime(self.format)

    def execute(self):
        try:
            if self.reference_time:
                try:
                    now = datetime.fromisoformat(self.reference_time.replace("Z", "+00:00"))
                except ValueError:
                    raise ValueError(f"Invalid reference_time format: {self.reference_time}")
            else:
                now = datetime.now(timezone.utc)

            now = now.replace(microsecond=0)
            unit = self.unit.lower()
            interval = int(self.interval)

            # 1. Nu afronden naar beneden
            if unit == "seconds":
                delta = timedelta(seconds=interval)
                floored = now - timedelta(seconds=now.second % interval)

            elif unit == "minutes":
                delta = timedelta(minutes=interval)
                floored = now - timedelta(
                    minutes=now.minute % interval,
                    seconds=now.second,
                )

            elif unit == "hours":
                delta = timedelta(hours=interval)
                floored = now - timedelta(
                    hours=now.hour % interval,
                    minutes=now.minute,
                    seconds=now.second,
                )

            else:
                raise ValueError(f"Unsupported unit: {unit}")

            window_end = floored
            window_start = window_end - delta

            self.window_start = self.format_time(window_start)
            self.window_end = self.format_time(window_end)

        except Exception as e:
            self.false_path = NodeError.format(e)