<p align="center">
  <img src="https://www.polysynergy.com/ps-color-logo-with-text.svg" alt="PolySynergy Logo" width="400"/>
</p>

# PolySynergy Nodes

<p align="center">
  <strong>⚠️ This repository is currently under construction ⚠️</strong>
</p>

<p align="center">
  <em>Modular nodes for the PolySynergy orchestration system</em>
</p>

---

## Overview

**polysynergy_nodes** is a comprehensive Python library containing modular, reusable nodes for the PolySynergy orchestration system. Each node represents a specific functionality that can be connected and orchestrated to build complex workflows and automation pipelines.

## 🏗️ Current Status

This project is actively under development. Features, APIs, and documentation may change frequently. Use at your own discretion in production environments.

## Architecture

The library follows a plugin-based architecture where functionality is organized into distinct modules:

### 🧠 Agent System
- **AI Orchestration**: Support for OpenAI, Mistral AI providers
- **Memory Management**: Persistent chat memory with DynamoDB backend
- **Vector Storage**: Context management with Qdrant integration
- **Tool Integration**: Dynamic tool discovery and execution
- **Embeddings**: Multi-provider embedding support

### 📊 Data Processing
- **Variables**: String, JSON, list, and rich text handling with placeholder replacement
- **Transformations**: Base64 encoding/decoding, casting, comparisons
- **JSON Operations**: Querying, combining, switching based on JSON data
- **List Operations**: Filtering, sorting, merging, uniqueness, and advanced manipulations

### 🔄 Control Flow
- **Conditionals**: If-then-else logic, switch-case statements
- **Loops**: List iteration, break/continue controls
- **Jumps**: Flow control and routing

### 🧮 Utilities
- **Mathematics**: Comprehensive math operations (add, subtract, multiply, divide, etc.)
- **String Operations**: Case conversion, trimming, splitting, joining, pattern matching
- **Date/Time**: Current time, fixed time windows, scheduling
- **Random**: Data generation, path selection, one-of choices

### 🌐 Integrations
- **HTTP**: Request/response handling
- **Email**: SMTP email sending with attachments
- **AWS Services**: DynamoDB, S3, Textract OCR
- **Authentication**: JWT generation, OAuth token management
- **File Operations**: Upload, type detection, PDF generation

### 🔧 Development & Debugging
- **Logging**: Info and error logging nodes
- **Validation**: JSON schema validation
- **Mocking**: Route and schedule mocking for testing
- **Environment**: Environment variable access

## Installation

This project uses Poetry for dependency management:

```bash
# Install dependencies
poetry install

# Install with development dependencies
poetry install --with dev
```

## Node Directory Structure

**Critical Requirements:**

Each node must follow a strict directory structure for automatic loading by the API:

- **One Node Per Directory**: Each directory containing a node `.py` file can **only** contain a single node class
- **No Mixed Content**: Directories with node files cannot contain other node implementations
- **Automatic Registration**: Nodes are automatically discovered and loaded by the API - no manual registration required

### Directory Organization

```
polysynergy_nodes/
├── category_name/
│   ├── __init__.py
│   ├── node_name.py              # Contains single @node decorated class
│   ├── NodeClassName_README.md   # Documentation matching node class name
│   ├── icons/                    # Optional: SVG icons for UI
│   ├── tests/                    # Optional: Test files
│   └── services/                 # Optional: Supporting services/utilities
```

### Node Implementation Rules

1. **Single Responsibility**: One node class per `.py` file
2. **Decorator Required**: Must use `@node` decorator
3. **Inheritance**: Must inherit from `polysynergy_node_runner.setup_context.node.Node`
4. **Registration**: Added to `registered_nodes` list in `polysynergy_nodes/__init__.py`
5. **Documentation**: README files must follow `[NodeClassName]_README.md` naming convention for automatic matching

## Development

### Running Tests

Tests are organized by node category:

```bash
# Run tests for a specific node category
poetry run pytest polysynergy_nodes/math/tests/
poetry run pytest polysynergy_nodes/agent/tests/

# Run all tests
poetry run pytest
```

### Node Structure

Each node follows a consistent pattern:

- **Input/Output Configuration**: Using `NodeVariableSettings` with dock properties
- **Path Settings**: For conditional flow control (`true_path`/`false_path`)
- **Execute Method**: Main logic implementation
- **Error Handling**: Using `NodeError` conventions
- **Icons**: SVG icons in `icons/` subdirectories
- **Tests**: Comprehensive test suites in `tests/` subdirectories
- **Documentation**: README files for complex nodes

### Key Dependencies

- **polysynergy_node_runner**: Core node execution framework
- **pydantic**: Data validation and serialization
- **openai**, **mistralai**: AI provider clients
- **boto3**: AWS services integration
- **qdrant-client**: Vector database operations

## Node Categories

| Category | Description | Key Nodes |
|----------|-------------|-----------|
| **agent** | AI orchestration and tool integration | `agent`, `mistral_agent`, `openai_agent` |
| **variable** | Data handling and manipulation | `variable_string`, `variable_json`, `variable_list` |
| **math** | Mathematical operations | `math_add`, `math_multiply`, `math_divide` |
| **string** | String processing | `string_replace`, `string_split`, `string_case` |
| **list** | List operations | `filter_list`, `sort_list`, `merge_list` |
| **json** | JSON data manipulation | `json_query`, `json_combine`, `json_switch` |
| **http** | HTTP operations | `http_request`, `http_response` |
| **conditional** | Flow control | `if_then_else`, `switch_case` |
| **comparison** | Value comparisons | `comparison_equal`, `comparison_larger_than` |
| **file** | File operations | `upload_from_data`, `file_type` |
| **dynamodb** | AWS DynamoDB integration | `get`, `set` |

## Contributing

Since this project is under active construction, contribution guidelines are being developed. Please check back for updates.

## License

See [LICENSE](LICENSE) file for details.

## Support

For questions and support regarding PolySynergy, visit [polysynergy.com](https://www.polysynergy.com).

---

<p align="center">
  <strong>Built with PolySynergy - Orchestrating Intelligence</strong>
</p>