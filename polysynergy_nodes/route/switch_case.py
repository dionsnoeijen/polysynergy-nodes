from polysynergy_node_runner.execution_context.connection import Connection
from polysynergy_node_runner.setup_context.dock_property import dock_dict
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="Switch Case",
    category="route",
    icon='route.svg'
)
class SwitchCase(Node):
    out_connections: list[Connection] = []
    
    value: object = NodeVariableSettings(
        label="Value",
        info="The value to match against case keys",
        has_in=True,
        dock=True,
        required=True
    )

    cases: dict = NodeVariableSettings(
        label="Cases",
        dock=dock_dict(
            key_label="Case Value",
            in_switch=False,
            value_field=False,
            type_field=False,
            out_switch_default=True,
            out_switch_enabled=False,
            info="Cases for routing - keys are matched against input value",
        ),
        default=[{
            "type": "str",
            "value": "",
            "handle": "default",
            "has_in": False,
            "has_out": True,
            "published": False
        }]
    )

    false_path: dict = PathSettings(
        label="No Match", 
        info="Triggered when no cases match and no default exists"
    )

    def execute(self):
        if not self.out_connections:
            self.false_path = {"error": "No output connections available"}
            return

        # Convert input value to string for comparison
        str_value = str(self.value)
        
        # Check if value matches any case key
        matched_case = None
        if str_value in self.cases:
            matched_case = str_value
        else:
            # Check if "default" case exists
            if "default" in self.cases:
                matched_case = "default"
        
        if matched_case:
            # Kill connections that don't match the selected case
            for connection in self.out_connections:
                handle = connection.source_handle
                if handle.startswith("cases."):
                    handle = handle[len("cases."):]
                
                if handle != matched_case:
                    connection.make_killer()
                else:
                    # Pass the input value through the matched case
                    self.cases[matched_case] = self.value
        else:
            # No match found and no default - kill all connections and trigger false_path
            for connection in self.out_connections:
                connection.make_killer()
            self.false_path = {"error": f"No matching case for value: {self.value}"}