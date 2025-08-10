# Email Nodes

Professional email sending and attachment handling nodes with multi-provider support, async execution, and comprehensive validation.

## **Overview**

The email module provides a complete solution for sending emails in PolySynergy workflows. Built with modern async architecture, the nodes support multiple email providers, comprehensive validation, and production-ready error handling.

### **Available Nodes**

| Node | Description | Best For |
|------|-------------|----------|
| **Send Email** | SMTP-based email sending with validation | Standard email sending, existing SMTP infrastructure |
| **Send Email Enhanced** | Multi-provider email with SMTP and AWS SES | Production applications, provider flexibility |
| **Create Email Attachment** | File-to-attachment converter | Adding files to emails, document distribution |

---

## **Key Features**

### **🚀 Async Architecture**
- Non-blocking email operations
- Background file processing
- Concurrent attachment handling
- High-performance execution

### **📧 Multi-Provider Support**
- **SMTP:** Any SMTP server (Gmail, Outlook, SendGrid, Mailgun, etc.)
- **AWS SES:** Amazon Simple Email Service with advanced features
- Provider-specific optimizations and limits

### **✅ Comprehensive Validation**
- RFC 5322 compliant email address validation
- Content size limits (subject, body, attachments)
- MIME type validation and selection
- Provider-specific constraint checking

### **🔒 Security & Reliability**
- TLS encryption for SMTP connections
- Secure credential handling
- Input sanitization and validation
- Detailed error reporting and logging

### **📎 Advanced Attachment Support**
- Base64 encoding with size validation
- Extensive MIME type support
- Multiple attachment handling
- Memory-efficient file processing

---

## **Quick Start**

### **Basic Email Sending**
```yaml
# Simple email with SMTP
Send Email:
  smtp_host: "smtp.gmail.com"
  smtp_user: "your-app@gmail.com" 
  smtp_password: "[from secret node]"
  sender: "MyApp <your-app@gmail.com>"
  recipient: "user@example.com"
  subject: "Welcome!"
  body: "<h1>Thanks for joining!</h1>"
```

### **Email with Attachments**
```yaml
# Create attachment
Create Email Attachment:
  filepath: "/reports/monthly.pdf"
  filename: "Monthly Report.pdf"
  mimetype: "application/pdf"

# Send email with attachment  
Send Email:
  # ... SMTP config ...
  attachments: "[attachment from previous node]"
```

### **Multi-Provider Setup**
```yaml
# Enhanced email with provider selection
Send Email Enhanced:
  provider_type: "aws_ses"  # or "smtp"
  aws_region: "us-east-1"
  sender: "notifications@myapp.com"
  recipient: "user@example.com"
  subject: "Order Confirmation"
  body: "Your order has been confirmed."
```

---

## **Provider Comparison**

### **SMTP Provider**
✅ **Pros:**
- Works with any SMTP server
- Larger attachment limits (25MB per file, 50MB total)
- Full control over headers and configuration
- No cloud service dependencies

❌ **Cons:**
- Requires SMTP server maintenance
- Manual bounce/complaint handling
- No built-in analytics
- Potential deliverability issues

### **AWS SES Provider**  
✅ **Pros:**
- High deliverability rates
- Built-in bounce/complaint handling
- Detailed sending statistics
- Managed infrastructure and reputation
- Automatic scaling

❌ **Cons:**
- Smaller attachment limits (10MB total)
- Requires AWS account and setup
- Region-specific service availability
- Additional AWS costs

---

## **Architecture Overview**

```
Email Workflow Architecture:

[File System] ──┐
                │
[Variables] ────┼──> [Create Email Attachment] ──┐
                │                                 │
[Secrets] ──────┼──> [Send Email / Enhanced] ────┼──> [Success Path]
                │                                 │
[Templates] ────┘                                 └──> [Error Path]

Provider Abstraction Layer:
├── SMTP Provider (smtplib)
├── AWS SES Provider (boto3)
└── [Future providers...]
```

### **Key Components**

1. **Node Layer:** User-facing nodes with input validation
2. **Provider Layer:** Abstract email provider interface  
3. **Transport Layer:** Protocol-specific implementations (SMTP, AWS API)
4. **Validation Layer:** Email format, size, and content validation
5. **Error Handling:** Comprehensive error capture and reporting

---

## **Validation Rules**

### **Email Addresses**
- Must follow RFC 5322 format: `user@domain.tld`
- Support for named format: `"John Doe" <john@domain.tld>`
- Multiple recipients in CC/BCC (comma-separated)
- Duplicate detection and prevention

### **Content Limits**

| Component | SMTP Limit | AWS SES Limit | Validation |
|-----------|------------|---------------|------------|
| Subject | 998 chars | 998 chars | RFC 5322 compliant |
| Body | 1MB | 1MB | Size + encoding check |
| Attachment (each) | 25MB | 10MB | Provider-specific |
| Total Size | 50MB | 10MB | Provider-specific |

### **File Attachments**
- Supported file types via MIME type selection
- Base64 encoding validation
- File existence and permission checks
- Empty file detection

---

## **Error Handling**

### **Error Categories**
1. **Configuration Errors:** Missing or invalid provider settings
2. **Validation Errors:** Invalid email addresses, content too long
3. **Transport Errors:** Network issues, authentication failures  
4. **Provider Errors:** Service-specific limitations or failures

### **Error Response Format**
```json
{
  "error": "Detailed error message",
  "error_code": "ERROR_TYPE",
  "context": {
    "provider": "smtp",
    "recipient": "user@example.com",
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

### **Recovery Strategies**
- Automatic retry for transient failures
- Provider fallback mechanisms
- Graceful degradation for non-critical errors
- Comprehensive logging for debugging

---

## **Best Practices**

### **🔐 Security**
- **Credential Management:** Always use secret nodes for passwords and keys
- **TLS Encryption:** Enable TLS for all SMTP connections
- **Access Control:** Use IAM roles for AWS SES when possible
- **Domain Authentication:** Configure SPF, DKIM, and DMARC records

### **⚡ Performance**
- **Async Operations:** Leverage async architecture for high throughput
- **Batch Processing:** Group multiple emails when possible
- **Connection Reuse:** Use provider connection pooling
- **Size Optimization:** Compress large attachments when appropriate

### **🛠️ Reliability**
- **Error Handling:** Always handle false_path scenarios
- **Monitoring:** Track email delivery success rates
- **Testing:** Validate configurations in non-production environments
- **Fallbacks:** Have backup providers configured

### **📊 Observability**
- **Logging:** Log all email operations and outcomes
- **Metrics:** Monitor send rates, success rates, and errors
- **Alerting:** Set up alerts for delivery failures
- **Auditing:** Track email sending for compliance

---

## **Integration Patterns**

### **Transactional Emails**
```yaml
User Registration -> Generate Welcome Email -> Send Email -> Log Activity
```

### **Notification System**
```yaml
Event Trigger -> Template Processing -> Send Email Enhanced -> Update Status
```

### **Report Distribution**
```yaml
Generate Report -> Create PDF -> Create Attachment -> Send Email -> Archive
```

### **Bulk Email Processing**  
```yaml
User List -> For Each User -> Personalize Content -> Send Email -> Track Results
```

---

## **Troubleshooting Guide**

### **Common Issues**

#### **SMTP Authentication Failures**
- Verify username and password
- Check if 2FA requires app-specific passwords
- Confirm SMTP server settings (host, port, TLS)
- Test connection with email client first

#### **AWS SES Access Denied**  
- Verify IAM permissions for SES actions
- Check if sending domain is verified
- Confirm AWS region configuration
- Validate recipient email addresses (sandbox mode)

#### **Attachment Issues**
- Check file path and permissions
- Verify file size against provider limits
- Confirm MIME type selection
- Test base64 encoding manually

#### **Delivery Problems**
- Monitor bounce and complaint rates
- Check sender domain reputation
- Verify email content for spam indicators
- Test with different recipient domains

### **Debug Steps**
1. **Test Provider Connection:** Use validate_connection methods
2. **Check Email Format:** Validate addresses manually
3. **Verify Credentials:** Test with external email clients
4. **Monitor Logs:** Review detailed error messages
5. **Test Incrementally:** Start with simple emails, add complexity

---

## **Migration Guide**

### **From Legacy Email Systems**
1. **Assess Current Configuration:** Document existing SMTP settings
2. **Choose Provider:** Select SMTP vs AWS SES based on needs  
3. **Update Credentials:** Migrate to secret node pattern
4. **Test Thoroughly:** Validate all email scenarios
5. **Monitor Deployment:** Watch for delivery issues

### **Provider Migration**
1. **Parallel Testing:** Test new provider alongside existing
2. **Gradual Rollout:** Migrate email types incrementally
3. **Monitoring:** Compare delivery rates and performance
4. **Rollback Plan:** Keep old provider as fallback
5. **Complete Migration:** Remove old provider when stable

---

## **Future Enhancements**

### **Planned Features**
- Additional providers (SendGrid, Mailgun, Postmark)
- Email template system with variable substitution
- Delivery status tracking and webhooks
- Advanced scheduling and queuing
- HTML email builder node

### **Extensibility**
The provider architecture supports easy addition of new email services. Providers implement the `EmailProvider` interface for consistent behavior across all email sending nodes.

---

📧 **The Email module provides enterprise-grade email capabilities for PolySynergy workflows with the flexibility to choose the best provider for your use case.**