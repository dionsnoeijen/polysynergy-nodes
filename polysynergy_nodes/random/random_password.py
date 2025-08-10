import random
import string
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings
from polysynergy_node_runner.setup_context.node_error import NodeError


@node(
    name="Random Password",
    category="random",
    icon="dice.svg",
    version=1.0
)
class RandomPassword(Node):
    length: int = NodeVariableSettings(
        label="Length",
        default=12,
        has_in=True
    )
    
    include_uppercase: bool = NodeVariableSettings(
        label="Include Uppercase",
        default=True,
        has_in=True
    )
    
    include_lowercase: bool = NodeVariableSettings(
        label="Include Lowercase", 
        default=True,
        has_in=True
    )
    
    include_numbers: bool = NodeVariableSettings(
        label="Include Numbers",
        default=True,
        has_in=True
    )
    
    include_symbols: bool = NodeVariableSettings(
        label="Include Symbols",
        default=True,
        has_in=True
    )
    
    exclude_ambiguous: bool = NodeVariableSettings(
        label="Exclude Ambiguous Characters",
        default=False,
        has_in=True
    )

    true_path: str = PathSettings(label="Random Password")
    false_path: dict = PathSettings(label="Error")

    async def execute(self):
        try:
            if self.length < 1:
                self.false_path = NodeError.format("Password length must be at least 1")
                return

            # Build character set
            characters = ""
            
            if self.include_lowercase:
                chars = string.ascii_lowercase
                if self.exclude_ambiguous:
                    chars = chars.replace('l', '').replace('o', '')
                characters += chars
                
            if self.include_uppercase:
                chars = string.ascii_uppercase
                if self.exclude_ambiguous:
                    chars = chars.replace('I', '').replace('O', '')
                characters += chars
                
            if self.include_numbers:
                chars = string.digits
                if self.exclude_ambiguous:
                    chars = chars.replace('0', '').replace('1', '')
                characters += chars
                
            if self.include_symbols:
                chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
                characters += chars

            if not characters:
                self.false_path = NodeError.format("At least one character type must be selected")
                return

            # Generate password
            password = ''.join(random.choice(characters) for _ in range(self.length))
            self.true_path = password

        except Exception as e:
            self.false_path = NodeError.format(e)