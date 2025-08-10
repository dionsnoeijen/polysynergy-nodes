# Pattern Router

Routes string values based on regular expression pattern matching to different output paths.

## Description

The Pattern Router node matches input strings against regular expression patterns and routes them to corresponding output connections. This enables sophisticated string-based routing using the full power of regex pattern matching.

## Inputs

- **Value**: The string value to match against patterns (required, automatically converted to string)

## Outputs

Dynamic output connections based on regex patterns:

- **Pattern outputs**: Each regex pattern creates a corresponding output connection
- **default**: Fallback route for non-matching patterns

## Paths

- **No Match**: Triggered when no patterns match and no default exists

## Pattern Matching

- Uses Python's `re.match()` function for pattern matching
- Patterns are evaluated from the beginning of the string
- First matching pattern determines the routing
- Invalid regex patterns are ignored and don't match

## Behavior

1. Converts input value to string if not already a string
2. Evaluates string against each regex pattern in order
3. Routes to the first matching pattern output
4. If no patterns match, uses "default" route or triggers false path
5. Kills all non-matching output connections
6. Passes the original input value through the selected route

## Example Use Cases

- **Email validation and routing**: Route emails vs non-emails using `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`
- **URL categorization**: Route HTTP vs HTTPS URLs using `^https?://.*`
- **Phone number formats**: Route different phone formats using `^\d{3}-\d{3}-\d{4}$`
- **File type routing**: Route files by extension using `.*\.(jpg|png|gif)$`
- **User input classification**: Route commands vs queries using `^(get|list|show).*`
- **Content filtering**: Route messages containing specific keywords using `.*(urgent|important).*`

## Common Patterns

- **Email**: `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`
- **Phone (US)**: `^\d{3}-\d{3}-\d{4}$`
- **URL**: `^https?://.*`
- **Alphanumeric**: `^[a-zA-Z0-9]+$`
- **Numbers only**: `^\d+$`
- **Starts with**: `^hello.*`
- **Contains**: `.*keyword.*`
- **Case insensitive**: Use `(?i)pattern` for case-insensitive matching

## Pattern Tips

- Use `^` to match from the beginning of the string
- Use `$` to match to the end of the string
- Use `.*` to match any characters
- Use `\d` for digits, `\w` for word characters, `\s` for whitespace
- Escape special characters with backslash: `\.`, `\+`, `\?`
- Test patterns before deployment to ensure they match as expected