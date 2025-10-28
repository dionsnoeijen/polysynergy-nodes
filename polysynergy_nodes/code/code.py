from polysynergy_node_runner.setup_context.dock_property import dock_dict, dock_code_editor
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(name="Code", category="code", version=1.0)
class Code(Node):
    arguments: dict | None = NodeVariableSettings(
        label="Arguments",
        dock=dock_dict(
            key_label="Argument Name",
            value_label="Value (connect input)",
            info="Arguments available as variables in code scope"
        ),
        has_in=True,
        info="Arguments passed to code execution as local variables"
    )

    code: str = NodeVariableSettings(
        label="Code",
        dock=dock_code_editor(metadata={"language": "python"}),
        info="Python code to execute. Use 'return' to output a value. Supports async/await."
    )

    true_path: any = PathSettings(
        label="Result",
        info="Return value from code execution"
    )

    false_path: dict = PathSettings(
        label="Error",
        info="Exception details if execution fails"
    )

    async def execute(self):
        try:
            # Build execution scope with arguments as variables
            scope = {"__builtins__": __builtins__}

            if self.arguments and isinstance(self.arguments, dict):
                # Parse argument values: try JSON parsing for strings to convert types
                # "10" → 10, "true" → True, "[1,2,3]" → [1,2,3], "hello" → "hello"
                import json
                parsed_args = {}
                for key, value in self.arguments.items():
                    if isinstance(value, str):
                        try:
                            # Try to parse as JSON for automatic type conversion
                            parsed_args[key] = json.loads(value)
                        except (json.JSONDecodeError, ValueError):
                            # Not valid JSON, keep as string
                            parsed_args[key] = value
                    else:
                        # Already correct type (from connected nodes), keep as-is
                        parsed_args[key] = value

                scope.update(parsed_args)

            # Wrap user code in async function to support await
            wrapped_code = "async def __user_code():\n"
            for line in self.code.split("\n"):
                wrapped_code += f"    {line}\n"

            # Define the function in scope
            exec(wrapped_code, scope)

            # Execute and get result
            result = await scope['__user_code']()

            self.true_path = result
            self.false_path = False
            return result

        except Exception as e:
            self.false_path = {
                'error': str(e),
                'type': type(e).__name__
            }
            self.true_path = False
            return None
