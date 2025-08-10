# Format DateTime

Formats datetime values into custom string representations with support for various input types, locale settings, and predefined formats.

## Description

The Format DateTime node converts datetime values into formatted strings using custom format specifications. It supports multiple input types (strings, timestamps, datetime objects), locale-specific formatting, and includes several predefined formats for common use cases. The node is essential for displaying datetime values in user-friendly formats.

## Inputs

- **DateTime**: DateTime string, ISO format, timestamp, or datetime object (required)
- **Format String**: Output format specification (default: %Y-%m-%d %H:%M:%S)
- **Locale**: Locale code for formatting (optional, e.g., 'en_US', 'de_DE')

## Outputs

- **Formatted DateTime**: The datetime formatted according to the format string
- **ISO Format**: Always provides ISO 8601 format regardless of format string
- **UNIX Timestamp**: Unix timestamp of the datetime

## Paths

- **Success**: DateTime formatting completed successfully
- **Error**: Error during formatting (invalid datetime, format error, etc.)

## Supported Input Types

### String Formats
- **ISO 8601**: `2024-01-15T12:30:45`, `2024-01-15T12:30:45Z`
- **Standard formats**: `2024-01-15 12:30:45`, `01/15/2024 12:30:45`
- **With timezone**: `2024-01-15T12:30:45+05:00`

### Numeric Inputs
- **Unix timestamps**: `1705320645` (integer)
- **Float timestamps**: `1705320645.123` (with fractional seconds)
- **Timestamp strings**: `"1705320645"`

### Object Inputs
- **Python datetime objects**: Direct datetime object input

## Predefined Formats

### Special Format Keywords
- **iso8601**: ISO 8601 format (`2024-01-15T12:30:45`)
- **timestamp**: Unix timestamp (`1705320645`)
- **rfc2822**: RFC 2822 format (`Mon, 15 Jan 2024 12:30:45`)
- **rfc3339**: RFC 3339 format (ISO 8601 with Z suffix)

### Common Format Examples
- **Date only**: `%Y-%m-%d` → `2024-01-15`
- **Standard datetime**: `%Y-%m-%d %H:%M:%S` → `2024-01-15 12:30:45`
- **Full month**: `%B %d, %Y` → `January 15, 2024`
- **12-hour with AM/PM**: `%b %d, %Y %I:%M %p` → `Jan 15, 2024 02:30 PM`
- **Full names**: `%A, %B %d, %Y` → `Monday, January 15, 2024`
- **European format**: `%d/%m/%Y %H:%M` → `15/01/2024 12:30`
- **US format**: `%m/%d/%Y %I:%M %p` → `01/15/2024 02:30 PM`

## Format Codes Reference

### Date Components
- `%Y`: 4-digit year (2024)
- `%y`: 2-digit year (24)
- `%m`: Month as number (01-12)
- `%B`: Full month name (January)
- `%b`: Abbreviated month name (Jan)
- `%d`: Day of month (01-31)

### Time Components
- `%H`: Hour 24-hour format (00-23)
- `%I`: Hour 12-hour format (01-12)
- `%M`: Minute (00-59)
- `%S`: Second (00-59)
- `%f`: Microsecond (000000-999999)
- `%p`: AM/PM indicator

### Day of Week
- `%A`: Full weekday name (Monday)
- `%a`: Abbreviated weekday name (Mon)
- `%w`: Weekday as number (0=Sunday, 6=Saturday)

### Timezone
- `%Z`: Timezone name (UTC, EST)
- `%z`: UTC offset (+0000, -0500)

## Locale Support

### Locale Configuration
- **Format**: Language code + country code (e.g., 'en_US', 'de_DE', 'fr_FR')
- **Effect**: Changes month names, day names, and other locale-specific elements
- **Fallback**: Uses system default if specified locale is unavailable

### Example Locale Effects
```
Date: 2024-01-15, Format: %B %d, %Y

en_US: "January 15, 2024"
de_DE: "Januar 15, 2024" 
fr_FR: "janvier 15, 2024"
```

## Example Use Cases

### User Interface Display
- **Dashboard timestamps**: Format log entries and event times for display
- **Report generation**: Create human-readable dates in business reports
- **Email notifications**: Format dates in user-friendly email content
- **Web applications**: Display dates according to user preferences

### Data Export
- **CSV files**: Format datetime columns for spreadsheet compatibility
- **PDF reports**: Create properly formatted date headers and timestamps
- **API responses**: Standardize datetime output format for API consumers
- **Log files**: Format timestamps for log analysis tools

### Internationalization
- **Multi-language apps**: Display dates in user's preferred language and format
- **Regional compliance**: Format dates according to local conventions
- **Cultural adaptation**: Use appropriate date formats for different regions

## Practical Examples

### Business Report Format
```
Input: "2024-01-15T14:30:45"
Format: "%B %d, %Y at %I:%M %p"
Output: "January 15, 2024 at 02:30 PM"
```

### European Style
```
Input: "2024-01-15T14:30:45"
Format: "%d/%m/%Y %H:%M"
Output: "15/01/2024 14:30"
```

### Log File Timestamp
```
Input: 1705320645
Format: "%Y-%m-%d %H:%M:%S"
Output: "2024-01-15 12:30:45"
```

### Full Descriptive Format
```
Input: "2024-01-15T14:30:45"
Format: "%A, %B %d, %Y at %I:%M %p"
Output: "Monday, January 15, 2024 at 02:30 PM"
```

## Error Handling

### Input Validation
- **Invalid datetime**: Clear error messages for unparseable input
- **Unsupported formats**: Graceful handling of unrecognized format codes
- **Locale errors**: Fallback to default locale when specified locale unavailable

### Format Validation
- **Invalid format codes**: Detection and reporting of unsupported format specifiers
- **Format syntax errors**: Clear error messages for malformed format strings

## Output Consistency

### Dual Output Strategy
- **Formatted output**: Custom formatted string as specified
- **ISO format**: Always provides standardized ISO 8601 format
- **Timestamp**: Always includes Unix timestamp for precise time reference

## Performance Considerations

- **Locale caching**: Efficient locale switching for repeated formatting
- **Format parsing**: Optimized format string processing
- **Memory efficient**: Minimal memory overhead for formatting operations
- **Timezone handling**: Efficient timezone-aware formatting when applicable

## Best Practices

- **Consistent formats**: Use standardized format strings across applications
- **Locale awareness**: Consider user locale preferences for international applications
- **Error handling**: Always check error path for formatting failures
- **Format validation**: Test format strings with sample data before deployment
- **Performance**: Cache frequently used format strings for better performance