✅ **Enhanced:** This node has been upgraded with async support for better performance and non-blocking HTTP operations.

# HTTP Request

Sends a configurable HTTP request and returns the response.

## **Category:** http

## **Description**
The **HTTP Request** node allows you to perform asynchronous HTTP(S) requests using various methods (GET, POST, PUT, DELETE, etc.).  
It supports full control over all request parameters including headers, query strings, body, SSL options, and proxy configs.

It also supports dynamic URL construction via placeholder replacement using the `url_variables` input.

### **Key Features:**
- **Async Operations:** Non-blocking HTTP requests for better performance
- **Modern HTTP Client:** Uses `httpx` for reliable and efficient HTTP operations
- **Flexible Configuration:** Support for all HTTP methods, headers, and options
- **Dynamic URLs:** Placeholder replacement for parameterized requests
- **Error Handling:** Structured error responses with detailed information

## **Variables**

| Name                  | Type              | Input | Output | Description |
|-----------------------|-------------------|--------|--------|-------------|
| `url`                 | str               | ✅     | ❌      | Target URL. Placeholders like `{id}` can be used. |
| `url_variables`       | dict[str, str]    | ✅     | ❌      | Placeholder values for URL replacement. |
| `method`              | str               | ✅     | ❌      | HTTP method (GET, POST, PUT, DELETE, etc.). |
| `headers`             | dict[str, str]    | ✅     | ❌      | HTTP request headers. |
| `body`                | str or bytes      | ✅     | ❌      | Request body (raw or text). |
| `query`               | dict[str, str]    | ✅     | ❌      | Query string parameters. |
| `cookies`             | dict[str, str]    | ✅     | ❌      | Cookies to send with the request. |
| `timeout`             | float             | ✅     | ❌      | Timeout for the request in seconds. |
| `allow_redirects`     | bool              | ✅     | ❌      | Whether to follow redirects. |
| `verify_ssl`          | bool              | ✅     | ❌      | Whether to verify SSL certificates. |
| `proxies`             | dict              | ✅     | ❌      | Optional proxy configuration. |
| `response_http_status`| int               | ❌     | ✅      | HTTP status code from the response. |
| `response_body`       | str               | ❌     | ✅      | Response body as text. |
| `response_headers`    | dict[str, str]    | ❌     | ✅      | Response headers. |
| `response_cookies`    | dict[str, str]    | ❌     | ✅      | Response cookies. |
| `response_elapsed`    | float             | ❌     | ✅      | Time taken for the request (in seconds). |

## **Flow Control**

| Name         | Description |
|--------------|-------------|
| `true_path`  | Triggered if response status code is **less than 400**. Contains response body. |
| `false_path` | Triggered on exception or if response code is **400 or greater**. Contains error text. |

## **How It Works**
1. URL placeholders are replaced using the `url_variables` dictionary.
2. A request is made using the specified method and parameters.
3. Outputs and flow path are set depending on success or failure.

## **Example**

### **Input**
- `url` = `https://api.example.com/users/{user_id}`
- `url_variables` = { "user_id": "abc123" }
- `method` = `GET`

### **Output**
- `response_http_status` = `200`
- `response_body` = `{"id": "abc123", "name": "John"}`
- `true_path` triggered

### **Error Example**
- `response_http_status` = `404`
- `false_path` = `"404: Not Found"`

---

_Generated on 2025-04-30_
