from datetime import datetime
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="Date Difference",
    category="date_time",
    icon="time.svg"
)
class DateDifference(Node):
    start_datetime: str = NodeVariableSettings(
        label="Start DateTime",
        info="Start datetime string or ISO format",
        dock=True,
        has_in=True,
        required=True
    )
    
    end_datetime: str = NodeVariableSettings(
        label="End DateTime",
        info="End datetime string or ISO format",
        dock=True,
        has_in=True,
        required=True
    )

    total_seconds: float = NodeVariableSettings(
        label="Total Seconds",
        has_out=True
    )
    
    total_minutes: float = NodeVariableSettings(
        label="Total Minutes",
        has_out=True
    )
    
    total_hours: float = NodeVariableSettings(
        label="Total Hours",
        has_out=True
    )
    
    total_days: float = NodeVariableSettings(
        label="Total Days",
        has_out=True
    )
    
    absolute_difference: float = NodeVariableSettings(
        label="Absolute Difference (seconds)",
        has_out=True
    )
    
    human_readable: str = NodeVariableSettings(
        label="Human Readable",
        has_out=True
    )

    true_path: str = PathSettings(
        label="Success",
        info="Date difference calculation successful"
    )
    
    false_path: dict = PathSettings(
        label="Error",
        info="Error during date difference calculation"
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

    def format_human_readable(self, seconds: float) -> str:
        """Format seconds into human-readable format"""
        abs_seconds = abs(seconds)
        
        if abs_seconds < 60:
            return f"{abs_seconds:.1f} seconds"
        elif abs_seconds < 3600:  # Less than 1 hour
            minutes = abs_seconds / 60
            return f"{minutes:.1f} minutes"
        elif abs_seconds < 86400:  # Less than 1 day
            hours = abs_seconds / 3600
            return f"{hours:.1f} hours"
        else:  # 1 day or more
            days = abs_seconds / 86400
            return f"{days:.1f} days"

    def execute(self):
        try:
            # Parse input datetimes
            start_dt = self.parse_datetime_input(self.start_datetime)
            end_dt = self.parse_datetime_input(self.end_datetime)
            
            # Calculate difference (end - start)
            diff = end_dt - start_dt
            total_seconds_value = diff.total_seconds()
            
            # Calculate various time units
            self.total_seconds = total_seconds_value
            self.total_minutes = total_seconds_value / 60
            self.total_hours = total_seconds_value / 3600
            self.total_days = total_seconds_value / 86400
            self.absolute_difference = abs(total_seconds_value)
            
            # Generate human-readable format
            if total_seconds_value >= 0:
                self.human_readable = self.format_human_readable(total_seconds_value)
            else:
                self.human_readable = f"-{self.format_human_readable(total_seconds_value)}"
            
            self.true_path = f"Difference: {self.human_readable}"
            
        except Exception as e:
            self.false_path = NodeError.format(e)
            self.total_seconds = None
            self.total_minutes = None
            self.total_hours = None
            self.total_days = None
            self.absolute_difference = None
            self.human_readable = None