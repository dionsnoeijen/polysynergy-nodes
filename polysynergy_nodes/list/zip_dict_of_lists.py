from polysynergy_node_runner.setup_context.dock_property import dock_json, dock_dict
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="Zip Dict of Lists",
    category="list",
    icon="list.svg",
    version=1.0,
)
class ListDictToZippedObjects(Node):

    grouped_lists: dict = NodeVariableSettings(
        label="Grouped List Dict (e.g. {'a': [...], 'b': [...]})",
        dock=dock_dict(
            in_switch=False,
            in_switch_default=True,
            value_field=False,
            out_switch=False
        )
    )

    true_path: bool | list = PathSettings(label="Zipped Result")
    false_path: bool | dict = PathSettings(label="Error")

    def execute(self):
        try:
            if not isinstance(self.grouped_lists, dict):
                raise ValueError("Input must be a dictionary.")

            lengths = [len(v) for v in self.grouped_lists.values() if isinstance(v, list)]
            if len(set(lengths)) != 1:
                raise ValueError("All values must be lists of the same length.")

            keys = list(self.grouped_lists.keys())
            zipped = []
            for i in range(lengths[0]):
                item = {key: self.grouped_lists[key][i] for key in keys}
                zipped.append(item)

            self.true_path = zipped

        except Exception as e:
            self.false_path = NodeError.format(e)