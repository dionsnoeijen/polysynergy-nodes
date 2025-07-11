# Variable Json Node

The **Variable Json** node allows you to construct and manipulate JSON data dynamically, including **replacing placeholders** and optionally **appending extra keys**.  
It's designed for use in flows where structured data needs to be built or transformed before being passed to other nodes.

## **Category:** Variable

## **Description**
This node accepts a JSON **object, array, or string** (with optional placeholders), replaces placeholders using the provided `values`, and optionally appends a dictionary of new key-value pairs.

It outputs:
- A **parsed JSON object or list**
- A **stringified JSON representation**

This is especially useful when preparing structured payloads for use in integrations, API calls, or dynamic configuration generation.

## **Variables**

| Name             | Type         | Input | Output | Description |
|------------------|--------------|-------|--------|-------------|
| `value`          | str / dict / list | ✅ | ❌ | The base JSON input. Can be a string or actual structure. Placeholders like `{name}` can be used. |
| `values`         | dict         | ✅     | ✅     | Values used to replace placeholders inside `value` or `append`. |
| `append`         | dict (opt)   | ✅     | ❌     | Optional key-value pairs to append to the JSON object after replacement. Also supports placeholders. |
| `value_as_dict_or_list` | dict / list | ❌ | ✅     | The final parsed JSON after processing. |

## **Flow Control**
- `true_path` (str) – Set to the stringified JSON if parsing and replacement succeed.
- `false_path` (dict) – Contains the error details if something goes wrong (invalid JSON, missing placeholders, etc.).

## **How It Works**
1. Accepts `value` (string, dict, or list).
2. Replaces placeholders like `{key}` with values from `values`.
3. Parses the result into valid JSON.
4. Optionally appends additional keys from `append` (also with placeholder support).
5. Outputs both the structured and string versions of the result.

## **Example**

Given:
- `value = {"name": "{username}", "role": "editor"}`
- `values = {"username": "Alice"}`

Optional:
- `append = {"extra": "{role}", "active": true}`
- `values["role"] = "admin"`

The result:
```json
{
  "name": "Alice",
  "role": "editor",
  "extra": "admin",
  "active": true
}
```

## **Use Cases**
✔ Creating templated JSON payloads  
✔ Preparing request bodies for APIs  
✔ Dynamically appending metadata to config  
✔ Merging environment-specific settings

---

🧩 This node is ideal for making structured, mergeable, and placeholder-aware JSON within flows — without writing custom code.
