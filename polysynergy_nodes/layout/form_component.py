from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.dock_property import dock_json
from polysynergy_node_runner.setup_context.service_node import ServiceNode


@node(
    name="Form Component",
    category="layout",
    icon='layout.svg',
    version=1.0
)
class FormComponent(ServiceNode):
    """
    A form component for user input in layouts.

    Connect to a Layout node's components input.
    Define fields as a list of field configurations.
    """

    handle: str = NodeVariableSettings(
        label="Handle",
        dock=True,
        required=True,
        default="",
        info="Unique identifier used in template: {{ form('handle') }}"
    )

    action: str = NodeVariableSettings(
        label="Action URL",
        has_in=True,
        dock=True,
        required=False,
        default="",
        info="Form submission URL"
    )

    method: str = NodeVariableSettings(
        label="Method",
        dock=True,
        required=False,
        default="POST",
        info="HTTP method (GET or POST)"
    )

    fields: list = NodeVariableSettings(
        label="Fields",
        has_in=True,
        dock=dock_json(),
        required=False,
        default=[],
        info="""List of field configs: [{"name": "email", "type": "email", "label": "Email", "required": true}]"""
    )

    submit_label: str = NodeVariableSettings(
        label="Submit Button Label",
        dock=True,
        required=False,
        default="Submit",
        info="Text for the submit button"
    )

    css_class: str = NodeVariableSettings(
        label="CSS Class",
        dock=True,
        required=False,
        default="",
        info="CSS class(es) to apply to the form"
    )

    instance: "polysynergy_nodes.layout.component_node.ComponentNode" = NodeVariableSettings(
        info="Component instance for Layout node",
        has_out=True,
        type="polysynergy_nodes.layout.component_node.ComponentNode"
    )

    async def provide_instance(self) -> "FormComponent":
        return self

    def render(self) -> str:
        """Render the form to HTML."""
        class_attr = f' class="{self.css_class}"' if self.css_class else ""
        action_attr = f' action="{self.action}"' if self.action else ""

        fields_html = []
        for field in (self.fields or []):
            if not isinstance(field, dict):
                continue

            name = field.get("name", "")
            field_type = field.get("type", "text")
            label = field.get("label", name)
            required = field.get("required", False)
            placeholder = field.get("placeholder", "")
            options = field.get("options", [])

            required_attr = " required" if required else ""
            placeholder_attr = f' placeholder="{placeholder}"' if placeholder else ""

            field_html = f'<div class="form-field">\n'

            if label:
                field_html += f'    <label for="{name}">{label}</label>\n'

            if field_type == "textarea":
                field_html += f'    <textarea name="{name}" id="{name}"{placeholder_attr}{required_attr}></textarea>\n'
            elif field_type == "select":
                options_html = "".join(
                    f'<option value="{opt.get("value", opt)}">{opt.get("label", opt)}</option>'
                    for opt in options
                )
                field_html += f'    <select name="{name}" id="{name}"{required_attr}>{options_html}</select>\n'
            elif field_type == "checkbox":
                field_html += f'    <input type="checkbox" name="{name}" id="{name}"{required_attr}>\n'
            else:
                field_html += f'    <input type="{field_type}" name="{name}" id="{name}"{placeholder_attr}{required_attr}>\n'

            field_html += '</div>'
            fields_html.append(field_html)

        return f'''<form{class_attr}{action_attr} method="{self.method}">
{chr(10).join(fields_html)}
    <button type="submit">{self.submit_label}</button>
</form>'''
