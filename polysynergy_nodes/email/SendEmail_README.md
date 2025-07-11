# Send Email

Sends an email using a provided SMTP server.  
Supports both plain text and HTML content, with options for CC, BCC, and TLS.

## **Category:** Email

## **Description**
The **Send Email** node sends an email using an external SMTP server.  
It supports full SMTP configuration, including custom ports, TLS, and authentication.

The node auto-detects if it's running in AWS Lambda or locally:
- **In Lambda:** uses provided SMTP credentials directly.
- **Locally (Django):** uses Django's configured email backend.

## **Variables**

| Name            | Type   | Input | Output | Description |
|-----------------|--------|-------|--------|-------------|
| `smtp_host`     | str    | ✅     | ❌      | SMTP server host. Required in Lambda. |
| `smtp_port`     | int    | ✅     | ❌      | SMTP server port (default is 587). |
| `smtp_user`     | str    | ✅     | ❌      | SMTP login user. Required in Lambda. |
| `smtp_password` | str    | ✅     | ❌      | SMTP password (usually from a secret node). Required in Lambda. |
| `smtp_use_tls`  | bool   | ✅     | ❌      | Whether to use TLS (default is `true`). |
| `sender`        | str    | ✅     | ❌      | Sender address (e.g. "Example <no-reply@example.com>"). |
| `recipient`     | str    | ✅     | ❌      | Recipient email address. |
| `cc`            | str    | ✅     | ❌      | Optional CC address(es), comma-separated. |
| `bcc`           | str    | ✅     | ❌      | Optional BCC address(es), comma-separated. |
| `subject`       | str    | ✅     | ❌      | Subject of the email. |
| `body`          | str    | ✅     | ❌      | Body of the email. Can be plain text or HTML. |
| `is_html`       | bool   | ✅     | ❌      | Whether the email is HTML-formatted. |

## **Flow Control**

| Name         | Description |
|--------------|-------------|
| `true_path`  | Triggered when the email is successfully sent. |
| `false_path` | Triggered when sending the email fails. Contains an error dict. |

## **How It Works**
1. Detects whether it's running inside AWS Lambda.
2. Builds and sends an email based on the provided SMTP config:
   - In Lambda: manually sets up and uses `smtplib`.
   - Locally: uses Django's built-in `EmailMessage`.
3. Routes to:
   - `true_path` on success
   - `false_path` with error info on failure

---

## **Example Usage**

### **Input**
- `smtp_host` = `"smtp.example.com"`
- `smtp_port` = `587`
- `smtp_user` = `"no-reply@example.com"`
- `smtp_password` = `"••••••••"`
- `sender` = `"Example <no-reply@example.com>"`
- `recipient` = `"john@example.com"`
- `subject` = `"Welcome!"`
- `body` = `"<h1>Hi John</h1><p>Thanks for joining.</p>"`
- `is_html` = `true`

### **Output**
- `true_path` = `true`

---

## **Error Handling**
- Missing SMTP configuration (in Lambda) will trigger `false_path`.
- SMTP errors (auth failure, unreachable host, etc.) are passed as strings.
- Unexpected exceptions return their message in `false_path`.

---

## **Use Cases**
✔ Sending confirmation emails  
✔ Notifying users of changes  
✔ Triggered alerts or workflow updates

---

📧 **Use this node to send custom emails from your flows, using any SMTP provider.**