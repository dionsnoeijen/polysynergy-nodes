import random
import statistics
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings, dock_property
from polysynergy_node_runner.setup_context.path_settings import PathSettings
from polysynergy_node_runner.setup_context.node_error import NodeError


@node(
    name="Random Number Range",
    category="random", 
    icon="dice.svg",
    version=1.0
)
class RandomNumberRange(Node):
    count: int = NodeVariableSettings(
        label="Count",
        default=5,
        has_in=True
    )
    
    min_value: float = NodeVariableSettings(
        label="Min Value",
        default=0,
        has_in=True
    )
    
    max_value: float = NodeVariableSettings(
        label="Max Value", 
        default=100,
        has_in=True
    )
    
    number_type: str = NodeVariableSettings(
        label="Number Type",
        dock=dock_property(
            select_values={
                "int": "Integer",
                "float": "Float"
            }
        ),
        default="int",
        has_in=True
    )
    
    unique: bool = NodeVariableSettings(
        label="Unique Values Only",
        default=False,
        has_in=True
    )
    
    decimal_places: int = NodeVariableSettings(
        label="Decimal Places (for float)",
        default=2,
        has_in=True
    )

    true_path: list = PathSettings(label="Random Numbers")
    false_path: dict = PathSettings(label="Error")

    async def execute(self):
        try:
            if self.count < 1:
                self.false_path = NodeError.format("Count must be at least 1")
                return
                
            if self.min_value >= self.max_value:
                self.false_path = NodeError.format("Min value must be less than max value")
                return

            numbers = []
            
            if self.number_type == "int":
                if self.unique:
                    # For unique integers, check if range is sufficient
                    available_values = int(self.max_value) - int(self.min_value) + 1
                    if self.count > available_values:
                        self.false_path = NodeError.format(f"Cannot generate {self.count} unique integers in range [{int(self.min_value)}, {int(self.max_value)}]")
                        return
                    
                    numbers = random.sample(
                        range(int(self.min_value), int(self.max_value) + 1), 
                        self.count
                    )
                else:
                    numbers = [
                        random.randint(int(self.min_value), int(self.max_value))
                        for _ in range(self.count)
                    ]
            else:  # float
                for _ in range(self.count):
                    if self.unique:
                        # For unique floats, keep trying until we get a new value
                        attempts = 0
                        while attempts < 1000:  # Prevent infinite loops
                            num = round(
                                random.uniform(self.min_value, self.max_value), 
                                self.decimal_places
                            )
                            if num not in numbers:
                                numbers.append(num)
                                break
                            attempts += 1
                        else:
                            self.false_path = NodeError.format("Could not generate enough unique float values")
                            return
                    else:
                        numbers.append(
                            round(random.uniform(self.min_value, self.max_value), self.decimal_places)
                        )

            self.true_path = numbers

        except Exception as e:
            self.false_path = NodeError.format(e)