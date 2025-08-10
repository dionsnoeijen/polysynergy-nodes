# UUID Validate

Validates a UUID string and optionally checks its version.

## Inputs

- **UUID String** (required): The UUID string to validate
- **Check Version** (optional): Specific version to check for (0 = any version)

## Flow Control

- **True Path**: Triggered when UUID is valid (and matches version if specified). Contains boolean true.
- **False Path**: Triggered when UUID is invalid or doesn't match expected version. Contains boolean false or error message.

## Outputs

- **Version**: The detected version of the UUID (1, 3, 4, 5, or 0 for nil UUID)

## Behavior

- Validates UUID format (8-4-4-4-12 hexadecimal pattern)
- Detects and returns UUID version
- Supports uppercase and lowercase UUIDs
- Can validate any UUID version or check for specific version
- Handles nil UUID (all zeros) correctly
- Returns detailed error messages for invalid inputs

## Example Usage

```
UUID String: "f47ac10b-58cc-4372-a567-0e02b2c3d479"
Check Version: 0
Result: true, Version: 4
```

```
UUID String: "6ba7b810-9dad-11d1-80b4-00c04fd430c8"
Check Version: 1
Result: true, Version: 1
```

```
UUID String: "not-a-uuid"
Check Version: 0
Result: false, Version: 0
```