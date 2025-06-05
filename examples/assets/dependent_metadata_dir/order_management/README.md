# Order Management Metadata Sample

This sample demonstrates how to create a dependent metadata directory with custom Apex classes for Order Management in Agentforce agents.

## Contents

- `package.xml` - Required metadata package definition
- `classes/` - Directory containing Apex classes
  - `OrderManagementService.cls` - Custom Apex class for order management
  - `OrderManagementService.cls-meta.xml` - Metadata for the Apex class
- `permission_sets/` - Directory containing permission sets
  - `OrderManagementAccess.permissionset-meta.xml` - Permission set for order management

## Features

The `OrderManagementService` class provides an invocable method:

1. **Get Order Info** - Retrieves detailed order information by Order ID and Customer ID
2. Make sure to add the permission set to the agent user before testing the agent

## Usage

### CLI Usage

```bash
# Use this sample with the CLI
python -m agent_sdk.cli create \
    --username your-username \
    --password your-password \
    --agent-file path/to/your-agent.json \
    --dependent-metadata examples/dependent_metadata_samples/order_management \
    --deploy
```

### Programmatic Usage

```python
from agent_sdk import Agentforce
from agent_sdk.core.auth import BasicAuth

# Create agent with this dependent metadata
client = Agentforce(auth=BasicAuth(username="user", password="pass"))
result = client.create(agent, dependent_metadata_dir="examples/dependent_metadata_samples/order_management")
```