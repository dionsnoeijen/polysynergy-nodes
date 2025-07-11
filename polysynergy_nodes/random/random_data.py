import random
import uuid
from faker import Faker
from polysynergy_nodes.base.setup_context.node import Node
from polysynergy_nodes.base.setup_context.node_decorator import node
from polysynergy_nodes.base.setup_context.node_variable_settings import NodeVariableSettings, dock_property
from polysynergy_nodes.base.setup_context.path_settings import PathSettings

faker = Faker()

@node(
    name="Random Data",
    category="data",
    icon="dice.svg"
)
class RandomData(Node):
    type: str = NodeVariableSettings(
        label="Type",
        dock=dock_property(
            select_values={
                "name": "Name",
                "email": "Email",
                "uuid": "UUID",
                "text": "Text",
                "int": "Integer",
                "float": "Float",
                "date": "Date",
                "company": "Company"
            }
        ),
        default="name",
        has_in=True
    )

    min: int = NodeVariableSettings(label="Min (for numbers)", default=0, has_in=True)
    max: int = NodeVariableSettings(label="Max (for numbers)", default=100, has_in=True)

    true_path: str | int | float = PathSettings(label="Random Value")

    def execute(self):
        if self.type == "name":
            self.true_path = faker.name()
        elif self.type == "email":
            self.true_path = faker.email()
        elif self.type == "uuid":
            self.true_path = str(uuid.uuid4())
        elif self.type == "text":
            self.true_path = faker.sentence()
        elif self.type == "int":
            self.true_path = random.randint(self.min, self.max)
        elif self.type == "float":
            self.true_path = round(random.uniform(self.min, self.max), 2)
        elif self.type == "date":
            self.true_path = faker.date_time_between(start_date='-1y', end_date='now').isoformat()
        elif self.type == 'company':
            self.true_path = faker.company()
        else:
            self.true_path = f"Unsupported type: {self.type}"