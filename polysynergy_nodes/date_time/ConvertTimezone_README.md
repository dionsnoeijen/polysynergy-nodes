# Convert Timezone

Converts datetime values between different timezones with support for various input formats.

## Description

The Convert Timezone node takes a datetime value and converts it from one timezone to another. It supports automatic timezone detection for timezone-aware datetimes and can localize naive datetimes to a source timezone before conversion. The node handles daylight saving time transitions automatically.

## Inputs

- **DateTime**: DateTime string, ISO format, or timestamp to convert (required)
- **From Timezone**: Source timezone (e.g., 'UTC', 'America/New_York', 'Europe/London') (default: UTC)
- **To Timezone**: Target timezone (e.g., 'UTC', 'America/New_York', 'Europe/London') (default: America/New_York)
- **Output Format**: Format for the converted datetime (default: iso8601)

## Outputs

- **Converted DateTime**: The datetime converted to the target timezone
- **UNIX Timestamp**: Unix timestamp of the converted datetime

## Paths

- **Success**: Timezone conversion completed successfully
- **Error**: Error during timezone conversion (invalid timezone, parse error, etc.)

## Supported Input Formats

- **ISO 8601**: `2024-01-15T12:00:00`, `2024-01-15T12:00:00Z`, `2024-01-15T12:00:00+05:00`
- **Standard formats**: `2024-01-15 12:00:00`, `2024-01-15`
- **Datetime objects**: Python datetime objects
- **Microseconds**: `2024-01-15T12:00:00.123456`

## Timezone Handling

- Uses pytz library for accurate timezone conversion
- Automatically handles daylight saving time transitions
- If input datetime is naive, localizes to the "From Timezone"
- If input datetime is already timezone-aware, "From Timezone" is ignored
- Supports all standard timezone names (e.g., 'UTC', 'America/New_York', 'Europe/London')

## Output Formats

- **iso8601**: ISO 8601 format with timezone offset
- **Custom format**: Any valid strftime format string

## Example Use Cases

- **API timezone normalization**: Convert user input from local timezone to UTC for storage
- **Multi-timezone applications**: Display times in user's local timezone
- **Scheduling systems**: Convert appointment times between different office locations
- **Log analysis**: Normalize timestamps from different servers in various timezones
- **International coordination**: Convert meeting times for participants in different regions

## Common Timezone Examples

- **UTC**: `UTC` - Coordinated Universal Time
- **US Timezones**: `America/New_York`, `America/Chicago`, `America/Denver`, `America/Los_Angeles`
- **European**: `Europe/London`, `Europe/Paris`, `Europe/Berlin`, `Europe/Amsterdam`
- **Asian**: `Asia/Tokyo`, `Asia/Shanghai`, `Asia/Kolkata`, `Asia/Dubai`
- **Australian**: `Australia/Sydney`, `Australia/Melbourne`

## Error Handling

- Invalid timezone names trigger error path
- Unparseable datetime inputs trigger error path
- Timezone conversion errors are handled gracefully
- Detailed error messages help diagnose issues

## DST Considerations

- Automatically handles daylight saving time transitions
- Correctly converts times during DST changeover periods
- Uses historical DST rules for accurate past date conversions
- Future DST changes are handled based on current timezone rules