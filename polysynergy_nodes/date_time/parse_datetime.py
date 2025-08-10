from datetime import datetime
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="Parse DateTime",
    category="date_time",
    icon="time.svg"
)
class ParseDateTime(Node):
    datetime_string: str = NodeVariableSettings(
        label="DateTime String",
        info="String to parse into datetime",
        dock=True,
        has_in=True,
        required=True
    )
    
    format_string: str = NodeVariableSettings(
        label="Format String",
        info="Custom format string (optional, auto-detect if empty)",
        dock=True,
        has_in=True,
        default=""
    )
    
    output_format: str = NodeVariableSettings(
        label="Output Format",
        info="Output format string (default: ISO8601)",
        dock=True,
        has_in=True,
        default="iso8601"
    )

    parsed_datetime: str = NodeVariableSettings(
        label="Parsed DateTime",
        has_out=True
    )
    
    timestamp_output: int = NodeVariableSettings(
        label="UNIX Timestamp",
        has_out=True
    )
    
    year: int = NodeVariableSettings(
        label="Year",
        has_out=True
    )
    
    month: int = NodeVariableSettings(
        label="Month",
        has_out=True
    )
    
    day: int = NodeVariableSettings(
        label="Day",
        has_out=True
    )
    
    hour: int = NodeVariableSettings(
        label="Hour",
        has_out=True
    )
    
    minute: int = NodeVariableSettings(
        label="Minute",
        has_out=True
    )
    
    second: int = NodeVariableSettings(
        label="Second",
        has_out=True
    )

    true_path: str = PathSettings(
        label="Success",
        info="DateTime parsing successful"
    )
    
    false_path: dict = PathSettings(
        label="Error",
        info="Error during datetime parsing"
    )

    def auto_parse_datetime(self, dt_string: str) -> datetime:
        """Auto-detect and parse various datetime formats"""
        # Remove common timezone indicators for parsing
        clean_string = dt_string.strip()
        
        # Handle ISO format with Z
        if clean_string.endswith('Z'):
            clean_string = clean_string.replace('Z', '+00:00')
        
        # Try ISO format first
        try:
            return datetime.fromisoformat(clean_string)
        except ValueError:
            pass
        
        # Common datetime formats to try
        formats = [
            # ISO variants
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%dT%H:%M:%S.%f",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M:%S.%f",
            
            # US formats
            "%m/%d/%Y %H:%M:%S",
            "%m/%d/%Y %I:%M:%S %p",
            "%m/%d/%Y",
            
            # European formats
            "%d/%m/%Y %H:%M:%S",
            "%d/%m/%Y",
            "%d-%m-%Y %H:%M:%S",
            "%d-%m-%Y",
            
            # Other common formats
            "%Y-%m-%d",
            "%B %d, %Y",
            "%b %d, %Y",
            "%d %B %Y",
            "%d %b %Y",
            
            # Time only formats
            "%H:%M:%S",
            "%H:%M",
            "%I:%M:%S %p",
            "%I:%M %p",
            
            # Timestamp formats
            "%Y%m%d",
            "%Y%m%d%H%M%S",
        ]
        
        # Try each format
        for fmt in formats:
            try:
                return datetime.strptime(clean_string, fmt)
            except ValueError:
                continue
        
        # Try parsing as timestamp (Unix timestamp)
        try:
            timestamp = float(clean_string)
            return datetime.fromtimestamp(timestamp)
        except (ValueError, OSError):
            pass
        
        raise ValueError(f"Unable to parse datetime string: {dt_string}")

    def parse_with_format(self, dt_string: str, format_str: str) -> datetime:
        """Parse datetime using specific format string"""
        try:
            return datetime.strptime(dt_string, format_str)
        except ValueError as e:
            raise ValueError(f"Unable to parse '{dt_string}' with format '{format_str}': {e}")

    def format_datetime(self, dt: datetime) -> str:
        """Format datetime according to specified format"""
        if self.output_format.lower() == "iso8601":
            return dt.isoformat()
        else:
            return dt.strftime(self.output_format)

    def execute(self):
        try:
            # Parse datetime using custom format or auto-detection
            if self.format_string:
                parsed_dt = self.parse_with_format(self.datetime_string, self.format_string)
            else:
                parsed_dt = self.auto_parse_datetime(self.datetime_string)
            
            # Format output
            self.parsed_datetime = self.format_datetime(parsed_dt)
            self.timestamp_output = int(parsed_dt.timestamp())
            
            # Extract date/time components
            self.year = parsed_dt.year
            self.month = parsed_dt.month
            self.day = parsed_dt.day
            self.hour = parsed_dt.hour
            self.minute = parsed_dt.minute
            self.second = parsed_dt.second
            
            self.true_path = self.parsed_datetime
            
        except Exception as e:
            self.false_path = NodeError.format(e)
            self.parsed_datetime = None
            self.timestamp_output = None
            self.year = None
            self.month = None
            self.day = None
            self.hour = None
            self.minute = None
            self.second = None