# Salesforce AgentForce SDK Documentation

This directory contains comprehensive documentation and JSON schema files for the Salesforce AgentForce SDK.

## Contents

### API Documentation

- **[api_documentation.md](api_documentation.md)**: Comprehensive API documentation for the Salesforce AgentForce SDK, covering all major classes, methods, and usage patterns.

### JSON Schemas

- **[schemas/input_json_schema.json](schemas/input_json_schema.json)**: JSON schema for validating agent definitions in a single JSON file.
- **[schemas/nested_dir_structure_schema.json](schemas/nested_dir_structure_schema.json)**: JSON schema for validating the nested directory structure used for agent definitions.
- **[schemas/modular_dir_structure_schema.json](schemas/modular_dir_structure_schema.json)**: JSON schema for validating the modular directory structure used for agent definitions.

## Using the Documentation

### API Documentation

The API documentation provides a comprehensive guide to using the Salesforce AgentForce SDK. It covers:

- Core components (Agentforce, Models, Utilities)
- Working with agents (Creating, Retrieving, Updating, Deleting, Exporting)
- Directory structures (Single JSON File, Nested, Modular)
- Examples

### JSON Schemas

The JSON schemas can be used to validate your agent definitions against the expected format. You can use them with tools like [jsonschema](https://github.com/python-jsonschema/jsonschema) to validate your agent definitions.

Example:

```python
import json
from jsonschema import validate

# Load the schema
with open('schemas/input_json_schema.json') as f:
    schema = json.load(f)

# Load your agent definition
with open('your_agent.json') as f:
    agent = json.load(f)

# Validate the agent definition
validate(instance=agent, schema=schema)
```

## Directory Structures

The Salesforce AgentForce SDK supports multiple formats for defining agents:

### Single JSON File

A single JSON file containing the complete agent definition.

### Nested Directory Structure

A hierarchical directory structure:

```
agent_dir/
├── agent_name.json           # Agent details without topics
└── topics/
    ├── topic_name.json       # Topic details without actions
    └── topic_name/
        └── actions/
            └── action_name.json  # Action details
```

### Modular Directory Structure

A flat directory structure with references:

```
agent_dir/
├── agents/
│   └── agent_name.json       # Agent details with topic references
├── topics/
│   └── topic_name.json       # Topic details with action references
└── actions/
    └── action_name.json      # Action details with topic reference
```

## Examples

For more examples, please refer to the `examples` directory in the SDK repository. 