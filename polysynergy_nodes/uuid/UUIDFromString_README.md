# UUID From String

Generates a UUID from any input string using various hashing methods.

## Inputs

- **Input String** (required): The string to generate a UUID from
- **Method** (required): Hashing method ("sha1", "md5", or "truncate")
- **Namespace** (optional): Namespace for sha1/md5 methods ("DNS", "URL", "OID", "X500")

## Flow Control

- **True Path**: Triggered on successful generation. Contains the generated UUID string.
- **False Path**: Triggered on errors (e.g., invalid input or method). Contains error message.

## Behavior

- **SHA-1 Method**: Creates UUID v5 using SHA-1 hash with namespace
- **MD5 Method**: Creates UUID v3 using MD5 hash with namespace  
- **Truncate Method**: Creates UUID-like string by truncating SHA-256 hash (ignores namespace)
- Same input and method always produce the same result
- Handles Unicode strings correctly
- Different methods produce different results for same input
- Namespace affects sha1/md5 results but not truncate results

## Example Usage

```
Input String: "hello world"
Method: "sha1"
Namespace: "DNS"
Result: "2ed6657d-e927-568b-95e1-665ba9b6a5e1"
```

```
Input String: "hello world"
Method: "md5"
Namespace: "DNS"
Result: "5d41402a-bc4b-3c72-96e1-5bc862b5a4ac"
```

```
Input String: "hello world"
Method: "truncate"
Result: "b94d27b9-934d-3e08-a52e-52d7da7dabfa"
```