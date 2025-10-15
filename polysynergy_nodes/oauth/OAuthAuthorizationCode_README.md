# 👤 OAuth Authorization Code Node

The `OAuth Authorization Code` node implements the OAuth 2.0 Authorization Code Grant flow for user authentication. Redirects users to authorize access, then exchanges the authorization code for tokens.

---

## 📂 Category

**auth**

---

## ⚙️ Inputs

| Name            | Type       | Required | Description                              |
|-----------------|------------|----------|------------------------------------------|
| service_name    | str        | ✅        | Human-readable service name              |
| auth_url        | str        | ✅        | OAuth authorization endpoint URL         |
| token_url       | str        | ✅        | OAuth token endpoint URL                 |
| client_id       | str        | ✅        | OAuth client identifier                  |
| client_secret   | str        | ✅        | OAuth client secret                      |
| scopes          | list[str]  | ✅        | OAuth permission scopes                  |
| state           | str        | ❌        | CSRF protection state parameter          |
| response_type   | str        | ❌        | Response type (default: 'code')          |
| resource        | str        | ❌        | Resource parameter (Azure AD/SharePoint) |

---

## 🔌 Outputs

| Name              | Type       | Description                              |
|-------------------|------------|------------------------------------------|
| service_name_output | str      | Name of authenticated service            |
| scopes_output     | list[str]  | Granted OAuth scopes                     |
| access_token      | str        | OAuth access token                       |
| refresh_token     | str        | OAuth refresh token                      |
| token_type        | str        | Token type (usually 'Bearer')            |
| expires_in        | int        | Token expiry time in seconds             |

---

## 🔀 Flow Control

| Path        | Description                                 |
|-------------|---------------------------------------------|
| true_path   | Authorization successful (access token)     |
| false_path  | Authorization failed (error details)        |

---

## 📋 Authorization Flow

1. **Initial Request**: Generates authorization URL for user
2. **User Authorization**: User redirects to provider and grants permission
3. **Callback**: Provider redirects back with authorization code
4. **Token Exchange**: Code exchanged for access/refresh tokens
5. **Token Storage**: Tokens saved in DynamoDB for reuse

---

## ✅ Example Usage

### Google OAuth Example:
```json
{
  "service_name": "Google Drive",
  "auth_url": "https://accounts.google.com/o/oauth2/v2/auth",
  "token_url": "https://oauth2.googleapis.com/token",
  "client_id": "your_client_id.apps.googleusercontent.com",
  "client_secret": "your_client_secret",
  "scopes": ["https://www.googleapis.com/auth/drive.readonly"]
}
```

### Microsoft Azure AD Example:
```json
{
  "service_name": "Microsoft Graph",
  "auth_url": "https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize",
  "token_url": "https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token",
  "client_id": "your_app_id",
  "client_secret": "your_app_secret",
  "scopes": ["User.Read", "Files.Read"]
}
```

---

## 🔄 Token Lifecycle

- **Initial Authorization**: User grants permission via browser
- **Token Storage**: Tokens cached in DynamoDB per node ID
- **Automatic Refresh**: Expired tokens refreshed using refresh_token
- **Session Persistence**: Tokens persist across workflow executions

---

## 🔒 Security Features

- **State Parameter**: CSRF protection with encoded state data
- **Secure Storage**: Tokens stored in DynamoDB with encryption
- **Token Rotation**: Supports refresh token rotation
- **Tenant Isolation**: Node ID-based token isolation

---

## 💡 Use Cases

- **User Data Access**: Access user's Google Drive, Dropbox, etc.
- **Social Login**: Authenticate users with Google, Facebook, GitHub
- **Calendar Integration**: Access user's calendar events
- **Email Access**: Read/send emails on user's behalf

---

## ⚠️ Notes

- **Callback Configuration**: Requires callback URL configured in OAuth app
- **Provider-Specific**: Different providers have different scope formats
- **Button Integration**: Works with UI button to initiate OAuth flow
- **Refresh Handling**: Automatically refreshes tokens when expired
