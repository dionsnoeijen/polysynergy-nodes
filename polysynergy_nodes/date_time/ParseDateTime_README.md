# Parse DateTime

Parses datetime strings from various formats into standardized datetime objects with automatic format detection and component extraction.

## Description

The Parse DateTime node converts datetime strings from a wide variety of formats into standardized datetime objects. It supports both automatic format detection and custom format specification. The node extracts individual datetime components (year, month, day, hour, minute, second) and provides multiple output formats including ISO 8601 and Unix timestamps.

## Inputs

- **DateTime String**: String to parse into datetime (required)
- **Format String**: Custom format string (optional, auto-detect if empty)
- **Output Format**: Format for the parsed datetime output (default: iso8601)

## Outputs

- **Parsed DateTime**: The parsed datetime in the specified format
- **UNIX Timestamp**: Unix timestamp of the parsed datetime
- **Year**: Extracted year component
- **Month**: Extracted month component (1-12)
- **Day**: Extracted day component (1-31)
- **Hour**: Extracted hour component (0-23)
- **Minute**: Extracted minute component (0-59)
- **Second**: Extracted second component (0-59)

## Paths

- **Success**: DateTime parsing completed successfully
- **Error**: Error during parsing (invalid format, unparseable string, etc.)

## Auto-Detection Formats

### ISO Formats
- `2024-01-15T12:30:45`
- `2024-01-15T12:30:45.123456`
- `2024-01-15T12:30:45Z`
- `2024-01-15T12:30:45+05:00`
- `2024-01-15 12:30:45`

### US Formats
- `01/15/2024 12:30:45`
- `01/15/2024 2:30:45 PM`
- `01/15/2024`

### European Formats
- `15/01/2024 12:30:45`
- `15/01/2024`
- `15-01-2024 12:30:45`
- `15-01-2024`

### Named Formats
- `January 15, 2024`
- `Jan 15, 2024`
- `15 January 2024`
- `15 Jan 2024`

### Time-Only Formats
- `12:30:45`
- `12:30`
- `2:30:45 PM`
- `2:30 PM`

### Compact Formats
- `20240115` (YYYYMMDD)
- `20240115123045` (YYYYMMDDHHMMSS)

### Unix Timestamps
- `1705320645` (as string)
- `1705320645.123` (with fractional seconds)

## Custom Format Specification

When providing a custom format string, use standard strftime format codes:

### Common Format Codes
- `%Y`: 4-digit year (2024)
- `%m`: Month as number (01-12)
- `%d`: Day of month (01-31)
- `%H`: Hour 24-hour format (00-23)
- `%M`: Minute (00-59)
- `%S`: Second (00-59)
- `%f`: Microsecond (000000-999999)

### Examples
- `%d/%m/%Y %H:%M:%S` → `15/01/2024 12:30:45`
- `%B %d, %Y` → `January 15, 2024`
- `%Y-%m-%d` → `2024-01-15`

## Output Formats

- **iso8601**: ISO 8601 format (`2024-01-15T12:30:45`)
- **Custom format**: Any valid strftime format string

## Example Use Cases

### Data Import
- **CSV processing**: Parse datetime columns from various CSV file formats
- **API integration**: Handle datetime strings from different API responses
- **Log parsing**: Extract timestamps from log files with varying formats
- **Database migration**: Convert datetime strings between different database formats

### User Input Processing
- **Form validation**: Parse user-entered datetime strings from web forms
- **Configuration files**: Process datetime settings from config files
- **Command-line tools**: Parse datetime arguments in various formats
- **Batch processing**: Handle mixed datetime formats in data batches

## Practical Examples

### Auto-Detection Success
```
Input: "January 15, 2024 2:30 PM"
Output: "2024-01-15T14:30:00"
Components: Year=2024, Month=1, Day=15, Hour=14, Minute=30, Second=0
```

### Custom Format Parsing
```
Input: "15/01/2024 14:30:45"
Format: "%d/%m/%Y %H:%M:%S"  
Output: "2024-01-15T14:30:45"
```

### Unix Timestamp Parsing
```
Input: "1705320645"
Output: "2024-01-15T12:30:45"
Timestamp: 1705320645
```

### Time-Only Parsing
```
Input: "2:30 PM"
Output: Today's date with "14:30:00"
Components: Hour=14, Minute=30, Second=0
```

## Component Extraction

The node automatically extracts all datetime components:
- **Year**: Full 4-digit year
- **Month**: Numeric month (1=January, 12=December)
- **Day**: Day of month (1-31)
- **Hour**: 24-hour format (0-23)
- **Minute**: Minute within hour (0-59)
- **Second**: Second within minute (0-59)

## Error Handling

### Common Error Scenarios
- **Invalid format**: Unrecognizable datetime string format
- **Format mismatch**: Custom format doesn't match input string
- **Invalid dates**: February 30th, invalid leap year dates
- **Ambiguous formats**: Strings that could be parsed multiple ways

### Error Messages
- Clear descriptions of parsing failures
- Examples of supported formats
- Specific format mismatch details
- Suggestions for correct format strings

## Auto-Detection Algorithm

1. **ISO format attempts**: Try various ISO 8601 variants first
2. **Common formats**: Test frequently used datetime formats
3. **Regional variants**: Try US, European, and other regional formats
4. **Time-only formats**: Handle time-only strings with today's date
5. **Numeric formats**: Attempt Unix timestamp parsing
6. **Fallback handling**: Provide clear error if no format matches

## Performance Considerations

- **Format caching**: Efficient format detection for repeated similar inputs
- **Early exit**: Stops testing formats after successful match
- **Optimized patterns**: Most common formats tested first
- **Memory efficient**: Minimal memory usage during parsing

## Best Practices

- **Consistent input**: Use standardized formats when possible for better performance
- **Format specification**: Provide custom format when input format is known and consistent
- **Error handling**: Always check error path for parsing failures
- **Component validation**: Validate extracted components match expected ranges
- **Timezone awareness**: Consider timezone handling for timezone-aware applications