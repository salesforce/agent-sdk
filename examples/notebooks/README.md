# AgentForce SDK Jupyter Notebooks

This directory contains Jupyter notebooks that demonstrate how to use the AgentForce SDK.

## Prerequisites

- Python 3.8+
- Jupyter Notebook or JupyterLab
- Salesforce credentials

## Installation

Before running these notebooks, ensure you have the required dependencies:

```bash
pip install jupyter
pip install agentforce-sdk
```

## Available Notebooks

1. **create_agent_examples.ipynb**: Demonstrates various methods to create agents:
   - Create agent from JSON file
   - Create agent from directory structure
   - Create agent programmatically
   - Create and export an agent to directory structure

2. **run_agent_examples.ipynb**: Shows how to interact with agents:
   - Basic agent interaction
   - Continuing conversations with session IDs
   - Interactive chat interface
   - Managing multiple agent sessions
   - Asynchronous agent interaction

3. **advanced_integrations.ipynb**: Demonstrates integration with popular AI frameworks:
   - Using AgentForce with LangChain as a tool
   - Building customer support workflows with LangGraph
   - Enhancing agents with RAG capabilities using LlamaIndex
   - Creating hybrid systems that combine multiple frameworks
   - Designing integrated AgentForce agents with advanced capabilities

## Usage

1. Start Jupyter:
   ```bash
   jupyter notebook
   ```

2. Open one of the notebooks from the Jupyter interface.

3. Replace the placeholder Salesforce credentials with your own.

4. Run the cells in order to see the examples in action.

## Note

These notebooks include example code with the actual API calls commented out to prevent unintended API usage. Remove the comments to execute the API calls.

For the advanced integrations notebook, you'll also need to provide API keys for OpenAI and other services as indicated in the notebook.
