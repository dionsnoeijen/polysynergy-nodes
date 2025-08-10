# Time Router

Routes datetime values based on time-of-day and day-of-week categorization to different output paths.

## Description

The Time Router node analyzes datetime values and routes them to predefined time-based categories. It supports flexible datetime input formats and provides both time-of-day routing (morning, afternoon, evening, night) and day-type routing (weekday, weekend).

## Inputs

- **DateTime**: DateTime object, timestamp, or ISO string to route based on time (required)

## Outputs

Predefined output connections for time-based routing:

- **morning**: Routes times from 5:00 AM to 11:59 AM
- **afternoon**: Routes times from 12:00 PM to 4:59 PM  
- **evening**: Routes times from 5:00 PM to 8:59 PM
- **night**: Routes times from 9:00 PM to 4:59 AM
- **weekday**: Routes Monday through Friday
- **weekend**: Routes Saturday and Sunday
- **default**: Fallback route for invalid datetime or unmatched categories

## Paths

- **No Match**: Triggered when datetime is invalid and no default exists

## Supported DateTime Formats

- **DateTime objects**: Python `datetime` objects
- **Unix timestamps**: Integer or float timestamps (e.g., `1705309800`)
- **ISO strings**: ISO 8601 format (e.g., `"2024-01-15T14:30:00"`)
- **Common formats**:
  - `"2024-01-15 14:30:00"`
  - `"2024-01-15"`
  - `"14:30:00"`
  - `"14:30"`

## Time Categories

### Time of Day
- **Morning**: 5:00 AM - 11:59 AM (05:00 - 11:59)
- **Afternoon**: 12:00 PM - 4:59 PM (12:00 - 16:59)
- **Evening**: 5:00 PM - 8:59 PM (17:00 - 20:59)
- **Night**: 9:00 PM - 4:59 AM (21:00 - 04:59)

### Day Type
- **Weekday**: Monday through Friday (0-4)
- **Weekend**: Saturday and Sunday (5-6)

## Routing Priority

1. **Time of day categories** have highest priority
2. **Day type categories** are used if time of day not available
3. **Default** route is used if no specific categories match

## Behavior

1. Parses input into a Python datetime object
2. If parsing fails, uses "default" route or triggers false path
3. Determines time category based on hour and day of week
4. Routes to the most specific available category
5. Kills all non-matching output connections
6. Passes the original input value through the selected route

## Example Use Cases

- **Business hours routing**: Route requests differently during business vs after hours
- **Scheduled processing**: Route jobs to different queues based on time of day
- **User experience**: Show different content for morning vs evening users
- **Resource allocation**: Scale services differently for weekday vs weekend traffic
- **Notification timing**: Send different notification types based on time
- **Backup scheduling**: Route backup jobs based on time windows

## Time Zone Considerations

- All times are processed in the system's local timezone
- Unix timestamps are converted to local time
- ISO strings with timezone info are converted to local time
- For UTC processing, ensure input datetimes are already in UTC

## Configuration Examples

**Morning-focused workflow**:
```
Available outputs: morning, default
Morning tasks -> morning output
All other times -> default output
```

**Business hours routing**:
```  
Available outputs: morning, afternoon, evening, default
Business hours (morning/afternoon) -> respective outputs
After hours (evening/night/weekend) -> default output
```

**Weekend vs weekday**:
```
Available outputs: weekday, weekend
Monday-Friday -> weekday output
Saturday-Sunday -> weekend output
```