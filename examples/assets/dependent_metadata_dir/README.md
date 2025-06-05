# Dependent Metadata Samples

This directory contains sample dependent metadata directories that demonstrate how to use the `--dependent-metadata` feature with the Agentforce SDK.

## What is Dependent Metadata?

Dependent metadata allows you to provide your own custom Salesforce metadata (Apex classes, flows, objects, etc.) instead of using the default template classes that come with the SDK.

## Requirements

A dependent metadata directory must contain:
- `package.xml` - Required metadata package definition

## Available Samples

### order_management/
An example with a custom Apex class that provides order management functionality for agents.

**Contains:**
- Custom Apex class with `@InvocableMethod` annotations for order management
- Proper error handling and response structures
- Example agent configuration

## Quick Start

1. **CLI Usage:**
```bash
python -m agent_sdk.cli create \
    --username your-username \
    --password your-password \
    --agent-file path/to/agent.json \
    --dependent-metadata examples/assets/dependent_metadata_dir/order_management \
    --deploy
```

2. **Programmatic Usage:**
```python
from agent_sdk import AgentUtils

agent = AgentUtils.create_agent_from_dict(
    agent_data,
    dependent_metadata_dir="examples/assets/dependent_metadata_dir/order_management"
)
```

## Validation

The SDK will automatically validate your dependent metadata:
- ✅ Checks that `package.xml` exists
- ✅ Shows summary of metadata contents
- ✅ Allows any Salesforce metadata type

## Creating Your Own

1. Create a new directory for your metadata
2. Add `package.xml` with your metadata types
3. Add your custom metadata files (classes, flows, etc.)
4. Use the `--dependent-metadata` parameter

For detailed examples, see the individual sample directories. 