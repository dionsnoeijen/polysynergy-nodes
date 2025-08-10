# Expression Evaluator

Evaluates complex boolean expressions with support for logical operators, comparisons, and parentheses.

## Inputs

- **Variables A-H**: Dynamic input variables (a, b, c, d, e, f, g, h)
- **Expression** (required): Boolean expression to evaluate using variables

## Flow Control

- **True Path**: Triggered when expression evaluates to true. Contains boolean true.
- **False Path**: Triggered when expression evaluates to false, or on error. Contains boolean false or error message.

## Behavior

- Supports comparison operators: `>`, `<`, `>=`, `<=`, `==`, `!=`
- Supports logical operators: `&&` (AND), `||` (OR), `!` (NOT)
- Supports parentheses for grouping: `()`
- Supports numeric literals in expressions
- Automatic type coercion for strings to numbers/booleans
- Proper operator precedence: `!` > `&&` > `||`
- Variables must be connected (non-null) to be used in expressions
- Throws error for undefined variables or invalid syntax

## Expression Syntax

Variables are referenced by their lowercase names (a, b, c, etc.)
Numbers can be used directly: `a > 10`
Strings are compared as-is or coerced to numbers when possible

## Example Usage

```
Variables: a = 10, b = 5
Expression: "a > b"
Result: true
```

```
Variables: a = 5, b = 25
Expression: "(a > b) || (b > 20)"
Result: true (second condition is true)
```

```
Variables: a = 10, b = 5, c = 20, d = 15
Expression: "((a > b) && (c > d)) || (b < 3)"
Result: true ((true && true) || false = true)
```

```
Variables: a = "hello", b = "world"
Expression: "a != b"
Result: true
```