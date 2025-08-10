# Delay

Pauses execution for a specified number of seconds, then passes the input value through.

## Inputs

- **Seconds** (required): Number of seconds to wait (default: 1.0)
- **Value** (optional): Value to pass through after the delay

## Outputs

- **Result**: The input value after the delay completes

## Flow Control

- **True Path**: Triggered after the delay completes. Contains the input value.
- **False Path**: Triggered on errors (e.g., invalid seconds value). Contains error information.

## Behavior

- Pauses execution using async/await for the specified time
- Accepts seconds as integer, float, or string (converts automatically)
- Safety limits: Negative values become 0, maximum delay is 300 seconds (5 minutes)
- Passes through the input value unchanged after delay
- Non-blocking for other parts of the system (uses async sleep)
- Useful for rate limiting, timing delays, or testing workflows
- Maintains data flow while adding time delays

## Example Usage

```
Seconds: 2.5, Value: "hello"
Result: "hello" (after 2.5 second delay)
```

```
Seconds: 1, Value: [1, 2, 3]
Result: [1, 2, 3] (after 1 second delay)
```

```
Seconds: 0, Value: "instant"
Result: "instant" (no delay)
```

```
Seconds: "1.5", Value: 42
Result: 42 (after 1.5 second delay, string converted to float)
```