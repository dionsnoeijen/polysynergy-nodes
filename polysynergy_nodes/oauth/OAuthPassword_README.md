# 🔑 OAuth Password Node

The `OAuth Password` node implements the OAuth 2.0 Resource Owner Password Credentials Grant flow. Directly exchanges username and password for access tokens.

---

## 📂 Category

**auth**

---

## ⚠️ **SECURITY WARNING**

This grant type is **NOT RECOMMENDED** for most applications because:
- Exposes user credentials to the application
- No consent screen or scope approval
- Bypasses browser-based security features
- Only use when other flows are not possible

**Preferred alternatives**: Authorization Code or Client Credentials flows

---

## ⚙️ Inputs

| Name           | Type   | Required | Description                              |
|----------------|--------|----------|------------------------------------------|
| token_url      | str    | ✅        | OAuth token endpoint URL                 |
| client_id      | str    | ✅        | OAuth client identifier                  |
| client_secret  | str    | ✅        | OAuth client secret                      |
| username       | str    | ✅        | Resource owner username                  |
| password       | str    | ✅        | Resource owner password                  |
| scope          | str    | ❌        | OAuth scope (optional)                   |

---

## 🔌 Outputs

| Name           | Type   | Description                              |
|----------------|--------|------------------------------------------|
| access_token   | str    | OAuth access token                       |
| refresh_token  | str    | OAuth refresh token (if provided)        |
| token_type     | str    | Token type (usually 'Bearer')            |
| expires_in     | int    | Token expiry time in seconds             |

---

## 🔀 Flow Control

| Path        | Description                                 |
|-------------|---------------------------------------------|
| true_path   | Authentication successful (Bearer token)    |
| false_path  | Authentication failed (error details)       |

---

## ✅ Example Usage

### Basic Password Flow:
```json
{
  "token_url": "https://oauth.provider.com/token",
  "client_id": "your_client_id",
  "client_secret": "your_client_secret",
  "username": "user@example.com",
  "password": "user_password",
  "scope": "api.read api.write"
}
```

**Output:** `"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."`

---

## 🔄 Token Management

- **Direct Exchange**: Username/password directly exchanged for tokens
- **Refresh Token**: Some providers return refresh tokens
- **Token Storage**: Tokens cached in DynamoDB (if configured)
- **No User Interaction**: Completely automated flow

---

## 🔒 Security Considerations

### Risks:
- ❌ Application has access to user credentials
- ❌ Credentials transmitted directly to application
- ❌ No multi-factor authentication support
- ❌ No consent screen or scope approval

### When to Use:
- ✅ Highly trusted first-party applications only
- ✅ Legacy systems requiring this flow
- ✅ Migration from basic auth to OAuth
- ✅ Internal tools with limited alternatives

---

## 💡 Use Cases

- **Legacy System Migration**: Transitioning from basic auth
- **First-Party Mobile Apps**: Highly trusted mobile applications
- **Internal Tools**: Corporate internal applications
- **Development/Testing**: Testing environments only

---

## ⚠️ Notes

- **Deprecated**: This flow is deprecated in OAuth 2.1
- **Provider Support**: Not all providers support this grant type
- **Use Secrets**: Never hardcode passwords in flows
- **Prefer Alternatives**: Use Authorization Code flow when possible
- **Refresh Tokens**: Not all providers issue refresh tokens with this flow
