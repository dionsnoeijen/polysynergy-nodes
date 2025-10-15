# 🔄 OAuth Refresh Token Node

The `OAuth Refresh Token` node implements the OAuth 2.0 Refresh Token Grant flow. Exchanges a refresh token for a new access token without requiring user interaction.

---

## 📂 Category

**auth**

---

## ⚙️ Inputs

| Name           | Type   | Required | Description                              |
|----------------|--------|----------|------------------------------------------|
| client_id      | str    | ✅        | OAuth client identifier                  |
| client_secret  | str    | ✅        | OAuth client secret                      |
| token_url      | str    | ✅        | OAuth token endpoint URL                 |
| refresh_token  | str    | ✅        | Refresh token to exchange                |
| scope          | str    | ❌        | OAuth scope (some providers require)     |

---

## 🔌 Outputs

| Name              | Type   | Description                              |
|-------------------|--------|------------------------------------------|
| access_token      | str    | New OAuth access token                   |
| new_refresh_token | str    | New refresh token (if provider issues)   |
| token_type        | str    | Token type (usually 'Bearer')            |
| expires_in        | int    | Token expiry time in seconds             |

---

## 🔀 Flow Control

| Path        | Description                                 |
|-------------|---------------------------------------------|
| true_path   | Token refreshed successfully (Bearer token) |
| false_path  | Token refresh failed (error details)        |

---

## ✅ Example Usage

### Basic Refresh Flow:
```json
{
  "client_id": "your_client_id",
  "client_secret": "your_client_secret",
  "token_url": "https://oauth.provider.com/token",
  "refresh_token": "1//0hWJx..."
}
```

**Output:** `"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."`

---

## 🔄 Token Rotation

### Single-Use Refresh Tokens:
Some providers (Google, Microsoft) issue a **new** refresh token with each refresh:
```json
{
  "access_token": "new_access_token",
  "refresh_token": "new_refresh_token",  // ← Use this next time
  "expires_in": 3600
}
```

### Reusable Refresh Tokens:
Some providers keep the same refresh token:
```json
{
  "access_token": "new_access_token",
  // No new refresh_token - keep using the old one
  "expires_in": 3600
}
```

---

## 🔒 Security Features

- **Token Storage**: Saves new tokens to DynamoDB automatically
- **Token Rotation**: Handles both single-use and reusable refresh tokens
- **Expiry Management**: Tracks token expiry times
- **Automatic Fallback**: Stores new refresh token if provided

---

## 💡 Use Cases

- **Background Jobs**: Refresh tokens for long-running tasks
- **Scheduled Workflows**: Automated workflows requiring fresh tokens
- **Token Renewal**: Keep access tokens valid without user interaction
- **Session Extension**: Extend user sessions automatically

---

## 📊 Refresh Token Lifecycle

```
Initial Auth
    ↓
Access Token (expires 1h) + Refresh Token (expires 30d)
    ↓
Access Token Expires
    ↓
Use Refresh Token → Get New Access Token
    ↓
[Provider may issue new refresh token]
    ↓
Continue with new tokens
```

---

## ⚠️ Notes

- **No User Interaction**: Completely automated token renewal
- **Refresh Token Expiry**: Refresh tokens also expire (typically 30-90 days)
- **Rotation Support**: Handles both token rotation patterns
- **Provider Differences**: Token rotation behavior varies by provider
- **Storage Critical**: Always store new refresh tokens when provided
- **Scope Changes**: Some providers require scope parameter on refresh

---

## 🔗 Integration Pattern

```
Authorization Code Node
    ↓
Store refresh_token
    ↓
[Time passes, access_token expires]
    ↓
OAuth Refresh Token Node
    ↓
New access_token + (maybe) new refresh_token
    ↓
Store new tokens
```
