import jmespath
import json
from polysynergy_nodes.base.execution_context.connection import Connection
from polysynergy_nodes.base.setup_context.dock_property import dock_dict
from polysynergy_nodes.base.setup_context.node import Node
from polysynergy_nodes.base.setup_context.node_decorator import node
from polysynergy_nodes.base.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_nodes.base.setup_context.path_settings import PathSettings


@node(
    name="JSON Switch",
    category="flow",
    icon='arrow.svg'
)
class Switch(Node):

    out_connections: list[Connection] = []

    json_as_string: str = NodeVariableSettings(label="Json As String", has_in=True, dock=True)
    json_as_dict: dict = NodeVariableSettings(label="Json As Dict", has_in=True, dock=True)
    json_path: str = NodeVariableSettings(label="Json Path", has_in=True, dock=True)

    branches: dict = NodeVariableSettings(
        label="Branches",
        dock=dock_dict(
            key_label="Branch Value Equals",
            in_switch=False,
            value_field=False,
            type_field=False,
            out_switch_default=True,
            out_switch_enabled=False,
            out_type_override="true_path,str,dict,list,int,float",
            info="Branches for the switch node",
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

    false_path: bool | dict = PathSettings(label="Error")

    def execute(self):
        value_to_check = ''

        if self.json_path:
            data = self.json_as_dict
            if not data and self.json_as_string:
                try:
                    data = json.loads(self.json_as_string)
                except Exception as e:
                    self.false_path = {"error": f"Invalid JSON string: {e}"}
                    return

            if data:
                try:
                    result = jmespath.search(self.json_path, data)
                    value_to_check = str(result) if result is not None else None
                except Exception as e:
                    self.false_path = {"error": f"JMESPath query failed: {e}"}
                    return

        if not value_to_check:
            self.false_path = {"error": "No value to switch on"}
            return

        if value_to_check in self.branches:
            for connection in self.out_connections:
                handle = connection.source_handle
                if handle.startswith("branches."):
                    handle = handle[len("branches."):]

                if handle != value_to_check:
                    connection.make_killer()
                else:
                    if data:
                        self.branches[value_to_check] = data
        else:
            for connection in self.out_connections:
                connection.make_killer()