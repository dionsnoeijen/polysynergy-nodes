from datetime import datetime, timedelta
import re
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="Subtract Time",
    category="date_time",
    icon="time.svg"
)
class SubtractTime(Node):
    datetime_input: str = NodeVariableSettings(
        label="DateTime",
        info="DateTime string or ISO format",
        dock=True,
        has_in=True,
        required=True
    )
    
    duration: str = NodeVariableSettings(
        label="Duration",
        info="Time to subtract (e.g., '5s', '10m', '2h', '3d', '1w')",
        dock=True,
        has_in=True,
        required=True
    )
    
    format_output: str = NodeVariableSettings(
        label="Output Format",
        info="Output format string (default: ISO8601)",
        dock=True,
        has_in=True,
        default="iso8601"
    )

    result_datetime: str = NodeVariableSettings(
        label="Result DateTime",
        has_out=True
    )
    
    timestamp_output: int = NodeVariableSettings(
        label="UNIX Timestamp",
        has_out=True
    )

    true_path: str = PathSettings(
        label="Success",
        info="Time subtraction successful"
    )
    
    false_path: dict = PathSettings(
        label="Error",
        info="Error during time subtraction"
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

    def parse_duration(self, duration_str: str) -> timedelta:
        """Parse duration string like '5s', '10m', '2h', '3d', '1w'"""
        if not duration_str:
            return timedelta(0)

        # Support multiple duration parts like '1h30m', '2d5h'
        pattern = r'(\d+)([smhdw])'
        matches = re.findall(pattern, duration_str.lower().strip())
        
        if not matches:
            raise ValueError(f"Invalid duration format: {duration_str}")

        total_delta = timedelta(0)
        
        for value_str, unit in matches:
            value = int(value_str)
            
            if unit == "s":
                total_delta += timedelta(seconds=value)
            elif unit == "m":
                total_delta += timedelta(minutes=value)
            elif unit == "h":
                total_delta += timedelta(hours=value)
            elif unit == "d":
                total_delta += timedelta(days=value)
            elif unit == "w":
                total_delta += timedelta(weeks=value)
            else:
                raise ValueError(f"Unsupported duration unit: {unit}")
        
        return total_delta

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
            
            # Parse duration
            duration_delta = self.parse_duration(self.duration)
            
            # Subtract duration from datetime
            result_dt = dt - duration_delta
            
            # Format output
            self.result_datetime = self.format_datetime(result_dt)
            self.timestamp_output = int(result_dt.timestamp())
            self.true_path = self.result_datetime
            
        except Exception as e:
            self.false_path = NodeError.format(e)
            self.result_datetime = None
            self.timestamp_output = None