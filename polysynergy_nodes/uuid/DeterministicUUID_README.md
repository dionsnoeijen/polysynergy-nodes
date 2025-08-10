# Deterministic UUID

Generates a deterministic UUID (version 5) from an input string using SHA-1 hashing with a namespace.

## Inputs

- **Input String** (required): The string to generate a UUID from
- **Namespace** (required): The namespace to use ("DNS", "URL", "OID", or "X500")

## Flow Control

- **True Path**: Triggered on successful generation. Contains the generated UUID string.
- **False Path**: Triggered on errors (e.g., non-string input). Contains error message.

## Behavior

- Same input string and namespace always generate the same UUID
- Uses SHA-1 hashing algorithm internally
- Namespace affects the generated UUID (different namespaces produce different UUIDs)
- Namespace is case-insensitive
- Invalid namespaces default to "DNS"
- Handles Unicode strings correctly

## Example Usage

```
Input String: "example.com"
Namespace: "DNS"
Result: "cfbff0d1-9375-5685-968c-48ce8b15ae17"
```

```
Input String: "example.com"
Namespace: "URL"
Result: "21f7f8de-8051-5b89-8680-0195ef798b6a"
```

```
Input String: "hello world"
Namespace: "DNS"
Result: "2ed6657d-e927-568b-95e1-665ba9b6a5e1"
```