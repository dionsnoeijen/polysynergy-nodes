# Environment Variable

A placeholder node for environment variable key configuration in PolySynergy workflows.  
This node acts as a configuration marker and does not perform any runtime operations.

## **Category:** Environment

## **Description**
The **Environment Variable** node serves as a configuration placeholder within PolySynergy workflows. It is designed to represent environment variable keys in the visual workflow editor but does not execute any functional logic at runtime.

This node is typically used for:
- **Configuration Documentation:** Visual representation of environment variables used in workflows
- **Workflow Planning:** Marking where environment variables are needed in the flow
- **Template Definition:** Defining environment variable placeholders in workflow templates

### **Important Note**
This node contains **no functional implementation** - the `execute()` method is intentionally empty (`pass`). It serves purely as a configuration marker in the PolySynergy system.

---

## **Variables**

### **Output Variables**

| Name        | Type      | Description |
|-------------|-----------|-------------|
| `true_path` | bool/str  | Environment variable key identifier |

### **Configuration**
- **Label:** "Key" 
- **Info:** "The environment variable key"
- **Purpose:** Identifies which environment variable this node represents

---

## **Flow Control**

| Path        | Condition | Description |
|-------------|-----------|-------------|
| `true_path` | Always    | Contains the environment variable key identifier |

**Note:** Since the node has no execution logic, the flow control is handled by the PolySynergy runtime system based on the node's configuration.

---

## **How It Works**

1. **Configuration Phase:** Node is configured with environment variable key information
2. **Runtime Phase:** Node's `execute()` method does nothing (`pass`)  
3. **Flow Control:** PolySynergy system uses the node's configuration for workflow logic
4. **Output:** The `true_path` contains the configured environment variable key

The actual environment variable management and retrieval is handled by:
- PolySynergy runtime system
- Environment Variable Manager service (if available)
- External configuration systems

---

## **Usage Patterns**

### **Workflow Documentation**
```yaml
# Visual representation of environment variables used
Environment Variable:
  key: "API_KEY"
  # Indicates this workflow requires API_KEY environment variable
```

### **Template Placeholders**
```yaml
# Workflow template with environment variable placeholders
Environment Variable:
  key: "DATABASE_URL"
  # Template indicates database connection is required
```

### **Configuration Markers**
```yaml
# Marking environment dependencies in complex workflows
Environment Variable:
  key: "SMTP_HOST"
  # Indicates email functionality requires SMTP configuration
```

---

## **Integration with Environment Management**

While the node itself is non-functional, it works with the broader PolySynergy environment system:

### **Environment Variable Manager**
The system includes an `EnvVarManager` service (located in the `polysynergy_node_runner` package) that provides:
- **Storage:** DynamoDB-based environment variable storage
- **Multi-Stage Support:** Development, staging, production environments
- **AWS Integration:** Seamless integration with AWS Lambda and DynamoDB
- **Project Isolation:** Environment variables scoped by project

### **Manager Features**
- `list_vars(project_id)` - List all variables for a project
- `get_var(project_id, stage, key)` - Retrieve specific variable
- `set_var(project_id, stage, key, value)` - Set variable value
- `delete_var(project_id, stage, key)` - Remove variable

---

## **Example Usage**

### **Basic Configuration**
```yaml
# Node represents an API key requirement
Environment Variable:
  true_path: "API_KEY"
  # Workflow indicates it needs API_KEY from environment
```

### **Multi-Variable Workflow**
```yaml
# Multiple environment variables in a workflow
Environment Variable (Database):
  true_path: "DATABASE_URL"

Environment Variable (API):
  true_path: "API_KEY"

Environment Variable (Cache):
  true_path: "REDIS_URL"
```

### **Service Integration**
```yaml
# Environment variables for different services
Environment Variable (SMTP):
  true_path: "SMTP_HOST"
  
Environment Variable (AWS):
  true_path: "AWS_ACCESS_KEY_ID"
  
Environment Variable (Storage):
  true_path: "S3_BUCKET_NAME"
```

---

## **Architecture Context**

### **Node Hierarchy**
```
PolySynergy Workflow
├── Functional Nodes (execute business logic)
├── Environment Variable Nodes (configuration markers)
└── Flow Control Nodes (routing logic)
```

### **Environment System Architecture**
```
Workflow Definition
├── Environment Variable Nodes (placeholders)
├── PolySynergy Runtime (variable resolution)
├── EnvVarManager (storage/retrieval)  
└── DynamoDB (persistent storage)
```

### **Stage-Based Configuration**
```yaml
Development Stage:
  - API_KEY: "dev-api-key-123"
  - DATABASE_URL: "dev-db.example.com"

Production Stage:
  - API_KEY: "prod-api-key-456" 
  - DATABASE_URL: "prod-db.example.com"
```

---

## **Best Practices**

### **Node Usage**
- **Descriptive Keys:** Use clear, descriptive environment variable names
- **Consistent Naming:** Follow consistent naming conventions (UPPER_SNAKE_CASE)
- **Documentation:** Document the purpose of each environment variable
- **Grouping:** Group related environment variables logically in workflows

### **Environment Management**
- **Stage Separation:** Use different values for dev/staging/production
- **Security:** Keep sensitive values encrypted and access-controlled
- **Validation:** Validate environment variables before workflow execution  
- **Defaults:** Provide sensible defaults where appropriate

### **Workflow Design**
- **Early Validation:** Check environment variables early in workflow
- **Error Handling:** Handle missing environment variables gracefully
- **Documentation:** Document environment requirements in workflow descriptions
- **Testing:** Test workflows with different environment configurations

---

## **Troubleshooting**

### **Common Issues**

#### **Node Not Functioning**
- **Expected Behavior:** This node is designed to be non-functional
- **Purpose:** Configuration marker only, not executable logic
- **Resolution:** Use the node for documentation and configuration purposes

#### **Missing Environment Variables**  
- **Symptom:** Workflow fails due to missing environment variables
- **Cause:** Environment variables not set in target environment
- **Resolution:** Configure required variables using EnvVarManager or system environment

#### **Configuration Errors**
- **Symptom:** Node not properly configured in workflow
- **Cause:** Missing or incorrect key configuration
- **Resolution:** Ensure `true_path` contains correct environment variable key

---

## **Testing**

The node includes comprehensive tests covering:

### **Basic Functionality**
- Node initialization and structure
- Execute method behavior (no-op)
- Property consistency after execution
- Multiple execution calls

### **Configuration Testing**  
- PathSettings integration
- Attribute persistence  
- Node decorator functionality

### **Integration Testing**
- Node decorator functionality
- PathSettings configuration
- Multiple execution scenarios

---

## **Migration Notes**

### **Environment Variable Manager Migration**
The Environment Variable Manager (`EnvVarManager`) has been moved to the `polysynergy_node_runner` package for better integration with the core system. This provides centralized environment variable management across all node types.

### **Compatibility**
- Node structure is stable and backward compatible
- Configuration format will remain consistent
- Integration with broader PolySynergy system is maintained

---

## **Use Cases**

### **✅ Appropriate Uses**
- **Workflow Documentation:** Visual indication of environment dependencies
- **Template Creation:** Placeholder for environment variables in templates
- **Configuration Planning:** Planning which environment variables are needed
- **System Integration:** Marking external system configuration requirements

### **❌ Inappropriate Uses**
- **Runtime Logic:** Expecting the node to execute functional code
- **Variable Storage:** Using the node to store actual environment values
- **Data Processing:** Processing environment variable values
- **Flow Control:** Conditional logic based on environment values

---

## **Related Components**

### **Environment Variable Manager**
- **Location:** `polysynergy_node_runner` package
- **Purpose:** Centralized environment variable management and storage
- **Features:** DynamoDB storage, multi-stage support, AWS integration

### **Node Runner Integration**
- **Current Location:** `polysynergy_node_runner` package
- **Status:** Integrated with core node runner system
- **Access:** Available to all node types through the runner framework

---

🌍 **Use this node as a configuration marker to document environment variable dependencies in your PolySynergy workflows.**