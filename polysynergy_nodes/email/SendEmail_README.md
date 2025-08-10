# Send Email

Sends an email using an SMTP server with enhanced validation and async execution.  
Supports both plain text and HTML content, with options for CC, BCC, attachments, and TLS.

## **Category:** Email

## **Description**
The **Send Email** node sends an email using an external SMTP server with comprehensive validation and error handling. The node executes asynchronously to prevent blocking during email operations.

Key features:
- **Async Execution:** Non-blocking SMTP operations
- **Email Validation:** RFC-compliant email address validation
- **Attachment Support:** Base64-encoded file attachments with size limits
- **Enhanced Security:** Input validation and size limits
- **Comprehensive Error Handling:** Detailed error messages and validation

## **Variables**

### **Input Variables**

| Name              | Type           | Required | Default | Description |
|-------------------|----------------|----------|---------|-------------|
| `smtp_host`       | str            | ✅       | -       | SMTP server hostname (e.g., "smtp.gmail.com") |
| `smtp_port`       | int            | ❌       | 587     | SMTP server port (usually 587 for TLS, 465 for SSL) |
| `smtp_user`       | str            | ✅       | -       | SMTP username/email for authentication |
| `smtp_password`   | str            | ✅       | -       | SMTP password (connect from secret node) |
| `smtp_use_tls`    | bool           | ❌       | true    | Enable TLS encryption (recommended) |
| `smtp_timeout`    | int            | ❌       | 30      | Connection timeout in seconds |
| `sender`          | str            | ✅       | -       | Sender address (e.g., "John Doe <john@example.com>") |
| `recipient`       | str            | ✅       | -       | Primary recipient email address |
| `cc`              | str            | ❌       | ""      | CC recipients (comma-separated) |
| `bcc`             | str            | ❌       | ""      | BCC recipients (comma-separated) |
| `subject`         | str            | ✅       | -       | Email subject line (max 998 characters) |
| `body`            | str            | ✅       | -       | Email body content (max 1MB) |
| `is_html`         | bool           | ❌       | true    | Whether body contains HTML content |
| `attachments`     | list[dict]/dict| ❌       | null    | File attachments (base64 encoded) |

### **Attachment Format**
Each attachment should be a dict with:
```json
{
  "filename": "document.pdf",
  "content": "base64-encoded-content",
  "mimetype": "application/pdf"
}
```

### **Output Variables**
*None - uses flow control paths only*

## **Flow Control**

| Name         | Description |
|--------------|-------------|
| `true_path`  | Triggered when the email is successfully sent. |
| `false_path` | Triggered when sending the email fails. Contains an error dict. |

## **How It Works**
1. **Validation Phase:**
   - Validates SMTP configuration completeness
   - Validates email address formats (sender, recipient, CC, BCC)
   - Validates content lengths (subject max 998 chars, body max 1MB)
   - Validates attachment sizes (max 25MB per file, 50MB total)

2. **Message Building Phase (Async):**
   - Creates email message structure in background thread
   - Processes and validates base64 attachments
   - Builds MIME message with proper headers

3. **Sending Phase (Async):**
   - Establishes SMTP connection with timeout
   - Authenticates with provided credentials
   - Sends email to all recipients (To, CC, BCC)
   - Properly closes connection

4. **Result:**
   - Routes to `true_path` on successful send
   - Routes to `false_path` with detailed error info on failure

---

## **Validation Rules**

### **Email Addresses**
- Must follow RFC 5322 format: `user@domain.tld`
- Supports name format: `"John Doe" <john@domain.tld>`
- CC/BCC lists are comma-separated and individually validated

### **Content Limits**
- **Subject:** Max 998 characters (RFC 5322 limit)
- **Body:** Max 1MB total size
- **Attachments:** Max 25MB per file, 50MB total

### **SMTP Configuration**
- `smtp_host`, `smtp_user`, and `smtp_password` are required
- Connection timeout prevents hanging operations
- TLS encryption is enabled by default for security

---

## **Example Usage**

### **Basic Email**
```yaml
smtp_host: "smtp.gmail.com"
smtp_port: 587
smtp_user: "your-app@gmail.com"
smtp_password: "app-specific-password"
sender: "MyApp <your-app@gmail.com>"
recipient: "user@example.com"
subject: "Welcome to MyApp!"
body: "<h1>Welcome!</h1><p>Thanks for joining us.</p>"
is_html: true
```

### **Email with Attachments**
```yaml
smtp_host: "smtp.example.com"
sender: "Reports <reports@company.com>"
recipient: "manager@company.com"
subject: "Monthly Report"
body: "Please find the monthly report attached."
attachments:
  - filename: "report.pdf"
    content: "JVBERi0xLjQKJeLjz9MKMSAwIG9iago8PA..."
    mimetype: "application/pdf"
```

### **Multi-Recipient Email**
```yaml
recipient: "primary@example.com"
cc: "manager@example.com, team@example.com"
bcc: "archive@example.com"
subject: "Project Update"
body: "The project status has been updated..."
```

---

## **Error Handling**

The node provides detailed error messages for common issues:

- **`"SMTP config missing"`** - Missing required SMTP settings
- **`"Invalid recipient email: xxx"`** - Email format validation failed
- **`"Invalid email addresses: xxx, yyy"`** - CC/BCC validation failed
- **`"Subject line too long"`** - Subject exceeds 998 characters
- **`"Email body too long"`** - Body exceeds 1MB limit
- **`"Attachment 'file.pdf' exceeds 25MB limit"`** - Attachment too large
- **`"Total attachment size exceeds 50MB limit"`** - All attachments too large
- **`"Connection failed"`** - SMTP server unreachable
- **`"Authentication failed"`** - Invalid SMTP credentials

---

## **Use Cases**
✅ **Transactional Emails** - Order confirmations, password resets  
✅ **Notifications** - System alerts, status updates  
✅ **Reports** - Automated reports with PDF attachments  
✅ **Marketing** - Newsletter distribution (small scale)  
✅ **Internal Communications** - Team notifications, alerts  

---

## **Best Practices**

### **Security**
- Always use TLS encryption (`smtp_use_tls: true`)
- Store SMTP passwords in secret nodes
- Use app-specific passwords for Gmail/Outlook
- Validate sender domain ownership (SPF/DKIM)

### **Performance**
- Use reasonable timeouts (30-60 seconds)
- Avoid large attachments when possible
- Consider email provider rate limits
- Use the Enhanced Email node for multiple providers

### **Reliability**
- Test SMTP configuration before deployment
- Handle bounced emails appropriately
- Monitor email sending success rates
- Have fallback email providers ready

---

📧 **Use this node to send reliable, validated emails through any SMTP provider with comprehensive error handling and security features.**