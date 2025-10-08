from datetime import datetime
import locale
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="Format DateTime",
    category="datetime",
    icon="time.svg"
)
class FormatDateTime(Node):
    datetime_input: str = NodeVariableSettings(
        label="DateTime",
        info="DateTime string, ISO format, or timestamp",
        dock=True,
        has_in=True,
        required=True
    )
    
    format_string: str = NodeVariableSettings(
        label="Format String",
        info="Output format string (e.g., '%Y-%m-%d %H:%M:%S', 'iso8601')",
        dock=True,
        has_in=True,
        default="%Y-%m-%d %H:%M:%S"
    )
    
    locale_code: str = NodeVariableSettings(
        label="Locale",
        info="Locale code for formatting (e.g., 'en_US', 'de_DE', optional)",
        dock=True,
        has_in=True,
        default=""
    )

    formatted_datetime: str = NodeVariableSettings(
        label="Formatted DateTime",
        has_out=True
    )
    
    iso_format: str = NodeVariableSettings(
        label="ISO Format",
        has_out=True
    )
    
    timestamp_output: int = NodeVariableSettings(
        label="UNIX Timestamp",
        has_out=True
    )

    true_path: str = PathSettings(
        label="Success",
        info="DateTime formatting successful"
    )
    
    false_path: dict = PathSettings(
        label="Error",
        info="Error during datetime formatting"
    )

    def parse_datetime_input(self, dt_input) -> datetime:
        """Parse various datetime input formats"""
        if isinstance(dt_input, datetime):
            return dt_input
        
        # Try parsing as timestamp first
        if isinstance(dt_input, (int, float)):
            try:
                return datetime.fromtimestamp(dt_input)
            except (ValueError, OSError):
                pass
        
        # Convert to string for string parsing
        dt_str = str(dt_input)
        
        # Try parsing as timestamp string
        try:
            timestamp = float(dt_str)
            return datetime.fromtimestamp(timestamp)
        except (ValueError, OSError):
            pass
        
        # Try ISO format first
        try:
            if dt_str.endswith('Z'):
                dt_str = dt_str.replace('Z', '+00:00')
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
            "%m/%d/%Y %H:%M:%S",
            "%m/%d/%Y",
            "%d/%m/%Y %H:%M:%S", 
            "%d/%m/%Y",
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(dt_str, fmt)
            except ValueError:
                continue
                
        raise ValueError(f"Unable to parse datetime: {dt_input}")

    def set_locale(self, locale_code: str):
        """Set locale for formatting"""
        if not locale_code:
            return
            
        try:
            # Try to set the locale
            if locale_code.lower() in ['c', 'posix']:
                locale.setlocale(locale.LC_TIME, 'C')
            else:
                # Add .UTF-8 if not present
                if '.' not in locale_code:
                    locale_code += '.UTF-8'
                locale.setlocale(locale.LC_TIME, locale_code)
        except locale.Error:
            # If locale setting fails, just continue with default
            pass

    def format_datetime(self, dt: datetime) -> str:
        """Format datetime according to specified format"""
        # Handle special format cases
        format_lower = self.format_string.lower()
        
        if format_lower == "iso8601":
            return dt.isoformat()
        elif format_lower == "timestamp":
            return str(int(dt.timestamp()))
        elif format_lower == "rfc2822":
            return dt.strftime("%a, %d %b %Y %H:%M:%S %z")
        elif format_lower == "rfc3339":
            return dt.isoformat() + "Z" if dt.tzinfo is None else dt.isoformat()
        else:
            # Use custom format string
            return dt.strftime(self.format_string)

    def get_predefined_formats(self) -> dict:
        """Get common predefined format examples"""
        return {
            "iso8601": "ISO 8601 format",
            "timestamp": "Unix timestamp",
            "rfc2822": "RFC 2822 format",
            "rfc3339": "RFC 3339 format",
            "%Y-%m-%d": "Date only (YYYY-MM-DD)",
            "%Y-%m-%d %H:%M:%S": "Standard datetime",
            "%B %d, %Y": "Full month name",
            "%b %d, %Y %I:%M %p": "12-hour with AM/PM",
            "%A, %B %d, %Y": "Full day and month names",
            "%d/%m/%Y %H:%M": "European format",
            "%m/%d/%Y %I:%M %p": "US format with 12-hour time",
        }

    def execute(self):
        try:
            # Parse input datetime
            dt = self.parse_datetime_input(self.datetime_input)
            
            # Set locale if specified
            self.set_locale(self.locale_code)
            
            # Format datetime
            self.formatted_datetime = self.format_datetime(dt)
            self.iso_format = dt.isoformat()
            self.timestamp_output = int(dt.timestamp())
            
            self.true_path = self.formatted_datetime
            
        except Exception as e:
            self.false_path = NodeError.format(e)
            self.formatted_datetime = None
            self.iso_format = None
            self.timestamp_output = None