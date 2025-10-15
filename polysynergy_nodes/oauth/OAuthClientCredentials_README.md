# 🔐 OAuth Client Credentials Node

The `OAuth Client Credentials` node implements the OAuth 2.0 Client Credentials Grant flow for service-to-service authentication. Ideal for server-to-server communication where no user interaction is required.

---

## 📂 Category

**auth**

---

## ⚙️ Inputs

| Name           | Type       | Required | Description                              |
|----------------|------------|----------|------------------------------------------|
| client_id      | str        | ✅        | OAuth client identifier                  |
| client_secret  | str        | ✅        | OAuth client secret                      |
| token_url      | str        | ✅        | OAuth token endpoint URL                 |
| scopes         | list[str]  | ❌        | OAuth permission scopes                  |
| resource       | str        | ❌        | Resource parameter (for older MS endpoints) |

---

## 🔌 Outputs

| Name           | Type       | Description                              |
|----------------|------------|------------------------------------------|
| access_token   | str        | Valid OAuth access token                 |
| token_type     | str        | Token type (usually 'Bearer')            |
| expires_in     | int        | Token expiry time in seconds             |
| scopes_output  | list[str]  | Granted OAuth scopes                     |

---

## 🔀 Flow Control

| Path        | Description                                 |
|-------------|---------------------------------------------|
| true_path   | Token obtained successfully (Bearer token)  |
| false_path  | Token request failed (error details)        |

---

## ✅ Example Usage

### Basic Client Credentials Flow:
```json
{
  "client_id": "your_client_id",
  "client_secret": "your_client_secret",
  "token_url": "https://oauth.provider.com/token",
  "scopes": ["api.read", "api.write"]
}
```

**Output:** `"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."`

### Microsoft Azure AD Example:
```json
{
  "client_id": "app_client_id",
  "client_secret": "app_secret",
  "token_url": "https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token",
  "scopes": ["https://graph.microsoft.com/.default"]
}
```

---

## 🔄 Token Management

- **Automatic Caching**: Tokens stored in DynamoDB (if configured)
- **Expiry Check**: Validates token expiry with 60-second buffer
- **Auto-Refresh**: Requests new token when expired
- **Persistent Storage**: Tokens reused across executions

---

## 🔒 Security Features

- Secure token storage in DynamoDB
- Automatic token renewal before expiry
- No user credentials stored
- Environment-based AWS configuration

---

## 💡 Use Cases

- **Microservice Authentication**: Service-to-service API calls
- **Background Jobs**: Automated tasks requiring API access
- **Server Applications**: Backend processes without user interaction
- **CI/CD Pipelines**: Automated deployments with API authentication

---

## ⚠️ Notes

- **Microsoft Scopes**: For Microsoft services, use `.default` scope (e.g., `https://graph.microsoft.com/.default`)
- **DynamoDB Optional**: Works without DynamoDB but won't cache tokens
- **Environment Variables**: Requires `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`
- **No User Context**: This flow doesn't involve user authentication
