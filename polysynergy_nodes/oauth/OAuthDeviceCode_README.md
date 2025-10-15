# 📺 OAuth Device Code Node

The `OAuth Device Code` node implements the OAuth 2.0 Device Code Grant flow for devices with limited input capability (smart TVs, IoT devices, CLI tools). Users authenticate on a separate device.

---

## 📂 Category

**auth**

---

## ⚙️ Inputs

| Name               | Type   | Required | Description                              |
|--------------------|--------|----------|------------------------------------------|
| device_auth_url    | str    | ✅        | Device authorization endpoint URL        |
| token_url          | str    | ✅        | OAuth token endpoint URL                 |
| client_id          | str    | ✅        | OAuth client identifier                  |
| client_secret      | str    | ❌        | OAuth client secret (optional)           |
| scope              | str    | ❌        | OAuth scope                              |
| device_code        | str    | ❌        | Device code for polling (2nd call)       |

---

## 🔌 Outputs

### Device Authorization Outputs:
| Name                      | Type   | Description                              |
|---------------------------|--------|------------------------------------------|
| user_code                 | str    | Code for user to enter                   |
| verification_url          | str    | URL where user authenticates             |
| verification_url_complete | str    | Pre-filled verification URL              |
| device_code_output        | str    | Device code for polling                  |
| expires_in_device         | int    | Device code expiry (seconds)             |
| interval                  | int    | Minimum polling interval (seconds)       |

### Token Outputs:
| Name           | Type   | Description                              |
|----------------|--------|------------------------------------------|
| access_token   | str    | OAuth access token                       |
| refresh_token  | str    | OAuth refresh token                      |
| token_type     | str    | Token type (usually 'Bearer')            |
| expires_in     | int    | Access token expiry (seconds)            |

---

## 🔀 Flow Control

| Path          | Description                                 |
|---------------|---------------------------------------------|
| true_path     | Device authorization info or token obtained |
| false_path    | Request failed (error details)              |
| pending_path  | User authorization pending (keep polling)   |

---

## 📋 Device Flow Sequence

### Step 1: Request Device Code
```json
{
  "client_id": "your_client_id",
  "device_auth_url": "https://oauth.provider.com/device",
  "token_url": "https://oauth.provider.com/token",
  "scope": "api.read"
}
```

**Output:**
```json
{
  "user_code": "ABCD-1234",
  "verification_url": "https://provider.com/device",
  "device_code": "GmRhmhc...",
  "expires_in": 1800,
  "interval": 5
}
```

### Step 2: User Authorizes
User visits `verification_url` and enters `user_code`

### Step 3: Poll for Token
```json
{
  "client_id": "your_client_id",
  "token_url": "https://oauth.provider.com/token",
  "device_code": "GmRhmhc..."
}
```

**Pending Response:**
```json
{
  "action": "authorization_pending",
  "message": "User has not yet authorized the device"
}
```

**Success Response:**
```json
"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

## 🔄 Polling Strategy

- **Initial Interval**: Use `interval` from device authorization response
- **Slow Down**: If `slow_down` error received, increase polling interval
- **Pending**: Keep polling until user authorizes or code expires
- **Expiry**: Device code expires after `expires_in_device` seconds

---

## 💡 Use Cases

- **Smart TV Apps**: OAuth for TV applications
- **CLI Tools**: Command-line tools requiring OAuth
- **IoT Devices**: Devices without browsers or keyboards
- **Embedded Systems**: Limited input capability devices

---

## ⚠️ Notes

- **Two-Step Process**: First get device code, then poll for token
- **User Experience**: Display verification URL and user code to user
- **Polling Interval**: Respect the `interval` parameter to avoid rate limiting
- **Code Expiry**: Device codes typically expire in 15-30 minutes
- **Slow Down**: Provider may request slower polling if too frequent
