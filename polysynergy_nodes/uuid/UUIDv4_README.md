# UUID v4

Generates a random UUID (version 4) using cryptographically secure random numbers.

## Inputs

No inputs required.

## Flow Control

- **True Path**: Always triggered. Contains the generated UUID string.
- **False Path**: Never triggered for valid executions.

## Behavior

- Generates a new random UUID v4 each time it executes
- Uses the standard UUID format: 8-4-4-4-12 hexadecimal characters
- Guarantees uniqueness with extremely low collision probability
- Returns UUID in lowercase format

## Example Usage

```
Result: "f47ac10b-58cc-4372-a567-0e02b2c3d479"
```

```
Result: "6ba7b810-9dad-11d1-80b4-00c04fd430c8"
```

```
Result: "550e8400-e29b-41d4-a716-446655440000"
```