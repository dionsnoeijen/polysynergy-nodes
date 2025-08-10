# Default Value

Provides a fallback value when the primary value is null, empty, or undefined.

## Inputs

- **Value** (required): Primary value to use if it's not null/empty
- **Default** (required): Fallback value to use if primary value is null/empty

## Outputs

- **Result**: The chosen value (either primary or default)

## Flow Control

- **True Path**: Always triggered. Contains the chosen value (primary or default).
- **False Path**: Triggered on errors. Contains error information.

## Behavior

- Uses comprehensive null/empty checking:
  - None/null values: Use default
  - Empty strings: "" or whitespace-only strings → Use default
  - Empty collections: [], {}, (), set() → Use default
  - String literals: "null", "none", "undefined" → Use default
- Preserves valid values:
  - Number 0 is kept (not replaced with default)
  - Boolean false is kept (not replaced with default)
  - Non-empty values are kept unchanged
- Essential for providing fallback values in workflows
- Prevents null/undefined errors in downstream nodes

## Example Usage

```
Value: null, Default: "fallback"
Result: "fallback"
```

```
Value: "", Default: "default text"
Result: "default text"
```

```
Value: "primary value", Default: "fallback"
Result: "primary value"
```

```
Value: 0, Default: 42
Result: 0 (zero is kept, not replaced)
```

```
Value: false, Default: true
Result: false (false is kept, not replaced)
```