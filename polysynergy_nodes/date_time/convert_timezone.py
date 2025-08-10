from datetime import datetime
import pytz
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings, dock_property
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="Convert Timezone",
    category="date_time",
    icon="time.svg"
)
class ConvertTimezone(Node):
    datetime_input: str = NodeVariableSettings(
        label="DateTime",
        info="DateTime string or ISO format to convert",
        dock=True,
        has_in=True,
        required=True
    )
    
    from_timezone: str = NodeVariableSettings(
        label="From Timezone",
        info="Source timezone (e.g., 'UTC', 'America/New_York', 'Europe/London')",
        dock=True,
        has_in=True,
        default="UTC"
    )
    
    to_timezone: str = NodeVariableSettings(
        label="To Timezone", 
        info="Target timezone (e.g., 'UTC', 'America/New_York', 'Europe/London')",
        dock=True,
        has_in=True,
        default="America/New_York"
    )
    
    format_output: str = NodeVariableSettings(
        label="Output Format",
        info="Output format string (default: ISO8601)",
        dock=True,
        has_in=True,
        default="iso8601"
    )

    converted_datetime: str = NodeVariableSettings(
        label="Converted DateTime",
        has_out=True
    )
    
    timestamp_output: int = NodeVariableSettings(
        label="UNIX Timestamp", 
        has_out=True
    )

    true_path: str = PathSettings(
        label="Success",
        info="Timezone conversion successful"
    )
    
    false_path: dict = PathSettings(
        label="Error",
        info="Error during timezone conversion"
    )

    def parse_datetime_input(self, dt_input: str) -> datetime:
        """Parse various datetime input formats"""
        if isinstance(dt_input, datetime):
            return dt_input
        
        # Try ISO format first
        try:
            if dt_input.endswith('Z'):
                dt_input = dt_input.replace('Z', '+00:00')
            return datetime.fromisoformat(dt_input)
        except ValueError:
            pass
        
        # Try common formats
        formats = [
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M:%S.%f",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%dT%H:%M:%S.%f",
            "%Y-%m-%d",
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(dt_input, fmt)
            except ValueError:
                continue
                
        raise ValueError(f"Unable to parse datetime: {dt_input}")

    def get_timezone(self, tz_name: str):
        """Get timezone object from name"""
        try:
            return pytz.timezone(tz_name)
        except pytz.UnknownTimeZoneError:
            raise ValueError(f"Unknown timezone: {tz_name}")

    def format_datetime(self, dt: datetime) -> str:
        """Format datetime according to specified format"""
        if self.format_output.lower() == "iso8601":
            return dt.isoformat()
        else:
            return dt.strftime(self.format_output)

    def execute(self):
        try:
            # Parse input datetime
            dt = self.parse_datetime_input(self.datetime_input)
            
            # Get timezone objects
            from_tz = self.get_timezone(self.from_timezone)
            to_tz = self.get_timezone(self.to_timezone)
            
            # Localize to source timezone if naive
            if dt.tzinfo is None:
                dt = from_tz.localize(dt)
            
            # Convert to target timezone
            converted_dt = dt.astimezone(to_tz)
            
            # Format output
            self.converted_datetime = self.format_datetime(converted_dt)
            self.timestamp_output = int(converted_dt.timestamp())
            self.true_path = self.converted_datetime
            
        except Exception as e:
            self.false_path = NodeError.format(e)
            self.converted_datetime = None
            self.timestamp_output = None