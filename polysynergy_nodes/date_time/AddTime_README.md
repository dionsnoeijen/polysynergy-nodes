# Add Time

Adds a specified duration to a datetime value with support for compound duration specifications.

## Description

The Add Time node takes a datetime input and adds a specified duration to it. The duration can be specified in various units (seconds, minutes, hours, days, weeks) and supports compound durations that combine multiple units. The node handles various datetime input formats and provides flexible output formatting.

## Inputs

- **DateTime**: DateTime string, ISO format, or timestamp (required)
- **Duration**: Time duration to add (e.g., '5s', '10m', '2h', '3d', '1w') (required)
- **Output Format**: Format for the result datetime (default: iso8601)

## Outputs

- **Result DateTime**: The datetime after adding the duration
- **UNIX Timestamp**: Unix timestamp of the result datetime

## Paths

- **Success**: Time addition completed successfully
- **Error**: Error during time addition (invalid duration, parse error, etc.)

## Duration Format

### Single Units
- **s**: Seconds (e.g., '30s' = 30 seconds)
- **m**: Minutes (e.g., '45m' = 45 minutes)
- **h**: Hours (e.g., '3h' = 3 hours)
- **d**: Days (e.g., '7d' = 7 days)
- **w**: Weeks (e.g., '2w' = 2 weeks)

### Compound Durations
- **Multiple units**: '1h30m' = 1 hour and 30 minutes
- **Complex combinations**: '2d5h30m15s' = 2 days, 5 hours, 30 minutes, 15 seconds
- **Any order**: '30m1h' = 1 hour and 30 minutes

### Examples
- `'5s'` - Add 5 seconds
- `'10m'` - Add 10 minutes  
- `'2h'` - Add 2 hours
- `'7d'` - Add 7 days
- `'1w'` - Add 1 week
- `'1h30m'` - Add 1 hour and 30 minutes
- `'2d5h30m15s'` - Add 2 days, 5 hours, 30 minutes, 15 seconds

## Supported Input Formats

- **ISO 8601**: `2024-01-15T12:00:00`, `2024-01-15T12:00:00Z`
- **Standard formats**: `2024-01-15 12:00:00`, `2024-01-15`
- **With timezone**: `2024-01-15T12:00:00+05:00`
- **Microseconds**: `2024-01-15T12:00:00.123456`

## Output Formats

- **iso8601**: ISO 8601 format
- **Custom format**: Any valid strftime format string

## Example Use Cases

- **Scheduling**: Calculate future appointment times or deadline extensions
- **SLA tracking**: Add service level agreement timeframes to incident timestamps
- **Workflow automation**: Schedule follow-up tasks or reminders at specific intervals
- **Data retention**: Calculate expiration dates by adding retention periods
- **Meeting planning**: Add buffer time or duration to start times
- **Backup scheduling**: Calculate next backup time by adding intervals

## Practical Examples

### Simple Additions
```
Input: "2024-01-15T12:00:00", Duration: "30m"
Result: "2024-01-15T12:30:00"
```

### Day Boundary Crossing
```
Input: "2024-01-15T23:30:00", Duration: "1h"
Result: "2024-01-16T00:30:00"
```

### Month Boundary Crossing
```
Input: "2024-01-31T12:00:00", Duration: "5d"  
Result: "2024-02-05T12:00:00"
```

### Complex Duration
```
Input: "2024-01-15T09:00:00", Duration: "2d5h30m"
Result: "2024-01-17T14:30:00"
```

### Year Addition
```
Input: "2024-01-15T12:00:00", Duration: "365d"
Result: "2025-01-15T12:00:00" (approximately)
```

## Duration Parsing

- Case insensitive unit specification
- Flexible ordering of duration components
- Handles whitespace and formatting variations
- Empty duration results in no change to input datetime
- Invalid duration formats trigger error path with descriptive messages

## Edge Cases Handling

- **Leap years**: Properly handles February 29th when adding days
- **DST transitions**: Maintains timezone context during DST changes
- **Month boundaries**: Correctly handles months with different numbers of days
- **Large durations**: Supports adding very large time periods (years worth of days)

## Error Handling

- Invalid duration formats provide clear error messages
- Unsupported duration units are identified and reported
- Unparseable datetime inputs trigger graceful error handling
- Duration parsing errors include examples of valid formats

## Performance Considerations

- Efficient parsing of compound duration strings
- Minimal memory overhead for duration calculations
- Optimized for repeated use with different inputs
- Fast execution for both simple and complex durations