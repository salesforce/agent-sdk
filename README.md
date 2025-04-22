# Salesforce Agentforce SDK

[![PyPI version](https://badge.fury.io/py/agentforce-sdk.svg)](https://badge.fury.io/py/agentforce-sdk)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python SDK for creating, managing, and deploying AI agents and prompt templates in Salesforce.

## Terms of the use
Use of this project with Salesforce is subject to the TERMS OF USE

## Introduction

The Salesforce AgentForce SDK provides a programmatic interface to Salesforce's Agent infrastructure, allowing developers to define and interact with agents using Python code. It also includes tools for generating and managing prompt templates with Salesforce field mappings.

## Installation

```bash
pip install agentforce-sdk
```

## Features

- Create and manage AI agents in Salesforce
- Generate and manage prompt templates with Salesforce field mappings
- Support for various Salesforce field types and relationships
- Automatic Apex class generation for related data queries
- Template tuning for different LLM models
- Multiple formats for defining agents (JSON, nested directory, modular directory)
- MCP server for HTTP-based integration

## Documentation

Comprehensive documentation for the SDK is available in the [docs](https://github.com/salesforce/agent-sdk/tree/main/docs) directory:

- [API Documentation](https://github.com/salesforce/agent-sdk/blob/main/docs/api_documentation.md): Detailed documentation for all SDK components, classes, and methods.
- [JSON Schemas](https://github.com/salesforce/agent-sdk/tree/main/docs/schemas): JSON schemas for validating agent definitions in various formats.

## Examples

### Prompt Template Examples

The SDK provides several examples demonstrating prompt template functionality:

- [Basic Template Generation](https://github.com/salesforce/agent-sdk/blob/main/examples/generate_prompt_template_example.py): Generate a prompt template with Salesforce field mappings
- [Template with Apex Actions](https://github.com/salesforce/agent-sdk/blob/main/examples/generate_template_with_apex_example.py): Create a template that includes Apex invocable actions
- [Template Tuning](https://github.com/salesforce/agent-sdk/blob/main/examples/tune_prompt_template_example.py): Tune an existing template for different LLM models
- [Template Deployment](https://github.com/salesforce/agent-sdk/blob/main/examples/deploy_prompt_template_example.py): Deploy a prompt template to Salesforce

#### Basic Template Generation

The `examples/generate_prompt_template_example.py` script demonstrates how to generate a prompt template with Salesforce field mappings:

```bash
python examples/generate_prompt_template_example.py \
  --username your_username \
  --password your_password \
  --security-token your_security_token \
  --output_dir templates \
  --model gpt-4
```

This will:
1. Connect to your Salesforce org
2. Generate a prompt template with appropriate field mappings
3. Save the template and any generated Apex classes to the specified output directory

#### Template with Apex Actions

The `examples/generate_template_with_apex_example.py` script shows how to create a template that includes Apex invocable actions:

```bash
python examples/generate_template_with_apex_example.py \
  --username your_username \
  --password your_password \
  --security-token your_security_token \
  --output_dir templates \
  --model gpt-4
```

This example demonstrates:
1. Creating a template for account opportunity analysis
2. Including Apex invocable actions for data manipulation
3. Generating necessary Apex classes for the actions
4. Saving the complete template with action mappings

#### Template Tuning

The `examples/tune_prompt_template_example.py` script demonstrates how to tune an existing template for different LLM models:

```bash
python examples/tune_prompt_template_example.py \
  --username your_username \
  --password your_password \
  --security-token your_security_token \
  --template-path templates/my_template.json \
  --output_dir tuned_templates \
  --model gpt-4
```

This example shows how to:
1. Load an existing template
2. Optimize it for specific LLM models
3. Add explicit instructions and validation rules
4. Save the enhanced template

### Agent Examples

The [examples](https://github.com/salesforce/agent-sdk/tree/main/examples) directory contains additional sample code for agent functionality:

- [Creating an agent programmatically](https://github.com/salesforce/agent-sdk/blob/main/examples/create_agent_programmatically.py)
- [Creating an agent from a JSON file](https://github.com/salesforce/agent-sdk/blob/main/examples/create_agent_from_json_file.py)
- [Creating an agent from a nested directory](https://github.com/salesforce/agent-sdk/blob/main/examples/create_agent_from_nested_directory.py)
- [Creating an agent from a modular directory](https://github.com/salesforce/agent-sdk/blob/main/examples/create_agent_from_modular_directory.py)
- [Creating an agent from a description](https://github.com/salesforce/agent-sdk/blob/main/examples/create_agent_from_description.py)
- [Creating Apex classes](https://github.com/salesforce/agent-sdk/blob/main/examples/create_apex_class_example.py)
- [Running an agent](https://github.com/salesforce/agent-sdk/blob/main/examples/run_agent.py)
- [Exporting an agent](https://github.com/salesforce/agent-sdk/blob/main/examples/export_salesforce_agent_example.py)
- [Using the MCP server](https://github.com/salesforce/agent-sdk/blob/main/examples/mcp_server_example.py)

## Quick Start

```python
from agent_sdk import Agentforce
from agent_sdk.core.auth import BasicAuth
from agent_sdk.core.prompt_template_utils import PromptTemplateUtils

# Initialize authentication
auth = BasicAuth(username="your_username", password="your_password")

# Initialize the client
client = Agentforce(auth=auth)

# Generate a prompt template
prompt_utils = PromptTemplateUtils(client.sf)
template = prompt_utils.generate_prompt_template(
    name="Account Health Analysis",
    description="Generate a health analysis for an account",
    output_dir="templates",
    model="gpt-4"
)

print(f"Template saved to: {template}")
```

## Project Structure

```
agent-sdk/
├── agent_sdk/
│   ├── core/
│   │   ├── agentforce.py
│   │   ├── auth.py
│   │   ├── base.py
│   │   └── prompt_template_utils.py
│   └── models/
│       ├── agent.py
│       └── prompt_template.py
├── examples/
│   ├── generate_prompt_template_example.py
│   └── [other examples]
└── README.md
```

## Development

To contribute to the project:

1. Clone the repository
2. Install development dependencies: `pip install -r requirements-dev.txt`
3. Run tests: `pytest`

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](https://github.com/salesforce/agent-sdk/blob/main/LICENSE) file for details. 
