from polysynergy_node_runner.execution_context.connection import Connection
from polysynergy_node_runner.setup_context.dock_property import dock_dict
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="List Contains Router",
    category="route",
    icon='route.svg'
)
class ListContainsRouter(Node):
    out_connections: list[Connection] = []
    
    value: object = NodeVariableSettings(
        label="Value",
        info="The value to check if it exists in lists",
        has_in=True,
        dock=True,
        required=True
    )

    lists: dict = NodeVariableSettings(
        label="Lists",
        dock=dock_dict(
            key_label="List Name",
            in_switch=True,
            value_field=True,
            type_field=False,
            out_switch_default=True,
            out_switch_enabled=False,
            info="Lists to check for value containment - provide list values as input",
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
        info="Triggered when value is not found in any list and no default exists"
    )

    def execute(self):
        if not self.get_out_connections():
            self.false_path = {"error": "No output connections available"}
            return

        # Check which list contains the value
        matched_list = None
        for list_key, list_value in self.lists.items():
            if list_key == "default":
                continue
                
            if self._value_in_list(self.value, list_value):
                matched_list = list_key
                break
        
        # If no match, try default
        if matched_list is None and "default" in self.lists:
            matched_list = "default"
        
        if matched_list:
            # Kill connections that don't match the selected list
            for connection in self.get_out_connections():
                handle = connection.source_handle
                if handle.startswith("lists."):
                    handle = handle[len("lists."):]
                
                if handle != matched_list:
                    connection.make_killer()
                else:
                    # Pass the input value through the matched list
                    self.lists[matched_list] = self.value
        else:
            # No match found and no default - kill all connections and trigger false_path
            for connection in self.get_out_connections():
                connection.make_killer()
            self.false_path = {"error": f"Value not found in any list: {self.value}"}

    def _value_in_list(self, value, list_value) -> bool:
        """Check if a value exists in a list"""
        if not isinstance(list_value, list):
            return False
        
        try:
            return value in list_value
        except TypeError:
            # Handle unhashable types by using string comparison
            str_value = str(value)
            return str_value in [str(item) for item in list_value]