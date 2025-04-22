#!/usr/bin/env python3

"""
Script to create sample Jupyter notebooks for the AgentForce SDK
"""

import json
import os

# Create the notebooks directory if it doesn't exist
notebooks_dir = os.path.join('examples', 'notebooks')
os.makedirs(notebooks_dir, exist_ok=True)

# Content for create_agent_examples.ipynb
create_agent_notebook = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# AgentForce SDK - Create Agent Examples\n",
                "\n",
                "This notebook demonstrates different ways to create agents using the AgentForce SDK."
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Prerequisites\n",
                "\n",
                "First, let's install the AgentForce SDK:"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Install the latest version of AgentForce SDK\n",
                "!pip install ../dist/agentforce_sdk-0.1.4-py3-none-any.whl"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Setup\n",
                "\n",
                "Let's set up our credentials for AgentForce:"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import os\n",
                "from agent_sdk import Agentforce, AgentUtils\n",
                "from agent_sdk.models.agent import Agent\n",
                "from agent_sdk.models.topic import Topic\n",
                "from agent_sdk.models.action import Action\n",
                "from agent_sdk.models.input import Input\n",
                "from agent_sdk.models.output import Output\n",
                "from agent_sdk.models.system_message import SystemMessage\n",
                "from agent_sdk.models.variable import Variable\n",
                "\n",
                "# Replace with your Salesforce credentials\n",
                "username = \"your_username\"\n",
                "password = \"your_password\"\n",
                "\n",
                "# Initialize the AgentForce client\n",
                "agentforce = Agentforce(username=username, password=password)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Method 1: Create Agent from JSON File\n",
                "\n",
                "This is the simplest way to create an agent, by using a pre-defined JSON file."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Path to JSON file\n",
                "json_file_path = \"../assets/input.json\"\n",
                "\n",
                "# Create the agent from JSON file\n",
                "agent = AgentUtils.create_agent_from_file(json_file_path)\n",
                "\n",
                "# View the agent configuration\n",
                "print(f\"Agent Name: {agent.name}\")\n",
                "print(f\"Description: {agent.description}\")\n",
                "print(f\"Company: {agent.company_name}\")\n",
                "print(f\"Topics: {len(agent.topics)}\")\n",
                "\n",
                "# To deploy the agent:\n",
                "# result = agentforce.create(agent)\n",
                "# print(f\"Agent created successfully\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Method 2: Create Agent from Directory Structure\n",
                "\n",
                "This method uses a modular directory structure where each component is defined in a separate file."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Path to directory structure\n",
                "directory_path = \"../assets/chained_agent_dir\"\n",
                "agent_name = \"order_management_agent\"\n",
                "\n",
                "# Create the agent from directory structure\n",
                "agent = AgentUtils.create_agent_from_directory_structure(directory_path, agent_name)\n",
                "\n",
                "# View the agent configuration\n",
                "print(f\"Agent Name: {agent.name}\")\n",
                "print(f\"Description: {agent.description}\")\n",
                "print(f\"Topics: {len(agent.topics)}\")\n",
                "\n",
                "# Display topic information\n",
                "for i, topic in enumerate(agent.topics):\n",
                "    print(f\"\\nTopic {i+1}: {topic.name}\")\n",
                "    print(f\"Description: {topic.description}\")\n",
                "    print(f\"Actions: {len(topic.actions) if topic.actions else 0}\")\n",
                "    \n",
                "    if topic.actions:\n",
                "        for j, action in enumerate(topic.actions):\n",
                "            print(f\"  Action {j+1}: {action.name}\")\n",
                "\n",
                "# To deploy the agent:\n",
                "# result = agentforce.create(agent)\n",
                "# print(f\"Agent created successfully\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Method 3: Create Agent Programmatically\n",
                "\n",
                "This method demonstrates how to create an agent by constructing it programmatically with objects."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Create an action with inputs and outputs\n",
                "action = Action(\n",
                "    name=\"findOrder\",\n",
                "    description=\"Find order details using an order ID\",\n",
                "    inputs=[\n",
                "        Input(\n",
                "            name=\"orderID\",\n",
                "            description=\"Order identification number\",\n",
                "            data_type=\"string\"\n",
                "        )\n",
                "    ],\n",
                "    outputs=[\n",
                "        Output(\n",
                "            name=\"orderDetails\",\n",
                "            description=\"Details of the order\",\n",
                "            data_type=\"object\"\n",
                "        )\n",
                "    ]\n",
                ")\n",
                "\n",
                "# Create a topic with the action\n",
                "topic = Topic(\n",
                "    name=\"Order Management\",\n",
                "    description=\"Handles all user requests related to finding and managing orders\",\n",
                "    scope=\"public\",\n",
                "    instructions=[\n",
                "        \"If a user cannot find their order, attempt to locate it using the order ID\",\n",
                "        \"If a user wants to check the status of their order, retrieve the order details\"\n",
                "    ],\n",
                "    actions=[action]\n",
                ")\n",
                "\n",
                "# Create the agent with the topic\n",
                "agent = Agent(\n",
                "    name=\"ProgrammaticAgent\",\n",
                "    description=\"An agent created programmatically for order management\",\n",
                "    agent_type=\"External\",\n",
                "    agent_template_type=\"EinsteinServiceAgent\",\n",
                "    company_name=\"Example Corp\",\n",
                "    sample_utterances=[\n",
                "        \"What's the status of my order?\",\n",
                "        \"I need to find my order\"\n",
                "    ],\n",
                "    system_messages=[\n",
                "        SystemMessage(message=\"Welcome to Order Management!\", msg_type=\"welcome\"),\n",
                "        SystemMessage(message=\"I'm sorry, I encountered an error.\", msg_type=\"error\")\n",
                "    ],\n",
                "    variables=[\n",
                "        Variable(name=\"apiKey\", data_type=\"string\", default_value=\"sample-key\")\n",
                "    ],\n",
                "    topics=[topic]\n",
                ")\n",
                "\n",
                "# View the agent configuration\n",
                "print(f\"Agent Name: {agent.name}\")\n",
                "print(f\"Description: {agent.description}\")\n",
                "print(f\"Topics: {len(agent.topics)}\")\n",
                "\n",
                "# To deploy the agent:\n",
                "# result = agentforce.create(agent)\n",
                "# print(f\"Agent created successfully\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Method 4: Create & Export Agent Directory Structure\n",
                "\n",
                "This method demonstrates how to create an agent programmatically and then export it to a directory structure."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# We'll use the same agent we created programmatically above\n",
                "export_dir = \"./exported_agent\"\n",
                "\n",
                "# Create the directory structure\n",
                "AgentUtils.create_agent_directory_structure(export_dir, agent)\n",
                "\n",
                "print(f\"Agent exported to directory: {export_dir}\")\n",
                "\n",
                "# You can then read it back\n",
                "# reimported_agent = AgentUtils.create_agent_from_directory_structure(export_dir, \"ProgrammaticAgent\")\n",
                "# print(f\"Re-imported agent name: {reimported_agent.name}\")"
            ]
        }
    ],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {
                "name": "ipython",
                "version": 3
            },
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.9.7"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

# Content for run_agent_examples.ipynb
run_agent_notebook = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# AgentForce SDK - Run Agent Examples\n",
                "\n",
                "This notebook demonstrates how to interact with agents using the AgentForce SDK."
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Prerequisites\n",
                "\n",
                "First, let's install the AgentForce SDK:"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Install the latest version of AgentForce SDK\n",
                "!pip install ../dist/agentforce_sdk-0.1.4-py3-none-any.whl"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Setup\n",
                "\n",
                "Let's set up our credentials for AgentForce:"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import os\n",
                "from agent_sdk import Agentforce\n",
                "\n",
                "# Replace with your Salesforce credentials\n",
                "username = \"your_username\"\n",
                "password = \"your_password\"\n",
                "\n",
                "# Initialize the AgentForce client\n",
                "agentforce = Agentforce(username=username, password=password)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Basic Agent Interaction\n",
                "\n",
                "This example shows how to have a basic conversation with an agent."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Replace with your agent's name\n",
                "agent_name = \"OrderManagementAgent\"\n",
                "\n",
                "# Send an initial message to the agent\n",
                "response = agentforce.send_message(\n",
                "    agent_name=agent_name,\n",
                "    user_message=\"Hi, I'm having trouble with my order number 12345.\"\n",
                ")\n",
                "\n",
                "# Print the agent's response\n",
                "print(\"Agent:\", response['agent_response'])\n",
                "\n",
                "# Store the session ID for the conversation\n",
                "session_id = response['session_id']\n",
                "print(f\"Session ID: {session_id}\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Continuing a Conversation\n",
                "\n",
                "This example demonstrates how to continue a conversation with an agent using the session ID."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Send a follow-up message using the same session ID\n",
                "response = agentforce.send_message(\n",
                "    agent_name=agent_name,\n",
                "    user_message=\"What's the status of my order?\",\n",
                "    session_id=session_id\n",
                ")\n",
                "\n",
                "# Print the agent's response\n",
                "print(\"Agent:\", response['agent_response'])"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Interactive Chat Interface\n",
                "\n",
                "This example creates a simple interactive chat interface for communicating with the agent."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "def chat_with_agent(agent_name):\n",
                "    print(f\"Starting chat with {agent_name}. Type 'exit' to end the conversation.\")\n",
                "    session_id = None\n",
                "    \n",
                "    while True:\n",
                "        # Get user input\n",
                "        user_message = input(\"You: \")\n",
                "        \n",
                "        # Check if user wants to exit\n",
                "        if user_message.lower() == 'exit':\n",
                "            print(\"Chat ended.\")\n",
                "            break\n",
                "            \n",
                "        # Send message to agent\n",
                "        try:\n",
                "            response = agentforce.send_message(\n",
                "                agent_name=agent_name,\n",
                "                user_message=user_message,\n",
                "                session_id=session_id\n",
                "            )\n",
                "            \n",
                "            # Update session ID if this is the first message\n",
                "            if session_id is None:\n",
                "                session_id = response['session_id']\n",
                "                \n",
                "            # Print agent's response\n",
                "            print(f\"Agent: {response['agent_response']}\")\n",
                "            \n",
                "        except Exception as e:\n",
                "            print(f\"Error: {str(e)}\")\n",
                "            \n",
                "# You can uncomment this line to run the interactive chat\n",
                "# chat_with_agent(agent_name)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Handling Agent Sessions\n",
                "\n",
                "This example demonstrates how to manage multiple agent sessions."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Start multiple sessions with different contexts\n",
                "def start_session(agent_name, initial_message):\n",
                "    response = agentforce.send_message(\n",
                "        agent_name=agent_name,\n",
                "        user_message=initial_message\n",
                "    )\n",
                "    return {\n",
                "        'session_id': response['session_id'],\n",
                "        'last_response': response['agent_response'],\n",
                "        'context': initial_message\n",
                "    }\n",
                "\n",
                "# Create two different sessions\n",
                "session1 = start_session(agent_name, \"I need to check on my reservation for tomorrow.\")\n",
                "session2 = start_session(agent_name, \"I'm having trouble with payment for my order.\")\n",
                "\n",
                "print(f\"Session 1 ID: {session1['session_id']}\")\n",
                "print(f\"Session 1 Context: {session1['context']}\")\n",
                "print(f\"Session 1 Response: {session1['last_response']}\\n\")\n",
                "\n",
                "print(f\"Session 2 ID: {session2['session_id']}\")\n",
                "print(f\"Session 2 Context: {session2['context']}\")\n",
                "print(f\"Session 2 Response: {session2['last_response']}\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Advanced: Asyncronous Agent Interaction\n",
                "\n",
                "This example shows how to interact with agents asynchronously using Python's asyncio library."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import asyncio\n",
                "import aiohttp\n",
                "\n",
                "async def send_message_async(agent_name, message, session_id=None):\n",
                "    # This is a simplified example - you would need to implement the actual async API call\n",
                "    # based on the AgentForce SDK's capabilities\n",
                "    await asyncio.sleep(1)  # Simulate network delay\n",
                "    response = agentforce.send_message(\n",
                "        agent_name=agent_name,\n",
                "        user_message=message,\n",
                "        session_id=session_id\n",
                "    )\n",
                "    return response\n",
                "\n",
                "async def process_multiple_queries():\n",
                "    # Define some queries\n",
                "    queries = [\n",
                "        \"What's the status of order 12345?\",\n",
                "        \"Can I update my shipping address?\",\n",
                "        \"I need help with a refund\"\n",
                "    ]\n",
                "    \n",
                "    # Send all queries concurrently\n",
                "    tasks = [send_message_async(agent_name, query) for query in queries]\n",
                "    responses = await asyncio.gather(*tasks)\n",
                "    \n",
                "    # Process the results\n",
                "    for i, response in enumerate(responses):\n",
                "        print(f\"Query: {queries[i]}\")\n",
                "        print(f\"Response: {response['agent_response']}\")\n",
                "        print(\"---\")\n",
                "\n",
                "# Uncomment to run the async example\n",
                "# asyncio.run(process_multiple_queries())"
            ]
        }
    ],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {
                "name": "ipython",
                "version": 3
            },
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.9.7"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

# Write the notebooks to files
with open(os.path.join(notebooks_dir, 'create_agent_examples.ipynb'), 'w') as f:
    json.dump(create_agent_notebook, f, indent=1)

with open(os.path.join(notebooks_dir, 'run_agent_examples.ipynb'), 'w') as f:
    json.dump(run_agent_notebook, f, indent=1)

print("Jupyter notebooks created successfully!") 