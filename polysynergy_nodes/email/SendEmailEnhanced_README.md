# Send Email Enhanced

Advanced email sending node with multi-provider support (SMTP and AWS SES).  
Features comprehensive validation, async execution, and provider-specific optimizations.

## **Category:** Email

## **Description**
The **Send Email Enhanced** node is a next-generation email sending solution that supports multiple email providers with automatic provider-specific validation and optimization. Built with async architecture for high performance and reliability.

### **Key Features**
- **Multi-Provider Support:** SMTP servers and AWS Simple Email Service (SES)
- **Async Execution:** Non-blocking operations for high performance
- **Smart Validation:** Provider-specific size limits and validation rules
- **Enhanced Addressing:** Support for named email addresses
- **Message Tracking:** Returns message IDs and provider information
- **Comprehensive Error Handling:** Detailed error reporting with context

### **Supported Providers**
- **SMTP:** Any SMTP server (Gmail, Outlook, SendGrid, Mailgun, etc.)
- **AWS SES:** Amazon Simple Email Service with raw email support

---

## **Variables**

### **Provider Configuration**

| Name               | Type | Required | Default | Description |
|--------------------|------|----------|---------|-------------|
| `provider_type`    | str  | ❌       | "smtp"  | Email provider: "smtp" or "aws_ses" |

### **SMTP Configuration** *(when provider_type = "smtp")*

| Name               | Type | Required | Default | Description |
|--------------------|------|----------|---------|-------------|
| `smtp_host`        | str  | ✅       | -       | SMTP server hostname |
| `smtp_port`        | int  | ❌       | 587     | SMTP server port |
| `smtp_user`        | str  | ✅       | -       | SMTP username |
| `smtp_password`    | str  | ✅       | -       | SMTP password (from secret node) |
| `smtp_use_tls`     | bool | ❌       | true    | Enable TLS encryption |
| `smtp_timeout`     | int  | ❌       | 30      | Connection timeout (seconds) |

### **AWS SES Configuration** *(when provider_type = "aws_ses")*

| Name                    | Type | Required | Default    | Description |
|-------------------------|------|----------|------------|-------------|
| `aws_region`            | str  | ❌       | "us-east-1"| AWS region |
| `aws_access_key_id`     | str  | ❌       | ""         | AWS Access Key (optional if using IAM) |
| `aws_secret_access_key` | str  | ❌       | ""         | AWS Secret Key (optional if using IAM) |

### **Email Content**

| Name          | Type           | Required | Default | Description |
|---------------|----------------|----------|---------|-------------|
| `sender`      | str            | ✅       | -       | Sender address with optional name |
| `recipient`   | str            | ✅       | -       | Primary recipient address |
| `cc`          | str            | ❌       | ""      | CC recipients (comma-separated) |
| `bcc`         | str            | ❌       | ""      | BCC recipients (comma-separated) |
| `subject`     | str            | ✅       | -       | Email subject line |
| `body`        | str            | ✅       | -       | Email body content |
| `is_html`     | bool           | ❌       | true    | Whether body is HTML formatted |
| `attachments` | list[dict]     | ❌       | null    | File attachments (base64 encoded) |

### **Output Variables**

| Name           | Type | Description |
|----------------|------|-------------|
| `message_id`   | str  | Unique message identifier from provider |
| `provider_used`| str  | Name of the email provider that was used |

---

## **Provider-Specific Features**

### **SMTP Provider**
- **Size Limits:** 25MB per attachment, 50MB total
- **Features:** Full MIME support, custom headers, TLS encryption
- **Best For:** Custom SMTP servers, high-volume sending, full control

### **AWS SES Provider**
- **Size Limits:** 10MB per attachment, 10MB total (AWS limit)
- **Features:** Raw email support, automatic bounce handling, reputation management
- **Authentication:** Uses IAM roles or access keys
- **Best For:** AWS-integrated applications, high deliverability, built-in analytics

---

## **Address Formats**

The enhanced node supports both simple and named email address formats:

```yaml
# Simple format
sender: "noreply@example.com"
recipient: "user@example.com"

# Named format  
sender: "MyApp Support <support@example.com>"
recipient: "John Doe <john.doe@example.com>"

# Mixed lists
cc: "manager@example.com, Team Lead <lead@example.com>"
bcc: "archive@example.com, Admin <admin@example.com>"
```

---

## **Example Usage**

### **SMTP Configuration**
```yaml
provider_type: "smtp"
smtp_host: "smtp.gmail.com"
smtp_port: 587
smtp_user: "myapp@gmail.com"
smtp_password: "app-specific-password"
sender: "MyApp <myapp@gmail.com>"
recipient: "customer@example.com"
subject: "Order Confirmation"
body: "<h1>Thank you for your order!</h1><p>Order #12345 has been confirmed.</p>"
is_html: true
```

### **AWS SES Configuration**
```yaml
provider_type: "aws_ses"
aws_region: "us-east-1"
sender: "orders@mycompany.com"
recipient: "customer@example.com"
cc: "sales@mycompany.com"
subject: "Order Shipped"
body: "Your order has been shipped and will arrive within 2-3 business days."
```

### **Email with Attachments**
```yaml
provider_type: "smtp"
smtp_host: "smtp.example.com"
# ... other SMTP config ...
subject: "Monthly Report"
body: "Please review the attached monthly report."
attachments:
  - filename: "report.pdf"
    content: "JVBERi0xLjQKJeLjz9MKMSAwIG9iago..."
    mimetype: "application/pdf"
  - filename: "data.csv"
    content: "bmFtZSxhZ2UKSm9obiwzMAoKYW5lLDI1"
    mimetype: "text/csv"
```

---

## **Flow Control**

| Path         | Condition | Description |
|--------------|-----------|-------------|
| `true_path`  | Success   | Email sent successfully, `message_id` and `provider_used` are set |
| `false_path` | Error     | Email sending failed, contains detailed error information |

---

## **Validation & Error Handling**

### **Email Address Validation**
- RFC 5322 compliant format checking
- Support for international domain names
- Named address parsing and validation
- Duplicate recipient detection

### **Content Validation**
- Subject line length (max 998 characters)
- Body size limits (provider-specific)
- Attachment size validation (provider-specific)
- MIME type validation

### **Provider-Specific Validation**
- SMTP: Validates connection parameters and TLS settings
- AWS SES: Validates AWS credentials and region settings
- Automatic size limit adjustment based on provider capabilities

### **Common Error Messages**

#### **Configuration Errors**
- `"SMTP configuration missing (host, user, password required)"`
- `"Unsupported provider type: xxx"`
- `"AWS SES configuration invalid"`

#### **Validation Errors**  
- `"Invalid recipient email: xxx"`
- `"Invalid sender email: xxx"`
- `"Subject line too long (max 998 characters)"`
- `"Email body too long (max 1MB)"`

#### **Attachment Errors**
- `"Attachment 'file.pdf' (size bytes) exceeds provider limit of limit bytes"`
- `"Total attachment size (size bytes) exceeds provider limit of limit bytes"`
- `"Invalid attachment content for 'file.pdf': error"`

#### **Provider Errors**
- `"Connection failed"` (SMTP)
- `"Authentication failed"` (SMTP)
- `"Access denied"` (AWS SES)
- `"Region not supported"` (AWS SES)

---

## **Provider Selection Guide**

### **Choose SMTP When:**
- Using existing email infrastructure
- Need larger attachment limits (25MB vs 10MB)
- Require custom SMTP features
- Working with third-party email services (SendGrid, Mailgun)
- Need full control over email headers and routing

### **Choose AWS SES When:**
- Already using AWS services
- Need high deliverability rates
- Want built-in bounce/complaint handling
- Require detailed sending statistics
- Need integration with other AWS services
- Want managed email reputation

---

## **Best Practices**

### **Provider Configuration**
- Test provider connections before deployment
- Use IAM roles for AWS SES when possible
- Store credentials securely in secret nodes
- Configure appropriate timeouts for your use case

### **Email Content**
- Validate email addresses at input time
- Use appropriate MIME types for attachments
- Keep attachment sizes reasonable
- Include both HTML and plain text versions when possible

### **Error Handling**
- Always handle `false_path` scenarios
- Log provider responses for debugging
- Implement retry logic for transient failures
- Monitor email sending success rates

### **Security**
- Always use TLS for SMTP connections
- Regularly rotate email credentials
- Validate sender domain ownership (SPF/DKIM)
- Monitor for abuse and spam complaints

---

## **Use Cases**

### **Transactional Emails**
- Order confirmations and receipts
- Password reset notifications
- Account verification emails
- Shipping notifications

### **Business Communications**
- Automated reports with attachments
- Team notifications and alerts  
- Customer support responses
- Internal workflow notifications

### **Marketing & Engagement**
- Welcome email sequences
- Newsletter distribution
- Event invitations
- Product announcements

---

📧 **Use the Enhanced Email node for production-grade email delivery with multiple provider options, comprehensive validation, and enterprise-level reliability.**