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
    parser = argparse.ArgumentParser(description='Create an AgentForce agent from JSON file')
    parser.add_argument('--username', required=True, help='Salesforce username')
    parser.add_argument('--password', required=True, help='Salesforce password')
    parser.add_argument('--security_token', required=False, help='Salesforce security token', default=None)
    args = parser.parse_args()
    
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
    
    try:
        # Create the agent in Salesforce
        print(f"Attempting to create agent: {agent.name}...")
        auth = BasicAuth(
            username=args.username,
            password=args.password,
            security_token=args.security_token
        )
        agentforce = Agentforce(auth=auth)
        result = agentforce.create(agent)

        # --- Check if create() returned None (early failure) ---
        if result is None:
            raise RuntimeError(f"Agent '{agent.name}' creation failed before deployment could start. Check logs for authentication or setup errors.")

        # --- Check deployment status ---
        deployment_status = result.get('deployResult', {}).get('status')
        deployment_id = result.get('id', 'N/A')

        if deployment_status == 'Succeeded':
            print(f"Agent '{agent.name}' deployed successfully. Deployment ID: {deployment_id}")
        else:
            error_message = f"Agent '{agent.name}' deployment did not succeed. Status: {deployment_status}. Full Result: {result}"
            raise RuntimeError(error_message) # Raise exception on failure

    except Exception as e:
        # Catch and re-raise other exceptions during the process
        raise RuntimeError(f"Error during agent creation process: {str(e)}")

if __name__ == "__main__":
    main() 