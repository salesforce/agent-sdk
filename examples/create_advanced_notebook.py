#!/usr/bin/env python3

"""
Script to create the advanced_integrations.ipynb notebook for the AgentForce SDK
"""

import json
import os

# Create the notebooks directory if it doesn't exist
notebooks_dir = os.path.join('examples', 'notebooks')
os.makedirs(notebooks_dir, exist_ok=True)

# Content for advanced_integrations.ipynb
advanced_notebook = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# AgentForce SDK - Advanced Integrations\n",
                "\n",
                "This notebook demonstrates how to integrate the AgentForce SDK with popular AI frameworks:\n",
                "\n",
                "* **LangChain**: For creating flexible language model chains and tools\n",
                "* **LangGraph**: For building complex agent workflows with state management\n",
                "* **LlamaIndex**: For data ingestion and RAG applications"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Prerequisites\n",
                "\n",
                "First, let's install the necessary packages:"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Install the AgentForce SDK and required packages\n",
                "!pip install ../dist/agentforce_sdk-0.1.4-py3-none-any.whl\n",
                "!pip install \"langchain>=0.1.12\" \"langchain-core>=0.1.31\" langgraph==0.0.32 llama-index==0.10.5 openai"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Setup\n",
                "\n",
                "Let's import the necessary modules and set up our clients:"
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
                "from agent_sdk.models import Agent, Topic, Action, Input, Output\n",
                "\n",
                "# LangChain imports\n",
                "from langchain_core.prompts import ChatPromptTemplate\n",
                "from langchain_core.output_parsers import StrOutputParser\n",
                "from langchain_openai import ChatOpenAI\n",
                "\n",
                "# LangGraph imports\n",
                "from langgraph.graph import END, StateGraph\n",
                "import langgraph.prebuilt as prebuilt\n",
                "\n",
                "# LlamaIndex imports\n",
                "from llama_index.core import SimpleDirectoryReader, VectorStoreIndex\n",
                "from llama_index.core.response_synthesizers import get_response_synthesizer\n",
                "\n",
                "# Set API keys (replace with your own)\n",
                "os.environ[\"OPENAI_API_KEY\"] = \"your-openai-api-key\"\n",
                "\n",
                "# Initialize AgentForce\n",
                "sf_username = \"your_username\"\n",
                "sf_password = \"your_password\"\n",
                "agentforce = Agentforce(username=sf_username, password=sf_password)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Part 1: AgentForce as a Tool in LangChain\n",
                "\n",
                "In this example, we'll create a LangChain tool that uses the AgentForce SDK to interact with an agent."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "from langchain.tools import tool\n",
                "from langchain.agents import AgentExecutor, create_openai_tools_agent\n",
                "from langchain_core.tools import Tool\n",
                "\n",
                "# Define a tool for interacting with the AgentForce agent\n",
                "@tool\n",
                "def query_agent(query: str) -> str:\n",
                "    \"\"\"Use this to ask questions to the OrderManagementAgent in Salesforce.\"\"\"\n",
                "    agent_name = \"OrderManagementAgent\"  # Replace with your agent name\n",
                "    response = agentforce.send_message(\n",
                "        agent_name=agent_name,\n",
                "        user_message=query\n",
                "    )\n",
                "    return response['agent_response']\n",
                "\n",
                "# Create a LangChain agent with our custom tool\n",
                "tools = [query_agent]\n",
                "llm = ChatOpenAI(model=\"gpt-4-turbo\", temperature=0)\n",
                "\n",
                "prompt = ChatPromptTemplate.from_messages([\n",
                "    (\"system\", \"You are an AI assistant with access to a Salesforce agent for order management. \"\n",
                "              \"Use the tools available to help answer questions about orders.\"),\n",
                "    (\"human\", \"{input}\"),\n",
                "    (\"user\", \"{agent_scratchpad}\")\n",
                "])\n",
                "\n",
                "agent = create_openai_tools_agent(llm, tools, prompt)\n",
                "agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Test the LangChain agent\n",
                "agent_executor.invoke({\"input\": \"I'm looking for information about my order #12345. Can you help me?\"})"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Part 2: Building a Customer Support Workflow with LangGraph\n",
                "\n",
                "Here we'll create a more complex workflow using LangGraph, which handles customer inquiries by routing them to different systems including AgentForce."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "from typing import List, Dict, TypedDict, Annotated, Literal\n",
                "import json\n",
                "\n",
                "# Define our state\n",
                "class State(TypedDict):\n",
                "    query: str\n",
                "    category: str\n",
                "    answer: str\n",
                "    history: List[Dict]\n",
                "\n",
                "# Function to categorize the customer query\n",
                "def categorize(state: State) -> State:\n",
                "    prompt = ChatPromptTemplate.from_messages([\n",
                "        (\"system\", \"Categorize the user query into one of these categories: 'order', 'payment', 'general', 'escalate'\"),\n",
                "        (\"human\", \"{query}\")\n",
                "    ])\n",
                "    chain = prompt | ChatOpenAI(temperature=0) | StrOutputParser()\n",
                "    category = chain.invoke({\"query\": state[\"query\"]})\n",
                "    return {**state, \"category\": category.lower().strip()}\n",
                "\n",
                "# Function to handle order queries with AgentForce\n",
                "def handle_order_query(state: State) -> State:\n",
                "    agent_name = \"OrderManagementAgent\"  # Replace with your agent name\n",
                "    response = agentforce.send_message(\n",
                "        agent_name=agent_name,\n",
                "        user_message=state[\"query\"]\n",
                "    )\n",
                "    return {**state, \"answer\": response['agent_response']}\n",
                "\n",
                "# Function to handle payment queries\n",
                "def handle_payment_query(state: State) -> State:\n",
                "    prompt = ChatPromptTemplate.from_messages([\n",
                "        (\"system\", \"You are a payment specialist. Answer the user's payment-related query.\"),\n",
                "        (\"human\", \"{query}\")\n",
                "    ])\n",
                "    chain = prompt | ChatOpenAI(temperature=0) | StrOutputParser()\n",
                "    answer = chain.invoke({\"query\": state[\"query\"]})\n",
                "    return {**state, \"answer\": answer}\n",
                "\n",
                "# Function to handle general queries\n",
                "def handle_general_query(state: State) -> State:\n",
                "    prompt = ChatPromptTemplate.from_messages([\n",
                "        (\"system\", \"You are a general customer support assistant. Answer the user's query.\"),\n",
                "        (\"human\", \"{query}\")\n",
                "    ])\n",
                "    chain = prompt | ChatOpenAI(temperature=0) | StrOutputParser()\n",
                "    answer = chain.invoke({\"query\": state[\"query\"]})\n",
                "    return {**state, \"answer\": answer}\n",
                "\n",
                "# Function to handle escalations\n",
                "def handle_escalation(state: State) -> State:\n",
                "    return {**state, \"answer\": \"I'm escalating your issue to a human agent who will contact you shortly. Your reference number is ESC-\" + str(hash(state[\"query\"]) % 10000)}\n",
                "\n",
                "# Function to decide next step based on category\n",
                "def route_query(state: State) -> Literal[\"order\", \"payment\", \"general\", \"escalate\"]:\n",
                "    category = state[\"category\"]\n",
                "    if \"order\" in category:\n",
                "        return \"order\"\n",
                "    elif \"payment\" in category:\n",
                "        return \"payment\"\n",
                "    elif \"escalate\" in category:\n",
                "        return \"escalate\"\n",
                "    else:\n",
                "        return \"general\"\n",
                "\n",
                "# Building the graph\n",
                "customer_support_graph = StateGraph(State)\n",
                "\n",
                "# Add the nodes\n",
                "customer_support_graph.add_node(\"categorize\", categorize)\n",
                "customer_support_graph.add_node(\"order\", handle_order_query)\n",
                "customer_support_graph.add_node(\"payment\", handle_payment_query)\n",
                "customer_support_graph.add_node(\"general\", handle_general_query)\n",
                "customer_support_graph.add_node(\"escalate\", handle_escalation)\n",
                "\n",
                "# Add edges\n",
                "customer_support_graph.add_edge(\"categorize\", route_query)\n",
                "customer_support_graph.add_edge(\"order\", END)\n",
                "customer_support_graph.add_edge(\"payment\", END)\n",
                "customer_support_graph.add_edge(\"general\", END)\n",
                "customer_support_graph.add_edge(\"escalate\", END)\n",
                "\n",
                "# Set the entry point\n",
                "customer_support_graph.set_entry_point(\"categorize\")\n",
                "\n",
                "# Compile the graph\n",
                "customer_support_app = customer_support_graph.compile()"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Test the LangGraph workflow\n",
                "result = customer_support_app.invoke({\n",
                "    \"query\": \"I need to check the status of my order #54321\",\n",
                "    \"category\": \"\",\n",
                "    \"answer\": \"\",\n",
                "    \"history\": []\n",
                "})\n",
                "\n",
                "print(\"Query Category:\", result[\"category\"])\n",
                "print(\"\\nResponse:\")\n",
                "print(result[\"answer\"])"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Part 3: Enhancing AgentForce with RAG using LlamaIndex\n",
                "\n",
                "Now we'll demonstrate how to use LlamaIndex to create a knowledge base for an AgentForce agent, enabling it to access custom data."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Create a simple knowledge base folder and document\n",
                "import os\n",
                "os.makedirs(\"knowledge_base\", exist_ok=True)\n",
                "\n",
                "# Create a sample product catalog document\n",
                "with open(\"knowledge_base/product_catalog.txt\", \"w\") as f:\n",
                "    f.write(\"\"\"\n",
                "Product Catalog - Spring 2025\n",
                "\n",
                "Product ID: P001\n",
                "Name: Premium Widget\n",
                "Price: $99.99\n",
                "Description: Our flagship widget with advanced features.\n",
                "Stock: 250 units\n",
                "\n",
                "Product ID: P002\n",
                "Name: Economy Widget\n",
                "Price: $49.99\n",
                "Description: Affordable option with essential features.\n",
                "Stock: 500 units\n",
                "\n",
                "Product ID: P003\n",
                "Name: Professional Gadget\n",
                "Price: $149.99\n",
                "Description: High-performance tool for professionals.\n",
                "Stock: 100 units\n",
                "\"\"\")"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Load documents from the knowledge base\n",
                "documents = SimpleDirectoryReader(\"knowledge_base\").load_data()\n",
                "\n",
                "# Create a vector index from the documents\n",
                "index = VectorStoreIndex.from_documents(documents)\n",
                "\n",
                "# Create a query engine\n",
                "query_engine = index.as_query_engine()"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Create an enhanced AgentForce function that uses LlamaIndex for product info\n",
                "def enhanced_agent_query(query):\n",
                "    # First check if it's a product query\n",
                "    if \"product\" in query.lower() or \"item\" in query.lower() or \"catalog\" in query.lower():\n",
                "        # Use LlamaIndex to answer product-related questions\n",
                "        result = query_engine.query(query)\n",
                "        return str(result)\n",
                "    else:\n",
                "        # Use AgentForce for other queries\n",
                "        agent_name = \"OrderManagementAgent\"  # Replace with your agent name\n",
                "        response = agentforce.send_message(\n",
                "            agent_name=agent_name,\n",
                "            user_message=query\n",
                "        )\n",
                "        return response['agent_response']\n",
                "\n",
                "# Test the enhanced query function\n",
                "print(\"Product Query Example:\")\n",
                "print(enhanced_agent_query(\"What is the price of the Premium Widget?\"))\n",
                "print(\"\\nOrder Query Example:\")\n",
                "print(enhanced_agent_query(\"What's the status of order #12345?\"))"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Part 4: Building a Hybrid Agent System\n",
                "\n",
                "Now let's put it all together to create a hybrid system that combines LangChain, LangGraph, and LlamaIndex with AgentForce."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Create a tool for our LangChain agent that uses the enhanced function\n",
                "@tool\n",
                "def hybrid_query(query: str) -> str:\n",
                "    \"\"\"Query the hybrid system that combines product knowledge and order management.\"\"\"\n",
                "    return enhanced_agent_query(query)\n",
                "\n",
                "# Create a LangChain agent with our hybrid tool\n",
                "hybrid_tools = [hybrid_query]\n",
                "\n",
                "prompt = ChatPromptTemplate.from_messages([\n",
                "    (\"system\", \"You are a comprehensive customer service assistant that can help with product information \"\n",
                "              \"and order management. Use the tools available to provide the best assistance.\"),\n",
                "    (\"human\", \"{input}\"),\n",
                "    (\"user\", \"{agent_scratchpad}\")\n",
                "])\n",
                "\n",
                "hybrid_agent = create_openai_tools_agent(llm, hybrid_tools, prompt)\n",
                "hybrid_executor = AgentExecutor(agent=hybrid_agent, tools=hybrid_tools, verbose=True)"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Test the hybrid system with a product query\n",
                "hybrid_executor.invoke({\"input\": \"What products do you have in stock and how much do they cost?\"})"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Test the hybrid system with an order query\n",
                "hybrid_executor.invoke({\"input\": \"I'd like to check the status of my order #54321 and also learn about the Professional Gadget.\"})"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Part 5: Creating an Integrated AgentForce Agent\n",
                "\n",
                "Finally, let's demonstrate how to create and deploy an AgentForce agent that can leverage these integrations."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Define an action that will use our LlamaIndex knowledge base\n",
                "product_lookup_action = Action(\n",
                "    name=\"lookupProductInfo\",\n",
                "    description=\"Look up information about products in the catalog\",\n",
                "    inputs=[\n",
                "        Input(\n",
                "            name=\"productQuery\",\n",
                "            description=\"Query about a product\",\n",
                "            data_type=\"string\"\n",
                "        )\n",
                "    ],\n",
                "    outputs=[\n",
                "        Output(\n",
                "            name=\"productInfo\",\n",
                "            description=\"Information about the requested product\",\n",
                "            data_type=\"string\"\n",
                "        )\n",
                "    ]\n",
                ")\n",
                "\n",
                "# Define a topic for product information\n",
                "product_topic = Topic(\n",
                "    name=\"Product Information\",\n",
                "    description=\"Provides information about products in the catalog\",\n",
                "    scope=\"public\",\n",
                "    instructions=[\n",
                "        \"When a user asks about a product, use the product lookup action to find information\",\n",
                "        \"Provide details such as price, description, and availability\"\n",
                "    ],\n",
                "    actions=[product_lookup_action]\n",
                ")\n",
                "\n",
                "# Define our integrated agent\n",
                "integrated_agent = Agent(\n",
                "    name=\"IntegratedShopAgent\",\n",
                "    description=\"A comprehensive shopping assistant that helps with product information and order management\",\n",
                "    agent_type=\"External\",\n",
                "    agent_template_type=\"EinsteinServiceAgent\",\n",
                "    company_name=\"Example Corp\",\n",
                "    sample_utterances=[\n",
                "        \"What products do you have available?\",\n",
                "        \"I'd like to check the status of my order\",\n",
                "        \"Tell me about the Premium Widget\"\n",
                "    ],\n",
                "    topics=[product_topic]\n",
                ")\n",
                "\n",
                "# This is where you would deploy the agent to Salesforce\n",
                "# result = agentforce.create(integrated_agent)\n",
                "# print(f\"Agent created successfully: {result}\")\n",
                "\n",
                "# Instead of deploying, let's just print the agent configuration\n",
                "print(integrated_agent.to_json())"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Conclusion\n",
                "\n",
                "In this notebook, we've demonstrated multiple ways to integrate the AgentForce SDK with modern AI frameworks:\n",
                "\n",
                "1. Using AgentForce as a tool in LangChain\n",
                "2. Building a customer support workflow with LangGraph that incorporates AgentForce\n",
                "3. Enhancing AgentForce with RAG capabilities using LlamaIndex\n",
                "4. Creating a hybrid system that combines all three frameworks\n",
                "5. Designing an integrated AgentForce agent that leverages these capabilities\n",
                "\n",
                "These integrations enable powerful capabilities such as:\n",
                "\n",
                "* Smart routing of customer inquiries\n",
                "* Access to external knowledge bases\n",
                "* Multi-agent coordination\n",
                "* Stateful conversations\n",
                "\n",
                "To implement this in a production environment, you would need to:\n",
                "\n",
                "1. Deploy the integrated AgentForce agent to Salesforce\n",
                "2. Set up a service to handle the LlamaIndex knowledge base\n",
                "3. Configure webhooks to connect external systems with the AgentForce agent\n",
                "4. Implement authentication and security measures\n",
                "\n",
                "For more information, refer to the documentation for each framework."
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

# Write the notebook to file
with open(os.path.join(notebooks_dir, 'advanced_integrations.ipynb'), 'w') as f:
    json.dump(advanced_notebook, f, indent=1)

print("Advanced integrations notebook created successfully!") 