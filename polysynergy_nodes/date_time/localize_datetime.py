from datetime import datetime
import pytz
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="Localize DateTime",
    category="date_time",
    icon="time.svg"
)
class LocalizeDateTime(Node):
    datetime_input: str = NodeVariableSettings(
        label="DateTime",
        info="Naive datetime string to localize",
        dock=True,
        has_in=True,
        required=True
    )
    
    timezone: str = NodeVariableSettings(
        label="Timezone",
        info="Timezone to apply (e.g., 'UTC', 'America/New_York', 'Europe/London')",
        dock=True,
        has_in=True,
        default="UTC"
    )
    
    format_output: str = NodeVariableSettings(
        label="Output Format",
        info="Output format string (default: ISO8601)",
        dock=True,
        has_in=True,
        default="iso8601"
    )

    localized_datetime: str = NodeVariableSettings(
        label="Localized DateTime",
        has_out=True
    )
    
    timestamp_output: int = NodeVariableSettings(
        label="UNIX Timestamp",
        has_out=True
    )

    true_path: str = PathSettings(
        label="Success",
        info="DateTime localization successful"
    )
    
    false_path: dict = PathSettings(
        label="Error",
        info="Error during datetime localization"
    )

    def parse_datetime_input(self, dt_input: str) -> datetime:
        """Parse various datetime input formats as naive datetime"""
        if isinstance(dt_input, datetime):
            # Remove timezone info if present to make it naive
            return dt_input.replace(tzinfo=None)
        
        # Remove timezone info from string if present
        dt_str = dt_input
        if dt_str.endswith('Z'):
            dt_str = dt_str[:-1]
        elif '+' in dt_str:
            dt_str = dt_str.split('+')[0]
        elif dt_str.count('-') > 2:  # Has timezone offset
            parts = dt_str.split('-')
            if len(parts) > 3:
                dt_str = '-'.join(parts[:3])
        
        # Try ISO format first
        try:
            return datetime.fromisoformat(dt_str)
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
                return datetime.strptime(dt_str, fmt)
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
            # Parse input datetime as naive
            naive_dt = self.parse_datetime_input(self.datetime_input)
            
            # Get timezone object
            tz = self.get_timezone(self.timezone)
            
            # Localize naive datetime
            localized_dt = tz.localize(naive_dt)
            
            # Format output
            self.localized_datetime = self.format_datetime(localized_dt)
            self.timestamp_output = int(localized_dt.timestamp())
            self.true_path = self.localized_datetime
            
        except Exception as e:
            self.false_path = NodeError.format(e)
            self.localized_datetime = None
            self.timestamp_output = None