# Range Router

Routes numeric values based on specified ranges and conditions to different output paths.

## Description

The Range Router node evaluates numeric values against various range conditions and routes them to corresponding output connections. It supports range specifications, comparison operators, and exact value matching for flexible numeric routing.

## Inputs

- **Value**: The numeric value to check against ranges (required)

## Outputs

Dynamic output connections based on range specifications:

- **Range outputs**: Each range condition creates a corresponding output (e.g., "0-100", ">50", "<=10")
- **default**: Fallback route for non-numeric values or unmatched ranges

## Paths

- **No Match**: Triggered when value is not numeric and no default exists, or no range matches

## Supported Range Formats

- **Inclusive ranges**: `0-100` (value between 0 and 100, inclusive)
- **Greater than**: `>50` (value greater than 50)
- **Less than**: `<10` (value less than 10)
- **Greater than or equal**: `>=30` (value greater than or equal to 30)
- **Less than or equal**: `<=20` (value less than or equal to 20)
- **Equal to**: `==5` or `5` (value exactly equals 5)

## Behavior

1. Attempts to convert input value to a numeric type (float)
2. If conversion fails, uses "default" route or triggers false path
3. Evaluates value against each range condition in order
4. Routes to the first matching range output
5. If no ranges match, uses "default" route or triggers false path
6. Kills all non-matching output connections
7. Passes the original input value through the selected route

## Example Use Cases

- **Age-based routing**: Route users to different flows based on age groups (0-17, 18-65, >65)
- **Score categorization**: Direct test scores to grade categories (0-59, 60-79, 80-100)
- **Temperature thresholds**: Route sensor readings to appropriate alert systems (<0, 0-25, >25)
- **Quantity handling**: Process orders differently based on item quantities (1-10, 11-100, >100)
- **Performance monitoring**: Alert different teams based on response times (<100ms, 100-500ms, >500ms)

## Range Evaluation

- Ranges are evaluated in the order they appear in the configuration
- The first matching range determines the routing
- Boundary values are handled according to the operator (inclusive for `-`, `<=`, `>=`)
- Invalid range formats are ignored and don't match any values