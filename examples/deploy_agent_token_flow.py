#!/usr/bin/env python3

"""
Example: Create an agent programmatically
"""

import os
import sys
import argparse

# Add parent directory to Python path so we can import agent_sdk directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent_sdk import Agentforce
from agent_sdk.core.auth import BasicAuth
from agent_sdk.models.agent import Agent
from agent_sdk.models.topic import Topic
from agent_sdk.models.action import Action, Input, Output
from agent_sdk.core.auth import ClientCredentialsAuth, JwtBearerAuth
from agent_sdk.models.system_message import SystemMessage
from agent_sdk.models.variable import Variable

def create_order_management_topic() -> Topic:
    """Create the Order Management topic with its actions."""
    # Create the topic
    topic = Topic(
        name="Order Management",
        description="Handle order-related queries and actions",
        scope="Handle order-related queries and actions"
    )
    
    # Set instructions
    topic.instructions = [
        "Process order requests efficiently",
        "Validate order details before confirmation",
        "Provide clear order status updates"
    ]
    
    # Create and configure actions
    actions = [
        Action(
            name="Place Order",
            inputs=[
                Input(name="product_id", description="ID of the product to order", data_type="String", required=True),
                Input(name="quantity", description="Quantity of the product", data_type="Number", required=True)
            ],
            example_output=Output(
                status="success",
                details={"order_id": "12345", "message": "Order placed successfully"}
            )
        ),
        Action(
            name="Check Order Status",
            inputs=[
                Input(
                    name="order_id",
                    description="ID of the order to check",
                    data_type="String",
                    required=True
                )
            ],
            example_output=Output(
                status="success",
                details={"status": "processing", "estimated_delivery": "2024-03-20"}
            )
        )
    ]
    
    # Set the actions for the topic
    topic.actions = actions
    return topic

def create_reservation_management_topic() -> Topic:
    """Create the Reservation Management topic with its actions."""
    # Create the topic
    topic = Topic(
        name="Reservation Management",
        description="Handle reservation-related queries and actions",
        scope="Handle reservation-related queries and actions"
    )
    
    # Set instructions
    topic.instructions = [
        "Process reservation requests efficiently",
        "Check availability before confirming reservations",
        "Handle reservation modifications and cancellations"
    ]
    
    # Create and configure actions
    actions = [
        Action(
            name="Make Reservation",
            inputs=[
                Input(name="date", description="Reservation date", data_type="Date", required=True),
                Input(name="time", description="Reservation time", data_type="Time", required=True),
                Input(name="party_size", description="Number of people", data_type="Number", required=True)
            ],
            example_output=Output(
                status="success",
                details={"reservation_id": "R123", "confirmation": "Reservation confirmed"}
            )
        )
    ]
    
    # Set the actions for the topic
    topic.actions = actions
    return topic

def main():
    # Initialize AgentForce client
    parser = argparse.ArgumentParser(description='Create an AgentForce agent using either Client Credentials or JWT Bearer Flow')
    
    # Common arguments
    parser.add_argument('--domain', required=True, help='Salesforce domain')
    parser.add_argument('--auth_type', choices=['client-credentials', 'jwt'], required=True, help='Authentication type to use')
    parser.add_argument('--custom_domain', help='Custom domain (optional)')
    # Client Credentials Flow arguments
    parser.add_argument('--client_id', help='Salesforce client id (required for both auth types)')
    parser.add_argument('--client_secret', help='Salesforce client secret (required for client-credentials auth)')
    
    # JWT Bearer Flow arguments
    parser.add_argument('--username', help='Salesforce username (required for JWT auth)')
    parser.add_argument('--private_key_path', help='Path to private key file (required for JWT auth)')
    
    args = parser.parse_args()
    
    # Validate arguments based on auth type
    if args.auth_type == 'client-credentials':
        if not args.client_id or not args.client_secret or not args.custom_domain: 
            parser.error('--client_id, --client_secret, and --custom_domain are required for client-credentials auth')
    elif args.auth_type == 'jwt':
        if not args.client_id or not args.username or not args.private_key_path:
            parser.error('--client_id, --username, and --private_key_path are required for JWT auth')
    
    # Create the agent
    agent = Agent(
        name="Order Management Agent",
        description="An agent that helps customers manage their orders and reservations",
        agent_type="External",
        company_name="Salesforce"
    )
    
    # Set sample utterances for the agent
    agent.sample_utterances = [
        "I want to place an order",
        "Check my order status",
        "I need to make a reservation",
        "What's my order tracking number?",
        "Can I modify my reservation?"
    ]
    
    # Set system messages for the agent
    agent.system_messages = [
        SystemMessage(
            message="You are a helpful order management assistant.",
            msg_type="system"
        ),
        SystemMessage(
            message="Always be professional and courteous.",
            msg_type="system"
        )
    ]
    
    # Set variables for the agent
    agent.variables = [
        Variable(
            name="customer_id",
            data_type="String"
        )
    ]
    
    # Create topics
    order_topic = create_order_management_topic()
    reservation_topic = create_reservation_management_topic()
    
    # Set topics for the agent
    agent.topics = [order_topic, reservation_topic]
    
    # Create authentication based on selected type
    if args.auth_type == 'client-credentials':
        auth = ClientCredentialsAuth(
            consumer_key=args.client_id,
            consumer_secret=args.client_secret,
            domain=args.custom_domain
        )
    else:  # JWT auth
        auth = JwtBearerAuth(
            username=args.username,
            consumer_key=args.client_id,
            private_key_path=args.private_key_path,
            domain=args.domain
        )
    
    try:
        # Create the agent in Salesforce
        print(f"Attempting to create agent: {agent.name}...")
        agentforce = Agentforce(auth=auth)
        result = agentforce.create(agent)
        
        # --- Check if create() returned None (early failure) ---
        if result is None:
            raise RuntimeError(f"Agent '{agent.name}' creation failed before deployment could start. Check logs for authentication or setup errors.")

        # --- Check deployment status ---
        deployment_status = result.get('deployResult', {}).get('status')
        deployment_id = result.get('id', 'N/A')

        if deployment_status == 'Succeeded':
            print(f"Agent '{agent.name}' deployed successfully using {args.auth_type}. Deployment ID: {deployment_id}")
        else:
            error_message = f"Agent '{agent.name}' deployment did not succeed. Status: {deployment_status}. Full Result: {result}"
            raise RuntimeError(error_message) # Raise exception on failure

    except Exception as e:
        raise RuntimeError(f"Error during agent creation process: {str(e)}")

if __name__ == "__main__":
    main() 
    
    
    
    
