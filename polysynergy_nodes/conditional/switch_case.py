from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="Switch Case",
    category="conditional",
    icon='condition.svg'
)
class SwitchCase(Node):
    value: object = NodeVariableSettings(
        label="Value",
        info="The value to match against cases",
        has_in=True,
        required=True
    )
    
    cases: dict = NodeVariableSettings(
        label="Cases",
        info="Dictionary of case_value: result_value pairs",
        has_in=True,
        required=True
    )
    
    default_value: object = NodeVariableSettings(
        label="Default Value",
        info="Value to return if no cases match",
        has_in=True
    )

    true_path: object = PathSettings(
        label="Result",
        info="The matched case value or default"
    )
    
    false_path: dict | bool = PathSettings(
        label="Error",
        info="Error information if cases is not a dictionary"
    )

    def execute(self):
        if not isinstance(self.cases, dict):
            self.false_path = NodeError.format(ValueError("Cases must be a dictionary"))
            self.true_path = False
            return
            
        # Check if value matches any case
        if self.value in self.cases:
            self.true_path = self.cases[self.value]
        else:
            # Check for string representation match (useful for numbers, booleans)
            str_value = str(self.value)
            if str_value in self.cases:
                self.true_path = self.cases[str_value]
            else:
                # No match found, use default
                self.true_path = self.default_value