# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

This is a Poetry-managed Python project. Common development commands:

```bash
# Install dependencies
poetry install

# Run tests (look for pytest or similar in individual node directories)
poetry run pytest polysynergy_nodes/[node_name]/tests/

# Install in development mode
poetry install --with dev
```

## Architecture Overview

This is `polysynergy_nodes` - a Python library containing modular nodes for the PolySynergy orchestration system. The architecture follows a plugin-based pattern where each functional area is organized as a separate module containing related nodes.

### Core Structure

- **Node Registration**: All nodes are registered in `polysynergy_nodes/__init__.py` via a `registered_nodes` list
- **Node Framework**: Nodes inherit from `polysynergy_node_runner.setup_context.node.Node` and use the `@node` decorator
- **Node Pattern**: Each node typically has:
  - Input/output variable settings with `NodeVariableSettings`
  - Path settings for flow control with `PathSettings`
  - An `execute()` method containing the main logic
  - Associated README files and tests

### Key Node Categories

- **Agent Nodes** (`agent/`): AI agent orchestration with support for OpenAI, Mistral, and various vector stores (Qdrant). Includes memory management, embeddings, and tool integration.
- **Variable Nodes** (`variable/`): Data handling nodes for strings, JSON, lists, etc. with placeholder replacement capabilities
- **Utility Nodes**: Math operations, list processing, JSON manipulation, file handling, HTTP requests
- **Integration Nodes**: AWS services (DynamoDB, S3, Textract), email, JWT, OAuth
- **Control Flow**: Jump/loop nodes, conditionals, scheduling

### Agent System Architecture

The agent system (`polysynergy_nodes/agent/`) implements a sophisticated AI orchestration layer:

- **Service Layer**: Abstracted clients for different AI providers (OpenAI, Mistral)
- **Memory Management**: Chat memory with DynamoDB backend support
- **Vector Storage**: Context management with Qdrant integration
- **Tool Integration**: Dynamic tool discovery and execution
- **Embeddings**: Multi-provider embedding support for context retrieval

### Node Development Patterns

- Nodes use `NodeVariableSettings` for configurable inputs/outputs with dock properties
- Path settings enable conditional flow control (true_path/false_path patterns)
- Error handling follows NodeError conventions
- Icons are stored in `icons/` subdirectories for UI representation
- Each functional area includes comprehensive test suites

### Dependencies

Key external dependencies managed via Poetry:
- `polysynergy_node_runner`: Core node execution framework (local path dependency)
- `openai`, `mistralai`: AI provider clients
- `boto3`: AWS services integration
- `qdrant-client`: Vector database
- `pydantic`: Data validation and serialization