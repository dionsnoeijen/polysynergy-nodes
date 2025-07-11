# JWT Generator

⚠️ **Warning:** This node provides full control over JWT structure and token exchange. Use with care and always follow secure coding practices when dealing with authentication and secrets.

This node allows you to programmatically create a JWT (JSON Web Token) and exchange it for an access token using OAuth 2.0 JWT Bearer Token Flow.

## Inputs

### `jwt_claims` (dict)
- Claims to include in the JWT payload.
- **Required keys:**  
  - `iss`: Issuer (e.g., service account email)  
  - `aud`: Audience (typically the token URI)
- **Optional:**  
  - `sub`: Subject  
  - `scope`: Requested scopes  
  - `exp_time`: Custom expiration duration (defaults to 3600 seconds)

### `exchange_config` (dict)
- Configuration for exchanging the signed JWT for an access token.
- **Required keys:**  
  - `private_key`: The RSA private key to sign the JWT  
  - `token_uri`: The OAuth 2.0 token endpoint to exchange the JWT
- **Optional:**  
  - `grant_type`: Defaults to `urn:ietf:params:oauth:grant-type:jwt-bearer`

## Outputs

### `access_token` (str)
- The returned access token from the token exchange.

### `expires_at` (int)
- Unix timestamp when the token expires.

## Path Outputs

- `true_path`: Returns the access token on success.
- `false_path`: Returns an error dict on failure.

## Example Usage

```json
"jwt_claims": {
  "iss": "your-service-account@example.com",
  "aud": "https://oauth2.googleapis.com/token",
  "scope": "https://www.googleapis.com/auth/cloud-platform"
}
```

```json
"exchange_config": {
  "private_key": "-----BEGIN PRIVATE KEY-----\n...",
  "token_uri": "https://oauth2.googleapis.com/token"
}
```

## Reference

- 📖 JWT Bearer Token Flow: [RFC 7523](https://datatracker.ietf.org/doc/html/rfc7523)