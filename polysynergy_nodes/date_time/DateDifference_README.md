# Date Difference

Calculates the time difference between two datetime values, providing multiple time unit outputs and human-readable descriptions.

## Description

The Date Difference node computes the difference between two datetime values (end - start) and outputs the result in multiple time units. It provides both positive and negative differences, absolute values, and human-readable descriptions. The node is essential for calculating durations, measuring elapsed time, and analyzing time intervals.

## Inputs

- **Start DateTime**: The starting datetime for the calculation (required)
- **End DateTime**: The ending datetime for the calculation (required)

## Outputs

- **Total Seconds**: Difference in seconds (positive/negative)
- **Total Minutes**: Difference in minutes (positive/negative)
- **Total Hours**: Difference in hours (positive/negative)
- **Total Days**: Difference in days (positive/negative)
- **Absolute Difference**: Absolute difference in seconds (always positive)
- **Human Readable**: User-friendly description of the time difference

## Paths

- **Success**: Date difference calculation completed successfully
- **Error**: Error during calculation (invalid datetime input, parse error, etc.)

## Calculation Logic

- **Formula**: Difference = End DateTime - Start DateTime
- **Positive result**: End datetime is after start datetime
- **Negative result**: End datetime is before start datetime
- **Zero result**: Both datetimes are identical

## Supported Input Formats

- **ISO 8601**: `2024-01-15T12:00:00`, `2024-01-15T12:00:00Z`
- **Standard formats**: `2024-01-15 12:00:00`, `2024-01-15`
- **With timezone**: `2024-01-15T12:00:00+05:00`
- **Microseconds**: `2024-01-15T12:00:00.123456`
- **Datetime objects**: Python datetime objects

## Human-Readable Format

The node automatically selects the most appropriate time unit:
- **< 60 seconds**: "45.0 seconds"
- **< 60 minutes**: "2.5 minutes"
- **< 24 hours**: "3.0 hours"
- **≥ 24 hours**: "5.0 days"

Negative differences are prefixed with a minus sign: "-3.0 hours"

## Example Use Cases

### Business Applications
- **SLA monitoring**: Calculate response times and resolution durations
- **Project management**: Measure task completion times and project phases
- **Performance metrics**: Analyze processing times and service intervals
- **Billing systems**: Calculate time-based charges and usage periods

### Data Analysis
- **Log analysis**: Measure time between events and system activities
- **User behavior**: Calculate session durations and interaction intervals
- **System monitoring**: Track uptime, downtime, and recovery periods
- **Trend analysis**: Measure time-based patterns and seasonal variations

## Practical Examples

### Same Day Difference
```
Start: "2024-01-15T09:00:00"
End: "2024-01-15T17:30:00"
Result: 8.5 hours, "8.5 hours"
```

### Multi-Day Difference
```
Start: "2024-01-15T12:00:00" 
End: "2024-01-20T12:00:00"
Result: 5.0 days, "5.0 days"
```

### Negative Difference
```
Start: "2024-01-15T17:30:00"
End: "2024-01-15T09:00:00" 
Result: -8.5 hours, "-8.5 hours"
```

### Minute-Level Precision
```
Start: "2024-01-15T12:00:00"
End: "2024-01-15T12:45:30"
Result: 45.5 minutes, "45.5 minutes"
```

### Microsecond Precision
```
Start: "2024-01-15T12:00:00.100000"
End: "2024-01-15T12:00:00.600000"
Result: 0.5 seconds, "0.5 seconds"
```

## Output Details

### Numerical Outputs
- **Total Seconds**: Floating-point precision for fractional seconds
- **Total Minutes**: Calculated as seconds / 60
- **Total Hours**: Calculated as seconds / 3600
- **Total Days**: Calculated as seconds / 86400
- **Absolute Difference**: Always positive, useful for duration calculations

### Time Unit Conversions
- 1 minute = 60 seconds
- 1 hour = 3,600 seconds
- 1 day = 86,400 seconds
- Leap seconds are not considered in calculations

## Edge Cases Handling

### Boundary Conditions
- **Zero difference**: Returns 0.0 for all time units
- **Microsecond differences**: Handles fractional seconds accurately
- **Large differences**: Supports calculations spanning years

### Date Boundaries
- **Midnight crossing**: Properly calculates across day boundaries
- **Month boundaries**: Handles months with different numbers of days
- **Year boundaries**: Correctly processes multi-year differences
- **Leap years**: Accounts for February 29th in calculations

## Timezone Considerations

- **Mixed timezones**: Handles datetime inputs with different timezone information
- **UTC normalization**: Automatically converts to comparable time values
- **DST handling**: Properly accounts for daylight saving time transitions
- **Timezone-naive inputs**: Treats as local system time

## Error Handling

- **Invalid datetime formats**: Clear error messages with format examples
- **Unparseable inputs**: Graceful handling of malformed datetime strings
- **Null values**: Proper error reporting for missing datetime inputs
- **Type errors**: Handles unexpected input types with descriptive messages

## Performance Characteristics

- **Efficient calculation**: Optimized datetime arithmetic operations
- **Memory efficient**: Minimal memory footprint for calculations
- **Precision handling**: Maintains microsecond precision throughout calculations
- **Scalable**: Handles both small intervals and large time spans equally well

## Best Practices

- **Consistent input formats**: Use standardized datetime formats when possible
- **Timezone awareness**: Consider timezone implications for cross-region calculations
- **Precision needs**: Choose appropriate precision level for your use case
- **Negative handling**: Account for negative differences in downstream processing