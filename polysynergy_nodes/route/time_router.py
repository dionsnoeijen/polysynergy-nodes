from datetime import datetime, time
from polysynergy_node_runner.execution_context.connection import Connection
from polysynergy_node_runner.setup_context.dock_property import dock_dict
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="Time Router",
    category="route",
    icon='route.svg'
)
class TimeRouter(Node):
    out_connections: list[Connection] = []
    
    datetime_value: object = NodeVariableSettings(
        label="DateTime",
        info="DateTime object, timestamp, or ISO string to route based on time",
        has_in=True,
        dock=True,
        required=True
    )

    time_ranges: dict = NodeVariableSettings(
        label="Time Ranges",
        dock=dock_dict(
            enabled=False,
            key_label="Time Range",
            in_switch=False,
            out_switch=False,
            value_field=False,
            type_field=False,
            out_switch_default=False,
            info="Time-based routing ranges",
        ),
        default=[
            {
                "handle": "morning",
                "has_in": False,
                "has_out": True,
                "published": False,
                "type": "str",
                "value": "",
            },
            {
                "handle": "afternoon",
                "has_in": False,
                "has_out": True,
                "published": False,
                "type": "str",
                "value": "",
            },
            {
                "handle": "evening",
                "has_in": False,
                "has_out": True,
                "published": False,
                "type": "str",
                "value": "",
            },
            {
                "handle": "night",
                "has_in": False,
                "has_out": True,
                "published": False,
                "type": "str",
                "value": "",
            },
            {
                "handle": "weekday",
                "has_in": False,
                "has_out": True,
                "published": False,
                "type": "str",
                "value": "",
            },
            {
                "handle": "weekend",
                "has_in": False,
                "has_out": True,
                "published": False,
                "type": "str",
                "value": "",
            },
            {
                "handle": "default",
                "has_in": False,
                "has_out": True,
                "published": False,
                "type": "str",
                "value": "",
            }
        ]
    )

    false_path: dict = PathSettings(
        label="No Match", 
        info="Triggered when datetime is invalid and no default exists"
    )

    def execute(self):
        if not self.get_out_connections():
            self.false_path = {"error": "No output connections available"}
            return

        # Convert input to datetime object
        dt = self._parse_datetime(self.datetime_value)
        
        if dt is None:
            # Invalid datetime - check for default
            if "default" in self.time_ranges:
                for connection in self.get_out_connections():
                    handle = connection.source_handle
                    if handle.startswith("time_ranges."):
                        handle = handle[len("time_ranges."):]
                    
                    if handle != "default":
                        connection.make_killer()
                    else:
                        self.time_ranges["default"] = self.datetime_value
                return
            else:
                # No default - kill all connections and trigger false_path
                for connection in self.get_out_connections():
                    connection.make_killer()
                self.false_path = {"error": f"Invalid datetime format: {self.datetime_value}"}
                return
        
        # Determine time category
        time_category = self._get_time_category(dt)
        
        # Check which time range matches
        matched_range = None
        if time_category in self.time_ranges:
            matched_range = time_category
        elif "default" in self.time_ranges:
            matched_range = "default"
        
        if matched_range:
            # Kill connections that don't match the selected range
            for connection in self.get_out_connections():
                handle = connection.source_handle
                if handle.startswith("time_ranges."):
                    handle = handle[len("time_ranges."):]
                
                if handle != matched_range:
                    connection.make_killer()
                else:
                    # Pass the input value through the matched range
                    self.time_ranges[matched_range] = self.datetime_value
        else:
            # No match found and no default - kill all connections and trigger false_path
            for connection in self.get_out_connections():
                connection.make_killer()
            self.false_path = {"error": f"No matching time range for: {time_category}"}

    def _parse_datetime(self, value) -> datetime:
        """Parse various datetime formats into a datetime object"""
        if isinstance(value, datetime):
            return value
        elif isinstance(value, (int, float)):
            # Unix timestamp
            try:
                return datetime.fromtimestamp(value)
            except (ValueError, OSError):
                return None
        elif isinstance(value, str):
            # Try to parse ISO format string
            try:
                return datetime.fromisoformat(value.replace('Z', '+00:00'))
            except ValueError:
                # Try other common formats
                formats = [
                    "%Y-%m-%d %H:%M:%S",
                    "%Y-%m-%d",
                    "%H:%M:%S",
                    "%H:%M"
                ]
                for fmt in formats:
                    try:
                        return datetime.strptime(value, fmt)
                    except ValueError:
                        continue
                return None
        else:
            return None

    def _get_time_category(self, dt: datetime) -> str:
        """Categorize datetime into predefined time ranges"""
        hour = dt.hour
        weekday = dt.weekday()  # 0=Monday, 6=Sunday
        
        # Time of day categories
        if 5 <= hour < 12:
            time_of_day = "morning"
        elif 12 <= hour < 17:
            time_of_day = "afternoon"
        elif 17 <= hour < 21:
            time_of_day = "evening"
        else:
            time_of_day = "night"
        
        # Day of week categories
        if weekday < 5:  # Monday to Friday
            day_type = "weekday"
        else:  # Saturday and Sunday
            day_type = "weekend"
        
        # Return the most specific match available
        # Priority: time_of_day > day_type > default
        if time_of_day in self.time_ranges:
            return time_of_day
        elif day_type in self.time_ranges:
            return day_type
        else:
            return "default"