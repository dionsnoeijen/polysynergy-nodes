import re
from polysynergy_node_runner.setup_context.dock_property import dock_text_area, dock_select_values
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="String Regex",
    category="string",
    icon='string.svg',
    version=1.0
)
class StringRegex(Node):
    text: str = NodeVariableSettings(
        label="Text",
        dock=dock_text_area(),
        has_in=True,
        required=True
    )
    
    pattern: str = NodeVariableSettings(
        label="Pattern",
        dock=dock_text_area(),
        has_in=True,
        required=True,
        info="Regular expression pattern"
    )
    
    operation: str = NodeVariableSettings(
        label="Operation",
        dock=dock_select_values({
            "match": "Match (full match)",
            "search": "Search (find first)",
            "findall": "Find All",
            "split": "Split",
            "replace": "Replace"
        }),
        default="search",
        has_in=True
    )
    
    replacement: str = NodeVariableSettings(
        label="Replacement",
        dock=dock_text_area(),
        has_in=True,
        default="",
        info="Replacement string (for replace operation)"
    )
    
    flags: str = NodeVariableSettings(
        label="Flags",
        dock=dock_select_values({
            "none": "None",
            "ignorecase": "Ignore Case",
            "multiline": "Multiline",
            "dotall": "Dot All",
            "ignorecase_multiline": "Ignore Case + Multiline"
        }),
        default="none",
        has_in=True
    )

    true_path: str | list | bool = PathSettings(
        label="Result",
        info="Match result (varies by operation)"
    )
    
    false_path: dict | bool = PathSettings(
        label="Error",
        info="Error information if regex fails"
    )

    def _get_flags(self):
        """Convert flag string to re flags."""
        flag_map = {
            "none": 0,
            "ignorecase": re.IGNORECASE,
            "multiline": re.MULTILINE,
            "dotall": re.DOTALL,
            "ignorecase_multiline": re.IGNORECASE | re.MULTILINE
        }
        return flag_map.get(self.flags, 0)

    async def execute(self):
        if not isinstance(self.text, str):
            self.false_path = NodeError.format(ValueError("Text must be a string"))
            self.true_path = False
            return
            
        if not isinstance(self.pattern, str):
            self.false_path = NodeError.format(ValueError("Pattern must be a string"))
            self.true_path = False
            return
            
        try:
            flags = self._get_flags()
            compiled_pattern = re.compile(self.pattern, flags)
            
            if self.operation == "match":
                match = compiled_pattern.match(self.text)
                self.true_path = match is not None
                
            elif self.operation == "search":
                match = compiled_pattern.search(self.text)
                if match:
                    self.true_path = match.group(0)
                else:
                    self.true_path = None
                    
            elif self.operation == "findall":
                self.true_path = compiled_pattern.findall(self.text)
                
            elif self.operation == "split":
                self.true_path = compiled_pattern.split(self.text)
                
            elif self.operation == "replace":
                self.true_path = compiled_pattern.sub(self.replacement, self.text)
                
            else:
                self.false_path = NodeError.format(ValueError(f"Invalid operation: {self.operation}"))
                self.true_path = False
                return
            
            self.false_path = False
        except re.error as e:
            self.false_path = NodeError.format(f"Regex error: {str(e)}")
            self.true_path = False
        except Exception as e:
            self.false_path = NodeError.format(e)
            self.true_path = False