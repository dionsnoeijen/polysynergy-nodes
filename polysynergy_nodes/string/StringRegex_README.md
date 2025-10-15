# 🔎 String Regex Node

The `String Regex` node performs regular expression operations on text including matching, searching, finding all occurrences, splitting, and replacing.

---

## 📂 Category

**string**

---

## ⚙️ Inputs

| Name        | Type   | Required | Description                              |
|-------------|--------|----------|------------------------------------------|
| text        | str    | ✅        | The text to process                      |
| pattern     | str    | ✅        | Regular expression pattern               |
| operation   | str    | ❌        | Operation type (default: search)         |
| replacement | str    | ❌        | Replacement string (for replace operation) |
| flags       | str    | ❌        | Regex flags (default: none)              |

---

## 🔌 Outputs

| Name        | Type            | Description                                 |
|-------------|-----------------|---------------------------------------------|
| true_path   | str \| list \| bool | Result based on operation type           |
| false_path  | dict            | Error information if regex fails            |

---

## ⚙️ Operations

| Operation | Description | Output Type |
|-----------|-------------|-------------|
| **match** | Full match from start | bool (True if matches) |
| **search** | Find first occurrence | str (matched text or None) |
| **findall** | Find all occurrences | list of matches |
| **split** | Split text by pattern | list of strings |
| **replace** | Replace matches | str (text with replacements) |

---

## 🎯 Regex Flags

- **none**: No flags
- **ignorecase**: Case-insensitive matching
- **multiline**: ^ and $ match line boundaries
- **dotall**: . matches newlines
- **ignorecase_multiline**: Combination of ignorecase and multiline

---

## ✅ Examples

### Search for Pattern:
```json
{
  "text": "Email: user@example.com",
  "pattern": "[\\w.-]+@[\\w.-]+",
  "operation": "search"
}
```
**Output:** `"user@example.com"`

### Find All Matches:
```json
{
  "text": "Prices: $10, $20, $30",
  "pattern": "\\$\\d+",
  "operation": "findall"
}
```
**Output:** `["$10", "$20", "$30"]`

### Split by Pattern:
```json
{
  "text": "apple,banana;cherry:date",
  "pattern": "[,;:]",
  "operation": "split"
}
```
**Output:** `["apple", "banana", "cherry", "date"]`

### Replace Pattern:
```json
{
  "text": "Phone: 123-456-7890",
  "pattern": "\\d",
  "operation": "replace",
  "replacement": "X"
}
```
**Output:** `"Phone: XXX-XXX-XXXX"`

### Case Insensitive Match:
```json
{
  "text": "Hello World",
  "pattern": "^hello",
  "operation": "match",
  "flags": "ignorecase"
}
```
**Output:** `true`

---

## 💡 Use Cases

- Validate email addresses, URLs, phone numbers
- Extract data from structured text
- Parse log files or formatted data
- Clean and normalize text
- Find and replace patterns

---

## ⚠️ Notes

- Pattern must be a valid regular expression
- Invalid regex patterns will trigger the `false_path`
- Use raw strings or escape backslashes in patterns
- Empty pattern will match at every position
- Search returns `None` (not error) when no match found
