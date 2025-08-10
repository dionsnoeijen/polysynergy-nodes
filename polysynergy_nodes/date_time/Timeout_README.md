# Timeout

Introduces a time delay in workflow execution by pausing for a specified number of seconds.

## Description

The Timeout node creates a pause in workflow execution for a specified duration. It uses Python's `time.sleep()` function to block execution for the given number of seconds before continuing to the next node. This node is essential for implementing delays, rate limiting, polling intervals, and timing controls in automated workflows.

## Inputs

- **Seconds**: Number of seconds to wait before continuing (default: 1)
  - Supports integer and floating-point values
  - Accepts fractional seconds for millisecond precision

## Outputs

None - This node only controls execution timing.

## Paths

- **True Path**: Always triggered after the timeout period completes

## Behavior

1. **Execution pause**: Stops workflow execution for the specified duration
2. **Blocking operation**: No other nodes execute during the timeout period
3. **Precise timing**: Uses system sleep function for accurate delays
4. **Always continues**: Always follows the true path after completion

## Example Use Cases

### Rate Limiting
- **API calls**: Add delays between API requests to respect rate limits
- **Web scraping**: Pause between page requests to avoid overwhelming servers
- **Database operations**: Space out intensive database operations

### Polling and Monitoring
- **Status checking**: Wait between status checks in polling loops
- **File monitoring**: Pause between file system checks
- **Health monitoring**: Interval delays in system health checks

### User Experience
- **Progressive disclosure**: Create timed reveals in user interfaces
- **Animation timing**: Coordinate with frontend animations or transitions
- **Notification spacing**: Space out notifications to users

### System Coordination
- **Service startup**: Allow time for services to initialize
- **Resource allocation**: Wait for resources to become available
- **Process synchronization**: Coordinate timing between different processes

## Duration Examples

### Sub-second Precision
```
Seconds: 0.1    → 100 milliseconds
Seconds: 0.5    → 500 milliseconds  
Seconds: 0.001  → 1 millisecond
```

### Standard Intervals
```
Seconds: 1      → 1 second
Seconds: 5      → 5 seconds
Seconds: 30     → 30 seconds
Seconds: 60     → 1 minute
```

### Longer Delays
```
Seconds: 300    → 5 minutes
Seconds: 3600   → 1 hour
Seconds: 86400  → 24 hours
```

## Practical Examples

### API Rate Limiting
```
Workflow: API Request → Timeout (1 second) → Next API Request
Purpose: Ensure 1-second gap between API calls
```

### Retry Logic with Backoff
```
Workflow: Try Operation → (if fails) → Timeout (5 seconds) → Retry Operation
Purpose: Wait before retrying failed operations
```

### Polling Loop
```
Workflow: Check Status → Timeout (10 seconds) → Check Status (repeat)
Purpose: Check system status every 10 seconds
```

### Batch Processing Pace
```
Workflow: Process Item → Timeout (0.1 seconds) → Process Next Item
Purpose: Limit processing rate to 10 items per second
```

## Timing Considerations

### Precision
- **System dependent**: Actual sleep time depends on system timer resolution
- **Minimum duration**: Very small values may be rounded up by the operating system
- **Interruption**: Sleep can be interrupted by system signals

### Performance Impact
- **Blocking behavior**: Completely stops workflow execution during timeout
- **Resource usage**: Minimal CPU usage during sleep period
- **Memory usage**: No additional memory overhead

## Edge Cases

### Zero and Negative Values
- **Zero seconds**: `time.sleep(0)` still yields control to other processes
- **Negative values**: Python's `time.sleep()` handles negative values as zero

### Large Values
- **Hour/day delays**: Supports very long timeout periods
- **System limits**: Subject to system-specific maximum sleep durations

## Error Handling

### Interruption Scenarios
- **Keyboard interrupt**: Ctrl+C can interrupt sleep operations
- **System signals**: Process signals may interrupt sleep
- **Graceful handling**: Interruptions are passed through to the workflow engine

## Best Practices

### Appropriate Usage
- **Necessary delays only**: Only use timeouts when genuinely needed
- **Reasonable durations**: Avoid excessively long delays that block workflows
- **User feedback**: Consider providing progress indicators for long delays

### Performance Optimization
- **Minimal delays**: Use the shortest delay that achieves the desired effect
- **Asynchronous alternatives**: Consider asynchronous patterns for concurrent operations
- **Batch operations**: Group operations to reduce the number of required delays

### Workflow Design
- **Clear purpose**: Document why delays are necessary in workflow design
- **Configurable timing**: Make timeout values configurable when possible
- **Fallback paths**: Design workflows to handle timeout interruptions gracefully

## Alternative Patterns

### When Not to Use Timeout
- **Waiting for events**: Use event-driven patterns instead of polling
- **Network operations**: Use proper timeout parameters in network calls
- **User interactions**: Use asynchronous user interface patterns

### Better Alternatives
- **Event-driven**: Wait for specific events or conditions
- **Asynchronous operations**: Use non-blocking operations where possible
- **Scheduled execution**: Use proper scheduling systems for time-based operations

## Integration Patterns

### Common Workflow Patterns
1. **Request → Timeout → Request**: Rate-limited API calls
2. **Action → Timeout → Check → Repeat**: Polling loops
3. **Batch → Timeout → Next Batch**: Paced batch processing
4. **Retry → Timeout → Retry**: Exponential backoff retry logic