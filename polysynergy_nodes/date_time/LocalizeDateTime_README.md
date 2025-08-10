# Localize DateTime

Adds timezone information to naive datetime values, converting them to timezone-aware datetimes.

## Description

The Localize DateTime node takes a naive datetime (without timezone information) and adds timezone awareness by localizing it to a specific timezone. This is essential for converting local times to timezone-aware datetimes that can be properly compared and converted between different timezones.

## Inputs

- **DateTime**: Naive datetime string to localize (required)
- **Timezone**: Timezone to apply (e.g., 'UTC', 'America/New_York', 'Europe/London') (default: UTC)
- **Output Format**: Format for the localized datetime (default: iso8601)

## Outputs

- **Localized DateTime**: The datetime with timezone information added
- **UNIX Timestamp**: Unix timestamp of the localized datetime

## Paths

- **Success**: DateTime localization completed successfully
- **Error**: Error during datetime localization (invalid timezone, parse error, etc.)

## Input Processing

- Automatically removes existing timezone information to ensure naive input
- Handles various datetime string formats
- Strips timezone suffixes like 'Z' or '+05:00' to create naive datetime
- Processes both string inputs and datetime objects

## Supported Input Formats

- **ISO 8601**: `2024-01-15T12:00:00` (timezone info removed if present)
- **Standard formats**: `2024-01-15 12:00:00`, `2024-01-15`
- **With timezone (stripped)**: `2024-01-15T12:00:00Z`, `2024-01-15T12:00:00+05:00`
- **Microseconds**: `2024-01-15T12:00:00.123456`

## Output Formats

- **iso8601**: ISO 8601 format with timezone offset
- **Custom format**: Any valid strftime format string (e.g., `%Y-%m-%d %H:%M:%S %Z`)

## Example Use Cases

- **Database storage preparation**: Localize user input before storing timezone-aware timestamps
- **API data processing**: Convert naive datetime from forms to timezone-aware format
- **Legacy system integration**: Add timezone context to datetime data from systems without timezone support
- **Time-based workflows**: Ensure all datetime values have proper timezone context
- **Scheduling systems**: Convert local appointment times to timezone-aware format

## Timezone Handling

- Uses pytz library for accurate timezone localization
- Handles daylight saving time rules automatically
- Supports all standard timezone identifiers
- Correctly applies historical timezone rules for past dates

## Common Scenarios

### Local Time to UTC
```
Input: "2024-01-15T14:30:00"
Timezone: "UTC"
Output: "2024-01-15T14:30:00+00:00"
```

### Local Time to Eastern Time
```
Input: "2024-07-15T14:30:00" 
Timezone: "America/New_York"
Output: "2024-07-15T14:30:00-04:00" (EDT)
```

### Remove and Re-add Timezone
```
Input: "2024-01-15T14:30:00+02:00"
Timezone: "Europe/London"
Output: "2024-01-15T14:30:00+00:00" (GMT)
```

## Error Handling

- Invalid timezone names trigger error path with descriptive messages
- Unparseable datetime inputs are handled gracefully
- Timezone localization errors provide detailed feedback
- Malformed input formats are detected and reported

## DST Considerations

- Automatically applies correct DST rules for the target timezone
- Handles ambiguous times during DST transitions
- Uses timezone-specific historical rules for accurate past date localization
- Future dates use current DST rules and planned transitions

## Best Practices

- Use this node before timezone conversion to ensure proper timezone awareness
- Always localize naive datetimes before storing in databases
- Combine with timezone conversion for multi-timezone applications
- Use UTC for server-side processing, local timezones for user interfaces