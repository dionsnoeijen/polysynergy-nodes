# Variable Rich Text

Stores and processes rich text/HTML content with placeholder replacement support.

## Inputs

- **Value** (required): Rich text or HTML string to process
- **Values** (optional): Dictionary of placeholder values

## Flow Control

- **True Path**: Triggered on successful processing. Contains the processed rich text.
- **False Path**: Triggered on errors. Contains error information.

## Behavior

- Designed for rich text editors with HTML content
- Supports Jinja2 placeholder replacement ({{ variable }})
- Validates that input value is a string
- Handles complex HTML structures with embedded variables
- Provides detailed error messages for missing placeholders
- Preserves HTML formatting and structure

## Example Usage

```
Value: "<p>Hello World!</p>"
Result: "<p>Hello World!</p>"
```

```
Value: "<h1>Welcome {{ username }}!</h1>"
Values: {"username": "Alice"}
Result: "<h1>Welcome Alice!</h1>"
```

```
Value: "<div><p>Hello {{ name }}!</p><p>You have {{ count }} messages.</p></div>"
Values: {"name": "John", "count": "5"}
Result: "<div><p>Hello John!</p><p>You have 5 messages.</p></div>"
```

```
Value: "<ul><li>Item {{ id }}</li></ul>"
Values: {}
Result: Error - 'id' is undefined
```