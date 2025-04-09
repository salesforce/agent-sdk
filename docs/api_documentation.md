# Salesforce AgentForce SDK API Documentation

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Core Components](#core-components)
  - [Agentforce](#agentforce)
  - [Models](#models)
  - [Utilities](#utilities)
- [Working with Agents](#working-with-agents)
  - [Creating an Agent](#creating-an-agent)
  - [Retrieving an Agent](#retrieving-an-agent)
  - [Updating an Agent](#updating-an-agent)
  - [Deleting an Agent](#deleting-an-agent)
  - [Exporting an Agent](#exporting-an-agent)
- [Directory Structures](#directory-structures)
  - [Single JSON File](#single-json-file)
  - [Nested Directory Structure](#nested-directory-structure)
  - [Modular Directory Structure](#modular-directory-structure)
- [Examples](#examples)

## Introduction

The Salesforce AgentForce SDK is a Python library for creating, managing, and deploying AI agents in Salesforce. This SDK provides a programmatic interface to Salesforce's Agent infrastructure, allowing developers to define and interact with agents using Python code.

## Installation

```bash
pip install agentforce-sdk
```

## Core Components

### Agentforce

The main entry point for interacting with the AgentForce SDK is the `Agentforce` class.

```python
from agent_sdk import Agentforce

# Initialize with username and password
agent_client = Agentforce(username="your_username", password="your_password")

# Or initialize with session ID and instance URL
agent_client = Agentforce(session_id="your_session_id", instance_url="your_instance_url")
```

#### Methods

| Method | Description |
|--------|-------------|
| `create(agent)` | Creates a new agent in Salesforce |
| `retrieve(agent_id)` | Retrieves an existing agent from Salesforce |
| `update(agent)` | Updates an existing agent in Salesforce |
| `delete(agent_id)` | Deletes an agent from Salesforce |
| `export(agent_id, export_path)` | Exports an agent from Salesforce to the specified path |
| `import_agent(agent_path)` | Imports an agent from a local file or directory |
| `retrieve_metadata(metadata_type, agent_name=None)` | Retrieves metadata from Salesforce |
| `run(agent_id, input_text)` | Runs an agent with the provided input text |

### Models

The SDK provides a set of Pydantic models for defining agents and their components.

#### Agent

Represents an AI agent with its topics, system messages, and variables.

```python
from agent_sdk.models import Agent

agent = Agent(
    name="Order Management Agent",
    description="An agent that helps manage orders",
    agent_type="External",  # or "External", "Internal"
    company_name="Salesforce"
)

# Add sample utterances
agent.sample_utterances = [
    "I want to place an order",
    "Check my order status"
]

# Access properties
print(agent.name)  # "Order Management Agent"
print(agent.to_dict())  # Convert to dictionary
print(agent.to_json())  # Convert to JSON string
```

#### Topic

Represents a topic or category of functionality within an agent.

```python
from agent_sdk.models import Topic

topic = Topic(
    name="Order Management",
    description="Handle order-related queries and actions",
    scope="Handle order-related queries and actions"
)

# Add instructions
topic.instructions = [
    "Process order requests efficiently",
    "Validate order details before confirmation"
]

# Access properties
print(topic.name)  # "Order Management"
print(topic.to_dict())  # Convert to dictionary
```

#### Action

Represents an action or function that an agent can perform.

```python
from agent_sdk.models import Action, Input, Output

action = Action(
    name="Place Order",
    description="Place a new order"
)

# Add inputs
action.add_input(
    name="product_id",
    description="ID of the product to order",
    data_type="String",
    required=True
)

# Alternative way to add inputs
action.inputs.append(
    Input(
        name="quantity",
        description="Quantity of the product",
        data_type="Number",
        required=True
    )
)

# Set example output
action.example_output = {
    "status": "success",
    "details": {"order_id": "12345", "message": "Order placed successfully"}
}

# Access properties
print(action.name)  # "Place Order"
print(action.to_dict())  # Convert to dictionary
```

#### SystemMessage

Represents a system message for an agent.

```python
from agent_sdk.models import SystemMessage

system_message = SystemMessage(
    message="You are a helpful order management assistant.",
    msg_type="system"  # or "welcome", "error"
)

# Access properties
print(system_message.message)  # "You are a helpful order management assistant."
print(system_message.to_dict())  # Convert to dictionary
```

#### Variable

Represents a variable used by an agent.

```python
from agent_sdk.models import Variable

variable = Variable(
    name="customer_id",
    data_type="String",
    default_value="",
    var_type="custom"  # or "system"
)

# Access properties
print(variable.name)  # "customer_id"
print(variable.to_dict())  # Convert to dictionary
```

### Utilities

The SDK provides utility classes for working with agents and their components.

#### AgentUtils

Provides utility methods for working with agents.

```python
from agent_sdk.utils.agent_utils import AgentUtils

# Create an agent from a JSON file
agent = AgentUtils.create_agent_from_file("path/to/agent.json")

# Create an agent from a dictionary
agent = AgentUtils.create_agent_from_dict(agent_dict)

# Create an agent from a nested directory structure
agent = AgentUtils.create_agent_from_directory_structure("path/to/agent_dir", "agent_name")

# Create an agent from a modular directory structure
agent = AgentUtils.create_agent_from_modular_files("path/to/agent_dir", "agent_name")

# Export an agent to a directory structure
AgentUtils.create_agent_directory_structure("path/to/export_dir", agent.to_dict())

# Export an agent to a modular directory structure
AgentUtils.export_agent_to_modular_files(agent.to_dict(), "path/to/export_dir")

# Generate agent information using OpenAI
AgentUtils.generate_agent_info(
    description="An agent that helps manage orders",
    company_name="Salesforce",
    agent_name="Order Management Agent",
    output_dir="path/to/output_dir"
)
```

## Working with Agents

### Creating an Agent

```python
from agent_sdk import Agentforce
from agent_sdk.models import Agent, Topic, Action, SystemMessage, Variable, Input, Output

# Initialize the client
client = Agentforce(username="your_username", password="your_password")

# Create the agent
agent = Agent(
    name="Order Management Agent",
    description="An agent that helps manage orders",
    agent_type="External",
    company_name="Salesforce"
)

# Add system messages
agent.system_messages = [
    SystemMessage(
        message="You are a helpful order management assistant.",
        msg_type="system"
    )
]

# Add variables
agent.variables = [
    Variable(
        name="customer_id",
        data_type="String"
    )
]

# Create a topic
topic = Topic(
    name="Order Management",
    description="Handle order-related queries and actions",
    scope="Handle order-related queries and actions"
)

# Set instructions
topic.instructions = [
    "Process order requests efficiently",
    "Validate order details before confirmation"
]

# Create an action
action = Action(
    name="Place Order",
    description="Place a new order",
    inputs=[
        Input(
            name="product_id", 
            description="ID of the product to order", 
            data_type="String", 
            required=True
        ),
        Input(
            name="quantity", 
            description="Quantity of the product", 
            data_type="Number", 
            required=True
        )
    ],
    example_output=Output(
        status="success",
        details={"order_id": "12345", "message": "Order placed successfully"}
    )
)

# Add action to topic
topic.actions = [action]

# Add topic to agent
agent.topics = [topic]

# Create the agent in Salesforce
result = client.create(agent)
print(f"Agent created with ID: {result['id']}")
```

### Retrieving an Agent

```python
from agent_sdk import Agentforce

# Initialize the client
client = Agentforce(username="your_username", password="your_password")

# Retrieve an agent
agent = client.retrieve("agent_id")
print(f"Retrieved agent: {agent.name}")
```

### Updating an Agent

```python
from agent_sdk import Agentforce

# Initialize the client
client = Agentforce(username="your_username", password="your_password")

# Retrieve an agent
agent = client.retrieve("agent_id")

# Update the agent
agent.description = "Updated description"

# Add a new system message
from agent_sdk.models import SystemMessage
agent.system_messages.append(
    SystemMessage(
        message="New system message",
        msg_type="system"
    )
)

# Update the agent in Salesforce
result = client.update(agent)
print(f"Agent updated: {result}")
```

### Deleting an Agent

```python
from agent_sdk import Agentforce

# Initialize the client
client = Agentforce(username="your_username", password="your_password")

# Delete an agent
result = client.delete("agent_id")
print(f"Agent deleted: {result}")
```

### Exporting an Agent

```python
from agent_sdk import Agentforce

# Initialize the client
client = Agentforce(username="your_username", password="your_password")

# Export an agent to a JSON file
client.export("agent_id", "path/to/export.json")

# Export an agent to a directory structure
client.export("agent_id", "path/to/export_dir/", format="directory")

# Export an agent to a modular directory structure
client.export("agent_id", "path/to/export_dir/", format="modular")
```

## Directory Structures

The SDK supports multiple formats for defining agents:

### Single JSON File

A single JSON file containing the complete agent definition:

```json
{
  "name": "Order Management Agent",
  "description": "An agent that helps manage orders",
  "agent_type": "External",
  "company_name": "Salesforce",
  "sample_utterances": [
    "I want to place an order",
    "Check my order status"
  ],
  "system_messages": [
    {
      "message": "You are a helpful order management assistant.",
      "msg_type": "system"
    }
  ],
  "variables": [
    {
      "name": "customer_id",
      "data_type": "String"
    }
  ],
  "topics": [
    {
      "name": "Order Management",
      "description": "Handle order-related queries and actions",
      "scope": "Handle order-related queries and actions",
      "instructions": [
        "Process order requests efficiently",
        "Validate order details before confirmation"
      ],
      "actions": [
        {
          "name": "Place Order",
          "description": "Place a new order",
          "inputs": [
            {
              "name": "product_id",
              "description": "ID of the product to order",
              "data_type": "String",
              "required": true
            },
            {
              "name": "quantity",
              "description": "Quantity of the product",
              "data_type": "Number",
              "required": true
            }
          ],
          "example_output": {
            "status": "success",
            "order_id": "12345",
            "message": "Order placed successfully"
          }
        }
      ]
    }
  ]
}
```

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

Example:

```
order_management_agent/
├── order_management_agent.json       # Agent details
└── topics/
    ├── order_management.json        # Order Management topic details
    └── order_management/
        └── actions/
            ├── place_order.json     # Place Order action details
            └── check_order_status.json  # Check Order Status action details
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

Example:

```
order_management_agent/
├── agents/
│   └── order_management_agent.json  # References topics by name
├── topics/
│   └── order_management.json       # References actions by name
└── actions/
    ├── place_order.json            # Contains topic reference
    └── check_order_status.json     # Contains topic reference
```

## Examples

For more examples, please refer to the `examples` directory in the SDK repository.

- [Creating an agent programmatically](../examples/create_agent_programmatically.py)
- [Creating an agent from a JSON file](../examples/create_agent_from_json_file.py)
- [Creating an agent from a nested directory](../examples/create_agent_from_nested_directory.py)
- [Creating an agent from a modular directory](../examples/create_agent_from_modular_directory.py)
- [Creating an agent from a description](../examples/create_agent_from_description.py)
- [Creating Apex classes](../examples/create_apex_class_example.py)
- [Running an agent](../examples/run_agent.py)
- [Exporting an agent](../examples/export_salesforce_agent_example.py) 