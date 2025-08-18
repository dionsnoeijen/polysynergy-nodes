from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="List to Keyed Objects",
    category="list",
    icon="list.svg",
    version=1.0,
)
class ListToKeyedObjects(Node):
    """
    Transforms a simple list into a list of objects with a specified key.
    
    Example:
    Input list: ["apple", "banana", "cherry"]
    Key name: "fruit"
    Output: [{"fruit": "apple"}, {"fruit": "banana"}, {"fruit": "cherry"}]
    """

    input_list: list = NodeVariableSettings(
        label="Input List",
        dock=True,
        has_in=True,
        info="List of values to transform into keyed objects"
    )

    key_name: str = NodeVariableSettings(
        label="Key Name",
        dock=True,
        default="value",
        info="The key name to use in each object (e.g., 'fruit', 'item', 'value')"
    )

    true_path: bool | list = PathSettings(label="Transformed List")
    false_path: bool | dict = PathSettings(label="Error")

    def execute(self):
        try:
            if not isinstance(self.input_list, list):
                raise ValueError("Input must be a list")
            
            if not self.key_name or not isinstance(self.key_name, str):
                raise ValueError("Key name must be a non-empty string")
            
            # Transform each item in the list to a dictionary with the specified key
            transformed = [{self.key_name: item} for item in self.input_list]
            
            self.true_path = transformed

        except Exception as e:
            self.false_path = NodeError.format(e)