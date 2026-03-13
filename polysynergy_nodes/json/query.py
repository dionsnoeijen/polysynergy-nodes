import jmespath
import json

from polysynergy_node_runner.setup_context.dock_property import dock_json, dock_code_editor
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings

@node(
    name="JSON Query",
    category="json",
    icon="json.svg"
)
class JsonQuery(Node):
    json_input_as_dict: dict | list = NodeVariableSettings(label="JSON Input as Dict or List", has_in=True)
    json_input_as_string: str = NodeVariableSettings(label="JSON Input as String", dock=dock_json(), has_in=True)
    query: str = NodeVariableSettings(label="JMESPath Query", dock=dock_code_editor(info="JMESPath expression for querying JSON data"), has_in=True)

    result_as_string: str = NodeVariableSettings(label="Query Result (String)", has_out=True)

    false_path: bool | dict = PathSettings(label="Error")
    true_path: bool | str | int | float | dict | list | bool = PathSettings(label="Result (str, int, float, dict, list, bool)")

    def execute(self):
        try:
            # Accept dict or list as direct input
            if isinstance(self.json_input_as_dict, (dict, list)) and self.json_input_as_dict:
                parsed_json = self.json_input_as_dict
            else:
                # Sometimes, you might have targeted a value through a placeholder
                # that contains a dict already, in that case it's fine to just
                # use it as is.
                if isinstance(self.json_input_as_string, (dict, list)):
                    parsed_json = self.json_input_as_string
                else:
                    parsed_json = json.loads(self.json_input_as_string)

            extracted_value = jmespath.search(self.query, parsed_json)

            self.result_as_string = json.dumps(extracted_value) if extracted_value is not None else "null"

            self.true_path = extracted_value

        except json.JSONDecodeError as e:
            self.false_path = NodeError.format(e)
        except Exception as e:
            self.false_path = NodeError.format(e)
