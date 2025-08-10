# UUID Nil

Generates the nil UUID (all zeros) as defined in RFC 4122.

## Inputs

No inputs required.

## Flow Control

- **True Path**: Always triggered. Contains the nil UUID string.
- **False Path**: Never triggered for valid executions.

## Behavior

- Always returns the same nil UUID: "00000000-0000-0000-0000-000000000000"
- Represents the special "null" UUID value
- Useful for initialization, default values, or placeholder scenarios
- Follows standard UUID format but with all zeros
- Consistent across all executions

## Example Usage

```
Result: "00000000-0000-0000-0000-000000000000"
```

```
Result: "00000000-0000-0000-0000-000000000000"
```

```
Result: "00000000-0000-0000-0000-000000000000"
```