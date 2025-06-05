#!/usr/bin/env python3

"""
Example: Creating an Agent with Custom Dependent Metadata

This example demonstrates how to create an agent that uses custom Salesforce metadata
instead of the default template classes. It shows a simple order management agent
that uses a custom Apex class for retrieving order information.
"""

import argparse
import sys
from pathlib import Path

# Add the project root to sys.path to import agent_sdk modules
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from agent_sdk import Agentforce
from agent_sdk.core.auth import BasicAuth
from agent_sdk.models.action import Action, Input, Output
from agent_sdk.models.agent import Agent
from agent_sdk.models.system_message import SystemMessage
from agent_sdk.models.topic import Topic

def create_order_management_topic() -> Topic:
    """Create the Order Management topic with its actions."""
    topic = Topic(
        name="Order Management",
        description="Handle order-related queries using custom Apex classes",
        scope="Handle order-related queries and actions",
    )

    topic.instructions = [
        "Always ask for the customer Id and Order Id before answering query about the order status",
        "If a user requests the status of an order, provide a detailed update on the order's current status, including shipping status by using the GetOrderInfo action.",
        "When the user provides the Customer Id and Order Id use and call GetOrderInfo action and display the results from the action in user friendly readable format",
        "If the user does not provide Customer Id and Order Id, ask them to provide one."
    ]

    # Create action that will use custom Apex class
    get_order_info_action = Action(
        name="GetOrderInfo",
        invocation_target="OrderManagementService",
        invocation_target_type="apex",
        description="Get order information using custom Apex class",
        inputs=[
            Input(
                name="orderId",
                description="ID of the order to check",
                data_type="String",
                required=True,
            ),
            Input(
                name="customerId",
                description="ID of the customer",
                data_type="String",
                required=True,
            )
        ],
        outputs=[
            Output(
                name="status",
                description="Status of the order info retrieval",
                data_type="String",
                required=True,
            ),
            Output(
                name="orderDetails",
                description="Details of the order",
                data_type="String",
                required=True,
            )
        ],
        example_output={"status": "success", "order_details": "Order #12345: 2 items, Status: Processing"}
    )

    topic.actions = [get_order_info_action]
    return topic

def main():
    parser = argparse.ArgumentParser(
        description="Create an AgentForce agent with dependent metadata"
    )
    parser.add_argument("--username", required=True, help="Salesforce username")
    parser.add_argument("--password", required=True, help="Salesforce password")
    parser.add_argument(
        "--security_token",
        required=False,
        help="Salesforce security token",
        default=None,
    )
    args = parser.parse_args()


    # Create the agent
    agent = Agent(
        name="Order Management",
        description="An agent that uses custom Apex classes to manage orders",
        agent_type="External",
        company_name="Salesforce",
    )

    # Set sample utterances
    agent.sample_utterances = [
        "What's the status of my order?",
        "Can you check order #12345?",
        "Show me my order details",
        "Get information about my recent order",
    ]

    # Set system messages
    agent.system_messages = [
        SystemMessage(
            message="You are an order management assistant.",
            msg_type="system"
        ),
        SystemMessage(
            message="Always verify order IDs before retrieving information.",
            msg_type="system"
        ),
    ]

    # Set variables and topics
    agent.topics = [create_order_management_topic()]

    try:
        print(f"Creating agent '{agent.name}' with custom metadata...")
        
        # Initialize client and create agent
        auth = BasicAuth(
            username=args.username,
            password=args.password,
            security_token=args.security_token,
        )
        agentforce = Agentforce(auth=auth)
        
        # Specify the path to custom metadata
        metadata_dir = "examples/assets/dependent_metadata_dir/order_management"
        
        # Create agent with dependent metadata
        result = agentforce.create(agent, dependent_metadata_dir=metadata_dir)

        if result is None:
            raise RuntimeError(
                f"Agent creation failed before deployment could start. Check logs for errors."
            )

        deployment_status = result.get("deployResult", {}).get("status")
        deployment_id = result.get("id", "N/A")

        if deployment_status == "Succeeded":
            print(f"Agent deployed successfully with custom metadata. Deployment ID: {deployment_id}")
        else:
            error_message = f"Agent deployment failed. Status: {deployment_status}. Result: {result}"
            raise RuntimeError(error_message)

    except Exception as e:
        raise RuntimeError(f"Error during agent creation: {str(e)}")

if __name__ == "__main__":
    main() 