
# 🚦 Route Node

The `Route` node is part of the **hidden** category and serves as the starting point for a route flow. It is automatically configured via the request to the corresponding endpoint in the flow, or via the mock configuration. This node is not configurable by the user, but it defines the basic properties required for routing and handles the flow of data.

---

## ✅ Functionality

This node is used as the starting point for a route flow. It is configured automatically by the system, either through the request at the endpoint or via mock configuration. The node defines HTTP-related properties like `method`, `headers`, `body`, `query`, and `cookies`, as well as any route-specific variables that are needed for the flow to continue.

---

## 🔌 Inputs

This node does not take any inputs, as it is automatically configured via the request or mock setup.

---

## 🔀 Outputs

| Name            | Type          | Description                                     |
|-----------------|---------------|-------------------------------------------------|
| true_path       | bool          | Indicates the flow state for the route (always true in this case). |
| method          | string        | The HTTP method for the route request (GET, POST, etc.). |
| headers         | dict          | A dictionary of HTTP headers for the request. |
| body            | string, bytes | The body of the HTTP request (for POST, PUT, etc.). |
| query           | dict          | Query parameters for the route request. |
| cookies         | dict          | Cookies to send with the route request. |
| route_variables | dict          | Variables that are part of the route URL (e.g., dynamic segments). |

---

## 💡 Example

### Input (Automatically configured based on the route request):
```json
{
  "method": "GET",
  "headers": {"Authorization": "Bearer token"},
  "body": null,
  "query": {"param1": "value1"},
  "cookies": {"session": "abc123"},
  "route_variables": {"resource_id": "123"}
}
```

### Output via `true_path`:
```json
{
  "true_path": true
}
```

---

## ⚠️ Notes

- This node is **automatically configured** and cannot be manually adjusted by the user.
- It provides the basic HTTP-related data (method, headers, body, etc.) that will be used throughout the route flow.
- The node does not perform any action by itself but is simply a starting point for the flow.
- This node is marked as part of the **hidden** category, meaning it does not appear in the node selection or UI for user configuration.

---

## 🔧 Dependencies

- **HTTPMethod**: The available HTTP methods (GET, POST, etc.) for selecting the request type.
- **PathSettings**: Defines the `true_path` output to indicate the success or continuation of the route flow.
