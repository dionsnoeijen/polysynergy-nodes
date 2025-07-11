# HTTP Response

⚠️ **Note:** This node cannot be followed by other nodes in a flow. It is a terminal node used to return a response in an HTTP route.

## **Category:** HTTP

## **Description**
The **HTTP Response** node creates a structured HTTP response for use in an HTTP route.  
It sets headers, body content, **Content‑Type**, and status code to return to the requester.

This node should only be used at the end of a flow triggered by an HTTP request.

## **Variables**

| Name            | Type                        | Input | Output | Description |
|-----------------|-----------------------------|:-----:|:------:|-------------|
| `headers`       | `dict[str, str]`            | ✅     | ❌      | Headers to include in the HTTP response. |
| `content_type`  | `str` (select)              | ✅     | ❌      | Convenience dropdown for common `Content‑Type` values (e.g. `application/json`). When set, it is merged into the headers as **`Content‑Type`**. |
| `body`          | `str \| bytes`             | ✅     | ❌      | The body of the HTTP response. |
| `http_status`   | `int`                       | ✅     | ❌      | The HTTP status code to return (default: **200 OK**). |

## **How It Works**
1. Copies the supplied `headers` (or initialises an empty dict).  
2. Inserts / overrides the `Content‑Type` header with the value from **`content_type`**.  
3. Combines headers, body, and status into a response‑dict consumable by the HTTP route handler.  
4. Any errors are logged and `response` is set to `None`.

No `true_path` or `false_path` is used—this is a terminal node.

---

## **Use Cases**
✔ Returning JSON (`application/json`) or HTML with the correct `Content‑Type` automatically.  
✔ Creating custom status responses from a flow.  
✔ Ending an HTTP route execution gracefully.

---

🚧 **This node is a terminal node and should be the last node in a route.**
