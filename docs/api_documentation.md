# Salesforce AgentForce SDK API Documentation

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Core Components](#core-components)
  - [Agentforce](#agentforce)
  - [Models](#models)
  - [Utilities](#utilities)
- [Attribute Mappings](#attribute-mappings)
  - [Overview](#overview)
  - [AttributeMapping Model](#attributemapping-model)
  - [Programmatic Approach](#programmatic-approach)
  - [JSON Configuration Approach](#json-configuration-approach)
  - [Best Practices](#best-practices)
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
    data_type="Text",  # "Text" or "Boolean"
    default_value="",
    var_type="conversation"  # "conversation" or "context"
)

# Access properties
print(variable.name)  # "customer_id"
print(variable.to_dict())  # Convert to dictionary
```

**Supported Data Types:**
- `Text`: For string/text values
- `Boolean`: For true/false values

**Supported Variable Types:**
- `conversation`: Variables that persist throughout the conversation
- `context`: Variables that provide contextual information

#### AttributeMapping

Represents a mapping between action parameters and agent variables.

```python
from agent_sdk.models import AttributeMapping, Variable

# Create a variable
customer_var = Variable(
    name="customer_id",
    data_type="Text",
    visibility="Internal",
    var_type="conversation"
)

# Create an attribute mapping
mapping = AttributeMapping(
    action_parameter="user_id",
    variable=customer_var,
    direction="input"  # or "output"
)

# Access properties
print(mapping.action_parameter)  # "user_id"
print(mapping.direction)  # "input"
print(mapping.to_dict())  # Convert to dictionary
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

## Attribute Mappings

### Overview

Attribute mappings enable you to connect action parameters (inputs and outputs) to agent variables, allowing data to flow between actions and maintain context throughout conversations. This is essential for creating stateful agents that can remember information across multiple interactions.

**Key Benefits:**
- **Context Preservation**: Store and retrieve information across conversation turns
- **Data Flow**: Automatically pass data between different actions
- **Personalization**: Maintain user-specific information throughout the conversation
- **Automation**: Reduce the need for users to repeat information

### AttributeMapping Model

The `AttributeMapping` model defines how action parameters map to agent variables:

```python
from agent_sdk.models import AttributeMapping, Variable

# Required fields
mapping = AttributeMapping(
    action_parameter="parameter_name",  # Name of the input/output parameter
    variable=variable_object,           # Variable object to map to/from
    direction="input"                   # "input" or "output"
)
```

**Fields:**
- `action_parameter`: Name of the action parameter (input or output)
- `variable`: The agent variable to map to/from
- `direction`: Direction of mapping ("input" for action inputs, "output" for action outputs)

### Programmatic Approach

When creating agents programmatically, you can add attribute mappings directly to actions:

```python
from agent_sdk.models import Agent, Topic, Action, Input, Output, Variable, AttributeMapping

# Create agent variables
customer_id_var = Variable(
    name="customer_id",
    description="Customer's unique identifier",
    data_type="Text",
    visibility="Internal",
    var_type="conversation",
    developer_name="customer_id",
    label="Customer ID"
)

order_id_var = Variable(
    name="last_order_id",
    description="ID of the customer's most recent order",
    data_type="Text",
    visibility="Internal",
    var_type="conversation",
    developer_name="last_order_id",
    label="Last Order ID"
)

# Create an action with inputs and outputs
place_order_action = Action(
    name="Place Order",
    description="Place an order for a product",
    inputs=[
        Input(
            name="customer_id",
            description="ID of the customer placing the order",
            data_type="String",
            required=True
        ),
        Input(
            name="product_id",
            description="ID of the product to order",
            data_type="String",
            required=True
        )
    ],
    outputs=[
        Output(
            name="order_id",
            description="Unique identifier for the order",
            data_type="String",
            required=True
        ),
        Output(
            name="status",
            description="Status of the order placement",
            data_type="String",
            required=True
        )
    ]
)

# Add attribute mappings
# Map customer_id input parameter to customer_id variable
place_order_action.attribute_mappings.append(
    AttributeMapping(
        action_parameter="customer_id",
        variable=customer_id_var,
        direction="input"
    )
)

# Map order_id output to last_order_id variable
place_order_action.attribute_mappings.append(
    AttributeMapping(
        action_parameter="order_id",
        variable=order_id_var,
        direction="output"
    )
)

# Alternative: Use convenience methods
place_order_action.map_input("customer_id", customer_id_var)
place_order_action.map_output("order_id", order_id_var)

# Create agent with variables
agent = Agent(
    name="Order Management Agent",
    description="An agent that helps manage orders",
    agent_type="External",
    company_name="Salesforce",
    variables=[customer_id_var, order_id_var]
)
```

### JSON Configuration Approach

When defining agents in JSON, attribute mappings are specified within each action:

```json
{
  "name": "Order Management Agent",
  "description": "An agent that helps manage orders",
  "agent_type": "External",
  "company_name": "Salesforce",
  "variables": [
    {
      "name": "customer_id",
      "data_type": "Text"
    }
  ],
  "topics": [
    {
      "name": "Order Management",
      "description": "Handle order-related queries and actions",
      "scope": "Handle order-related queries and actions",
      "actions": [
        {
          "name": "placeOrder",
          "description": "Place an order for a product",
          "inputs": [
            {
              "name": "customer_id",
              "description": "ID of the customer placing the order",
              "data_type": "string",
              "required": true
            },
            {
              "name": "product_id",
              "description": "ID of the product to order",
              "data_type": "string",
              "required": true
            }
          ],
          "outputs": [
            {
              "name": "order_id",
              "description": "Unique identifier for the order",
              "data_type": "string",
              "required": true
            },
            {
              "name": "status",
              "description": "Status of the order placement",
              "data_type": "string",
              "required": true
            }
          ],
          "attribute_mappings": [
            {
              "action_parameter": "customer_id",
              "variable_name": "customer_id",
              "direction": "input"
            },
            {
              "action_parameter": "order_id",
              "variable_name": "last_order_id",
              "direction": "output"
            }
          ],
          "example_output": {
            "order_id": "ORD-12345",
            "status": "confirmed"
          }
        },
        {
          "name": "checkOrderStatus",
          "description": "Check the status of an existing order",
          "inputs": [
            {
              "name": "order_id",
              "description": "ID of the order to check",
              "data_type": "string",
              "required": true
            }
          ],
          "outputs": [
            {
              "name": "status",
              "description": "Current status of the order",
              "data_type": "string",
              "required": true
            },
            {
              "name": "estimated_delivery",
              "description": "Estimated delivery date",
              "data_type": "string",
              "required": true
            }
          ],
          "attribute_mappings": [
            {
              "action_parameter": "order_id",
              "variable_name": "last_order_id",
              "direction": "input"
            }
          ],
          "example_output": {
            "status": "shipped",
            "estimated_delivery": "2024-03-25"
          }
        }
      ]
    }
  ]
}
```

**📋 For a comprehensive example with multiple topics and complex attribute mappings, see [attribute_mappings_example.json](attribute_mappings_example.json).**

### Best Practices

#### 1. Variable Naming Conventions
- Use descriptive, consistent names for variables
- Follow snake_case convention for variable names
- Use prefixes to group related variables (e.g., `customer_`, `order_`, `payment_`)

```python
# Good examples
customer_id_var = Variable(name="customer_id", ...)
customer_name_var = Variable(name="customer_name", ...)
order_id_var = Variable(name="current_order_id", ...)

# Avoid generic names
var1 = Variable(name="var1", ...)  # Too generic
temp = Variable(name="temp", ...)  # Not descriptive
```

#### 2. Input vs Output Mappings
- **Input mappings**: Use stored variable values as action inputs
- **Output mappings**: Store action results in variables for future use

```python
# Input mapping: Use stored customer ID for order lookup
check_order_action.map_input("customer_id", customer_id_var)

# Output mapping: Store order ID for future reference
place_order_action.map_output("order_id", order_id_var)
```

#### 3. Variable Scope and Lifecycle
- Use `conversation` scope for data that persists throughout the conversation
- Use `context` scope for contextual information that helps the agent understand the situation
- Consider data privacy when choosing visibility settings

```python
# Conversation-scoped variable (persists across turns)
customer_id_var = Variable(
    name="customer_id",
    var_type="conversation",
    visibility="Internal"  # Not visible to end users
)

# Context variable (provides contextual information)
user_preference_var = Variable(
    name="user_preference",
    var_type="context",
    visibility="Internal"
)
```

#### 4. Error Handling
- Always validate that required variables exist before mapping
- Provide meaningful descriptions for variables and mappings
- Test mappings with various data types and edge cases

```python
# Validate variable exists before mapping
if customer_id_var in agent.variables:
    action.map_input("customer_id", customer_id_var)
else:
    raise ValueError("customer_id variable not found in agent")
```

#### 5. Data Types
- Use `Text` for string/text information
- Use `Boolean` for true/false values
- Note: Only Text and Boolean data types are currently supported

```python
# Text variable for string data
customer_name_var = Variable(
    name="customer_name",
    data_type="Text"
)

# Boolean variable for true/false values
is_premium_customer_var = Variable(
    name="is_premium_customer",
    data_type="Boolean",
    description="Whether the customer has premium status"
)
```

#### 6. Documentation and Maintenance
- Document the purpose and usage of each variable
- Maintain a clear mapping between business logic and technical implementation
- Regular review and cleanup of unused variables

```python
# Well-documented variable
customer_preference_var = Variable(
    name="customer_preferences",
    description="Customer's saved preferences for communication and service",
    data_type="Text",
    label="Customer Preferences",
    var_type="conversation",
    visibility="Internal"
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
        data_type="Text"
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
      "data_type": "Text"
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
