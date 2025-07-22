from polysynergy_node_runner.setup_context.node import Node
from datetime import datetime
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="Schedule",
    category="schedule",
    icon="repeat.svg",
)
class Schedule(Node):
    schedule_name: str = NodeVariableSettings(label="Schedule Name", has_out=True)
    cron_expression: str = NodeVariableSettings(label="Cron Expression", has_out=True)
    start_time: datetime = NodeVariableSettings(label="Start Time", has_out=True)
    end_time: datetime = NodeVariableSettings(label="End Time", has_out=True)
    is_active: bool = NodeVariableSettings(label="Is Active", has_out=True)

    true_path: bool = PathSettings(default=True, label="Flow", info="The scheduled task")

    def execute(self):
        pass
