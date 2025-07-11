
# 🚗 Mock Route Node

The `Mock Route` node is part of the **mock** category and is used to simulate HTTP route requests for testing purposes. It allows you to specify a URL, HTTP method, headers, body, query parameters, and cookies, making it useful for testing how routes will behave in a real environment.

---

## ✅ Functionality

This node is designed to simulate a route request. You can define the URL, HTTP method, headers, body, query parameters, and cookies, and use it in a flow to mock the behavior of an HTTP request. This allows for testing without actually making real HTTP calls.

---

## 🔌 Inputs

| Name            | Type     | Required | Description                                        |
|-----------------|----------|----------|----------------------------------------------------|
| url             | string   | Yes      | The URL for the simulated route request. |
| method          | string   | Yes      | The HTTP method for the request, e.g., GET, POST. |
| headers         | dict     | No       | A dictionary of headers to send with the request. |
| body            | bytes    | No       | The body of the request, typically used for POST requests. |
| query           | dict     | No       | Query parameters for the route request. |
| cookies         | dict     | No       | Cookies to send with the request. |
| route_variables | dict     | No       | Additional route variables for simulating dynamic paths. |

---

## 🔀 Outputs

| Name        | Type             | Description                                    |
|-------------|------------------|------------------------------------------------|
| true_path   | bool             | A value indicating that the route simulation is ready to proceed. |

---

## 💡 Example

### Input:
```json
{
  "url": "/api/v1/resource",
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

- This node simulates an HTTP request but does not perform any actual network operation.
- The `method` input uses HTTP methods (GET, POST, etc.) and defaults to `GET`.
- The `route_variables` input allows you to simulate dynamic route parameters (e.g., `/api/v1/resource/{resource_id}`).
- This node includes a play button (`has_play_button=True`) for initiating the simulation in the workflow.
- This node does not generate any data itself but controls the flow based on the simulated request configuration.

---

## 🔧 Dependencies

- **HTTPMethod**: The available HTTP methods (GET, POST, etc.) for selecting the request type.
- **PathSettings**: Defines the `true_path` output that signals when the route is ready to be processed.
