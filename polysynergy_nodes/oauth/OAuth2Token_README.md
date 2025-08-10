# OAuth 2.0 Token

Handles OAuth 2.0 authentication flows to obtain and manage access tokens.  
Supports automatic token caching, expiry management, and refresh token flows for seamless API authentication.

## **Category:** Auth

## **Description**
The **OAuth 2.0 Token** node implements OAuth 2.0 authentication flows to obtain valid access tokens for API requests. It automatically handles token caching, expiry checking, and refresh token flows to ensure you always have a valid token.

Key features:
- **Client Credentials Flow**: For server-to-server authentication  
- **Refresh Token Flow**: For renewing expired access tokens
- **Automatic Token Management**: Caches tokens and handles expiry automatically
- **DynamoDB Storage**: Persists tokens for reuse across executions (optional)
- **Graceful Fallback**: Works without DynamoDB for simple use cases
- **Comprehensive Error Handling**: Clear error reporting for troubleshooting

## **Variables**

### **Input Variables**
| Name            | Type | Input | Output | Required | Description |
|-----------------|------|-------|--------|----------|-------------|
| `service_name`  | str  | ✅     | ❌      | ✅        | Unique identifier for this OAuth service (used for token storage) |
| `client_id`     | str  | ✅     | ❌      | ✅        | OAuth client identifier from your OAuth provider |
| `client_secret` | str  | ✅     | ❌      | ✅        | OAuth client secret from your OAuth provider |
| `token_url`     | str  | ✅     | ❌      | ✅        | OAuth token endpoint URL |
| `grant_type`    | str  | ✅     | ❌      | ❌        | OAuth grant type (`client_credentials` or `refresh_token`) |
| `scope`         | str  | ✅     | ❌      | ❌        | OAuth scope (space-separated list of permissions) |

### **Output Variables**
| Name           | Type | Input | Output | Description |
|----------------|------|-------|--------|-------------|
| `access_token` | str  | ❌     | ✅      | Valid OAuth access token ready for API requests |
| `token_type`   | str  | ❌     | ✅      | Token type (usually 'Bearer') |
| `expires_in`   | int  | ❌     | ✅      | Token expiry time in seconds |

## **Flow Control**

| Name         | Description |
|--------------|-------------|
| `true_path`  | Triggered when token is successfully obtained. Contains the access token. |
| `false_path` | Triggered when token request fails. Contains error details. |

## **How It Works**

### **Token Lifecycle Management**
1. **Check Existing Token**: First checks if a valid cached token exists
2. **Validate Expiry**: Ensures token hasn't expired (with 60-second buffer)
3. **Request New Token**: If needed, requests a new token using the specified grant type
4. **Cache Token**: Stores the new token for future use
5. **Output Token**: Returns the valid access token

### **Supported Grant Types**

#### **Client Credentials Flow** (Default)
Used for server-to-server authentication where your application authenticates itself:
```
POST /oauth/token
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials
&client_id=your_client_id
&client_secret=your_client_secret
&scope=your_requested_scope
```

#### **Refresh Token Flow**
Used to obtain a new access token using a previously obtained refresh token:
```
POST /oauth/token
Content-Type: application/x-www-form-urlencoded

grant_type=refresh_token
&client_id=your_client_id
&client_secret=your_client_secret
&refresh_token=your_refresh_token
```

---

## **Example Usage**

### **Basic Client Credentials Flow**
```
Input:
- service_name: "my_api_service"
- client_id: "your_app_client_id" 
- client_secret: "your_app_client_secret"
- token_url: "https://api.example.com/oauth/token"
- grant_type: "client_credentials"
- scope: "read write"

Output (Success):
- access_token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
- token_type: "Bearer"
- expires_in: 3600
- true_path: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### **Using with HTTP Request Node**
The access token output can be used directly in HTTP request headers:

**OAuth Node** → **HTTP Request Node**
- Connect `access_token` output to a variable
- In HTTP Request node, set Headers:
  ```json
  {
    "Authorization": "Bearer {{access_token}}"
  }
  ```

### **Refresh Token Flow Example**
```
Input:
- service_name: "my_api_service"  # Same as original request
- client_id: "your_app_client_id"
- client_secret: "your_app_client_secret"  
- token_url: "https://api.example.com/oauth/token"
- grant_type: "refresh_token"
# Note: refresh_token is loaded automatically from storage
```

### **Error Response Example**
```json
{
  "error": "Token request failed (400): invalid_client",
  "message": "Client authentication failed",
  "type": "OAuth2Error"
}
```

---

## **Token Storage**

### **DynamoDB Integration**
The node automatically stores tokens in a DynamoDB table named `OAuthTokens` with the following structure:
```json
{
  "service_name": "my_api_service",        # Partition key
  "access_token": "token_value",
  "refresh_token": "refresh_value",        # If provided
  "expires_at": 1640995200.0,             # Unix timestamp
  "token_type": "Bearer",
  "expires_in": 3600
}
```

### **Environment Variables**
Configure AWS credentials for DynamoDB access:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`  
- `AWS_REGION` (defaults to `eu-central-1`)

### **Graceful Fallback**
If DynamoDB is not available or configured, the node:
- ✅ Still functions normally for token requests
- ✅ Handles all OAuth flows without storage
- ❌ Cannot persist tokens between executions
- ❌ Must request new tokens on each run

---

## **Error Handling**

### **Common Error Scenarios**
| Error Type | Cause | Solution |
|------------|-------|----------|
| `invalid_client` | Wrong client_id or client_secret | Verify credentials with OAuth provider |
| `invalid_grant` | Invalid or expired refresh_token | Re-authenticate to get new refresh token |
| `invalid_scope` | Requested scope not allowed | Check scope permissions with OAuth provider |
| `Network Error` | Connection issues | Check network connectivity and token_url |
| `Invalid Grant Type` | Unsupported grant_type | Use `client_credentials` or `refresh_token` |

### **Error Response Format**
All errors return a structured error object:
```json
{
  "error": "Descriptive error message",
  "type": "ErrorType", 
  "message": "Additional context"
}
```

---

## **Best Practices**

### **Service Naming**
- Use descriptive, unique service names: `"salesforce_prod"`, `"github_api"`, `"slack_bot"`
- Avoid changing service names to preserve token cache
- Use different service names for different environments

### **Security**
- ✅ Store client secrets in environment variables or secure vaults
- ✅ Use minimum required scopes
- ✅ Monitor token usage and expiry
- ❌ Never log or expose client secrets
- ❌ Don't hardcode credentials in flows

### **Token Management**
- Let the node handle token expiry automatically
- Use the same `service_name` for token reuse
- The node adds a 60-second buffer before token expiry
- Refresh tokens are stored and used automatically

---

## **Integration Examples**

### **With Variable Storage**
```
OAuth Token → Variable (String) → HTTP Request
access_token    bearer_token      Authorization: Bearer {{bearer_token}}
```

### **Error Handling Flow**
```
OAuth Token
├─ true_path → HTTP Request → API Success
└─ false_path → Log Error → Notification
```

### **Multi-Service Setup**
```
OAuth Token (service: "api_a") → HTTP Request A
OAuth Token (service: "api_b") → HTTP Request B  
OAuth Token (service: "api_c") → HTTP Request C
```

---

## **Use Cases**
✔ **API Authentication**: Get tokens for RESTful API access  
✔ **Microservice Communication**: Server-to-server authentication  
✔ **Third-party Integrations**: Authenticate with external services  
✔ **Automated Workflows**: Long-running processes needing token refresh  
✔ **Multi-tenant Applications**: Different tokens per tenant/service  

---

🔐 **Use this node when you need OAuth 2.0 tokens for authenticated API requests. It handles the complexity of token management so you can focus on your application logic.**