# AgentForce SDK Examples

This directory contains example scripts demonstrating various features of the AgentForce SDK.

## Running Examples

There are two ways to run the examples:

### 1. Using the Helper Script

The `run_example.py` script provides a convenient way to run any example:

```bash
# List all available examples
python examples/run_example.py --list

# Run a specific example
python examples/run_example.py example_name [arguments]
```

For example:
```bash
# Run the prompt template generation example
python examples/run_example.py generate_prompt_template_example --username your_username --password your_password
```

### 2. Running Examples Directly

You can also run any example script directly:

```bash
# Run any example directly from the root directory
python examples/example_name.py [arguments]
```

For example:
```bash
python examples/generate_prompt_template_example.py --username your_username --password your_password
```

## Available Examples

1. **generate_prompt_template_example.py**
   - Demonstrates how to generate prompt templates for Salesforce agents
   - Shows different use cases with various Salesforce objects

2. **create_agent_programmatically.py**
   - Shows how to create an agent programmatically
   - Includes examples of creating topics, actions, and system messages

3. **create_agent_from_description.py**
   - Demonstrates creating an agent from a natural language description
   - Uses LLM to generate agent structure

4. **create_agent_from_json_file.py**
   - Shows how to create an agent from a JSON configuration file
   - Useful for version control and sharing agent configurations

5. **create_agent_from_modular_directory.py**
   - Demonstrates creating an agent from a modular directory structure
   - Good for organizing complex agents with multiple topics and actions

6. **create_agent_from_nested_directory.py**
   - Shows how to create an agent from a nested directory structure
   - Useful for complex agents with hierarchical organization

7. **create_apex_class_example.py**
   - Demonstrates generating Apex classes for agent actions
   - Shows how to create invocable actions for Salesforce

8. **deploy_agent_token_flow.py**
   - Shows how to deploy an agent using different authentication flows
   - Includes examples of client credentials and JWT bearer flows

9. **export_salesforce_agent_example.py**
   - Demonstrates how to export an existing Salesforce agent
   - Shows how to convert to modular format

10. **run_agent.py**
    - Shows how to run an agent and have a conversation
    - Demonstrates session management

11. **api_server_example.py**
    - Demonstrates running an API server for agent interactions
    - Shows how to handle agent requests via HTTP

## Directory Structure

- `assets/` - Contains sample files and configurations used by examples
- `exported_agents/` - Default directory for exported agent files
- `mcp_servers/` - MCP server configurations
- `notebooks/` - Jupyter notebook examples

## Notes

- All examples can be run directly without installing the package
- Examples automatically add the parent directory to Python path
- Most examples require Salesforce credentials
- Some examples may require additional setup (see individual example documentation)

## Pre Requisite

Create an org using the following
https://sfdc.co/OrgFarmSignup
Use code Agents$$

```bash
./setup_venv.sh
pip install jupyter
pip install agentforce-sdk
```

## Examples

### 1. Creating an Agent from JSON File (`create_agent_from_json_file.py`)

This example demonstrates how to create an agent from a single JSON file using the `AgentUtils.create_agent_from_json_file` method. This is useful for simple agents or when you have a complete agent configuration ready to use.

```bash
python examples/create_agent_from_json_file.py --username your_username --password your_password --json_file examples/assets/input.json
```

### 2. Creating an Agent from Directory (`create_agent_from_modular_directory.py`)

This example shows how to create an agent from a directory structure using the `AgentUtils.create_agent_from_modular_files` method. This approach is useful when your agent configuration is split across multiple files.

```bash
python examples/create_agent_from_modular_directory.py --username your_username --password your_password --agent_directory examples/assets/modular_agent_dir --agent_name order_management_agent
```

### 3. Building an Agent Programmatically (`create_agent_programmatically.py`)

This example shows how to create an agent, topics, and actions using the SDK's programmatic API. This approach gives you more control over the agent creation process and allows you to build agents dynamically.

```bash
python examples/create_agent_programmatically.py --username your_username --password your_password --company_name "Your Company"
```

### 4. Running Existing Agent (`run_agent.py`)

This example demonstrates how to interact with an existing agent using the SDK.

```bash
python examples/run_agent.py --username your_username --password your_password 
```

### 5. Create and Deploy Agent (`run_create_agent.py`)

This is a comprehensive example that creates an agent with multiple topics and actions, then deploys it to Salesforce.

```bash
python examples/run_create_agent.py --username your_username --password your_password --company_name "Your Company"
```

### 6. Jupyter Notebooks (`notebooks/`)

The `notebooks/` directory contains interactive Jupyter notebooks that demonstrate how to use the AgentForce SDK:

- **create_agent_examples.ipynb**: Shows different ways to create agents (JSON, directory structure, programmatically)
- **run_agent_examples.ipynb**: Demonstrates how to interact with agents, manage conversations, and handle sessions
- **advanced_integrations.ipynb**: Shows how to integrate AgentForce with popular AI frameworks like LangChain, LangGraph, and LlamaIndex

To run the notebooks:

```bash
cd examples
jupyter notebook notebooks/
```

See the [notebooks/README.md](notebooks/README.md) for more details.

## Directory Structure

The `modular_agent/` directory contains an example of how to structure your agent files for the modular approach:

```
modular_agent/
├── agents/
│   └── order_management_agent.json
├── topics/
│   ├── reservation_management.json
│   ├── payment_assistance.json
│   └── general_faqs.json
└── actions/
    ├── findReservation.json
    ├── updateReservation.json
    ├── processPayment.json
    └── ...
```

In this structure:

- **agents/**: Contains agent configuration files that reference topics
- **topics/**: Contains topic configuration files that reference actions
- **actions/**: Contains action configuration files with their inputs and outputs

## Using the Modular Approach in Your Projects

The modular approach is ideal for complex agents with many topics and actions. To use it in your projects:

1. Create a directory structure like the one above
2. Define your agent(s) in JSON files in the `agents/` directory, including references to topics
3. Define your topics in JSON files in the `topics/` directory, including references to actions
4. Define your actions in JSON files in the `actions/` directory

Then, load your agent using:

```python
from agent_sdk import Agentforce
from agent_sdk.utils.agent_utils import AgentUtils

# Create agent from modular files
agent = AgentUtils.create_agent_from_modular_files("path/to/modular_agent", "agent_name")

# Initialize Agentforce client and deploy the agent
client = Agentforce(username="your_username", password="your_password")
result = client.create(agent)
```

You can also export an existing agent to this modular structure:

```python
AgentUtils.export_agent_to_modular_files(agent.to_dict(), "path/to/export_directory")
``` 