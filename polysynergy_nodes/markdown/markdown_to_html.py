from polysynergy_nodes import markdown
from polysynergy_nodes.base.setup_context.node import Node
from polysynergy_nodes.base.setup_context.node_decorator import node
from polysynergy_nodes.base.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_nodes.base.setup_context.path_settings import PathSettings
from polysynergy_nodes.base.setup_context.node_error import NodeError


@node(
    name="Markdown to HTML",
    category="utils",
    icon="markdown.svg"
)
class MarkdownToHtml(Node):

    markdown_input: str = NodeVariableSettings(
        label="Markdown Input",
        has_in=True,
        required=True,
        info="The raw markdown string to convert to HTML."
    )

    true_path: bool | str | None = PathSettings(
        label="HTML Output",
        info="HTML result of the markdown conversion."
    )

    false_path: bool | dict | None = PathSettings(
        label="Error",
        info="Triggered if markdown conversion fails."
    )

    async def execute(self):
        try:
            html = markdown.markdown(self.markdown_input, extensions=["extra", "smarty"])
            self.true_path = html
        except Exception as e:
            self.false_path = NodeError.format(e)