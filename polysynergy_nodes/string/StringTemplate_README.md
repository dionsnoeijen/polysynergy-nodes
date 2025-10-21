# String Template

Render a Jinja2 template with variables to generate dynamic content.

## Description

The String Template node uses Jinja2 templating engine to render templates with dynamic variables. Perfect for generating HTML, emails, XML, or any formatted text with dynamic content.

## Features

- Full Jinja2 syntax support (variables, loops, conditionals, filters)
- Code editor with HTML syntax highlighting
- Safe variable substitution
- Comprehensive error handling

## Inputs

### Template (String)
The Jinja2 template to render. Supports:
- Variables: `{{ variable_name }}`
- Conditionals: `{% if condition %}...{% endif %}`
- Loops: `{% for item in items %}...{% endfor %}`
- Filters: `{{ text|upper }}`

### Variables (Dictionary)
Dictionary of variables to use in the template.

## Outputs

### Result (String)
The rendered template with all variables substituted.

### Error (Dictionary)
Error information if rendering fails (syntax errors, undefined variables, etc.)

## Example

### HTML Card Template
```html
<div class="card">
  <h2>{{ title }}</h2>
  <img src="{{ image_url }}" alt="{{ title }}" width="300" />
  <p>{{ description }}</p>
  <ul>
  {% for feature in features %}
    <li>{{ feature }}</li>
  {% endfor %}
  </ul>
</div>
```

### Variables
```json
{
  "title": "Product Name",
  "image_url": "https://example.com/product.jpg",
  "description": "This is an amazing product!",
  "features": ["Feature 1", "Feature 2", "Feature 3"]
}
```

### Result
```html
<div class="card">
  <h2>Product Name</h2>
  <img src="https://example.com/product.jpg" alt="Product Name" width="300" />
  <p>This is an amazing product!</p>
  <ul>
    <li>Feature 1</li>
    <li>Feature 2</li>
    <li>Feature 3</li>
  </ul>
</div>
```

## Use Cases

- Generate HTML for chat interfaces
- Create email templates
- Build dynamic reports
- Generate XML/JSON with variable content
- Create formatted documents

## Jinja2 Quick Reference

### Variables
```jinja2
{{ variable_name }}
```

### Conditionals
```jinja2
{% if user.is_admin %}
  <p>Admin content</p>
{% elif user.is_moderator %}
  <p>Moderator content</p>
{% else %}
  <p>Regular content</p>
{% endif %}
```

### Loops
```jinja2
{% for item in items %}
  <li>{{ item.name }}: {{ item.price }}</li>
{% endfor %}
```

### Filters
```jinja2
{{ text|upper }}           {# UPPERCASE #}
{{ text|lower }}           {# lowercase #}
{{ text|capitalize }}      {# Capitalize #}
{{ items|length }}         {# Count items #}
{{ value|default('N/A') }} {# Default value #}
```

## Notes

- Template syntax errors will be reported with line numbers
- Undefined variables will trigger an error (use `|default()` filter for optional variables)
- All Jinja2 built-in filters and functions are available
