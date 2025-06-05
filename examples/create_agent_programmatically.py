#!/usr/bin/env python3

"""
Example: Create an agent programmatically
"""

import argparse
import os
import sys

# Add parent directory to Python path so we can import agent_sdk directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent_sdk import Agentforce
from agent_sdk.core.auth import BasicAuth
from agent_sdk.models.action import Action, Input, Output
from agent_sdk.models.agent import Agent
from agent_sdk.models.attribute_mapping import AttributeMapping
from agent_sdk.models.system_message import SystemMessage
from agent_sdk.models.topic import Topic
from agent_sdk.models.variable import Variable

# Define all agent variables upfront
def create_agent_variables():
    """Create all variables needed for the agent."""
    customer_id_var = Variable(
        name="customer_id", 
        description="Customer's unique identifier",
        data_type="Text",
        include_in_prompt=True,
        visibility="Internal",
        var_type="conversation",
        developer_name="customer_id",
        label="Customer ID"
    )
    
    last_order_id_var = Variable(
        name="last_order_id",
        description="ID of the customer's most recent order",
        data_type="Text",
        include_in_prompt=True,
        visibility="Internal",
        var_type="conversation",
        developer_name="last_order_id",
        label="Last Order ID"
    )
    
    current_reservation_id_var = Variable(
        name="current_reservation_id",
        description="ID of the customer's current reservation",
        data_type="Text",
        include_in_prompt=True,
        visibility="Internal",
        var_type="conversation",
        developer_name="current_reservation_id",
        label="Current Reservation ID"
    )
    
    customer_name_var = Variable(
        name="customer_name",
        description="Customer's full name",
        data_type="Text",
        include_in_prompt=True,
        visibility="Internal",
        var_type="conversation",
        developer_name="customer_name",
        label="Customer Name"
    )
    
    preferred_contact_method_var = Variable(
        name="preferred_contact_method",
        description="Customer's preferred contact method",
        data_type="Text",
        include_in_prompt=False,
        visibility="Internal",
        var_type="conversation",
        developer_name="preferred_contact_method",
        label="Preferred Contact Method"
    )
    
    return {
        "customer_id": customer_id_var,
        "last_order_id": last_order_id_var,
        "current_reservation_id": current_reservation_id_var,
        "customer_name": customer_name_var,
        "preferred_contact_method": preferred_contact_method_var
    }


def create_order_management_topic(variables) -> Topic:
    """Create the Order Management topic with its actions."""
    # Create the topic
    topic = Topic(
        name="Order Management",
        description="Handle order-related queries and actions",
        scope="Handle order-related queries and actions",
    )

    # Set instructions
    topic.instructions = [
        "Process order requests efficiently",
        "Validate order details before confirmation",
        "Provide clear order status updates",
    ]

    # Get variables needed for this topic
    customer_variable = variables["customer_id"]
    order_id_variable = variables["last_order_id"]

    # Create and configure actions
    place_order_action = Action(
        name="Place Order",
        description="Place an order for a product",
        inputs=[
            Input(
                name="product_id",
                description="ID of the product to order",
                data_type="String",
                required=True,
            ),
            Input(
                name="quantity",
                description="Quantity of the product",
                data_type="Number",
                required=True,
            ),
            Input(
                name="customer_id",
                description="ID of the customer placing the order",
                data_type="String",
                required=True,
            ),
        ],
        outputs=[
            Output(
                name="status",
                description="Status of the order placement",
                data_type="String",
                required=True,
            ),
            Output(
                name="order_id",
                description="Unique identifier for the order",
                data_type="String",
                required=True,
            ),
            Output(
                name="message",
                description="Status message for the order",
                data_type="String",
                required=True,
            ),
        ],
        example_output=Output(
            status="success",
            order_id="12345",
            message="Order placed successfully",
        ),
    )
    
    # Map customer_id input parameter to customer_id variable
    place_order_action.attribute_mappings.append(
        AttributeMapping(
            action_parameter="customer_id",
            variable=customer_variable,
            direction="input"
        )
    )
    
    # Map order_id output to last_order_id variable
    place_order_action.attribute_mappings.append(
        AttributeMapping(
            action_parameter="order_id",
            variable=order_id_variable,
            direction="output"
        )
    )
    
    check_order_action = Action(
        name="Check Order Status",
        description="Check the status of an order",
        inputs=[
            Input(
                name="order_id",
                description="ID of the order to check",
                data_type="String",
                required=True,
            )
        ],
        outputs=[
            Output(
                name="status",
                description="Status of the order status check",
                data_type="String",
                required=True,
            ),
            Output(
                name="order_status",
                description="Current status of the order",
                data_type="String",
                required=True,
            ),
            Output(
                name="estimated_delivery",
                description="Estimated delivery date",
                data_type="String",
                required=True,
            ),
        ],
        example_output=Output(
            status="success",
            order_status="processing",
            estimated_delivery="2024-03-20",
        ),
    )
    
    # Map order_id input to last_order_id variable
    check_order_action.attribute_mappings.append(
        AttributeMapping(
            action_parameter="order_id",
            variable=order_id_variable,
            direction="input"
        )
    )

    # Set the actions for the topic
    topic.actions = [place_order_action, check_order_action]
    return topic


def create_reservation_management_topic(variables) -> Topic:
    """Create the Reservation Management topic with its actions."""
    # Create the topic
    topic = Topic(
        name="Reservation Management",
        description="Handle reservation-related queries and actions",
        scope="Handle reservation-related queries and actions",
    )

    # Set instructions
    topic.instructions = [
        "Process reservation requests efficiently",
        "Check availability before confirming reservations",
        "Handle reservation modifications and cancellations",
    ]
    
    # Get variables needed for this topic
    customer_variable = variables["customer_id"]
    reservation_id_variable = variables["current_reservation_id"]

    # Create and configure actions
    make_reservation_action = Action(
        name="Make Reservation",
        description="Make a reservation for a table",
        inputs=[
            Input(
                name="date",
                description="Reservation date",
                data_type="Date",
                required=True,
            ),
            Input(
                name="time",
                description="Reservation time",
                data_type="Time",
                required=True,
            ),
            Input(
                name="party_size",
                description="Number of people",
                data_type="Number",
                required=True,
            ),
            Input(
                name="customer_id",
                description="ID of the customer making the reservation",
                data_type="String",
                required=True,
            ),
        ],
        outputs=[
            Output(
                name="status",
                description="Status of the reservation request",
                data_type="String",
                required=True,
            ),
            Output(
                name="reservation_id",
                description="Unique identifier for the reservation",
                data_type="String",
                required=True,
            ),
            Output(
                name="confirmation",
                description="Confirmation message for the reservation",
                data_type="String",
                required=True,
            ),
        ],
        example_output=Output(
            status="success",
            reservation_id="R123",
            confirmation="Reservation confirmed",
        ),
    )
    
    # Map customer_id input parameter to customer_id variable
    make_reservation_action.attribute_mappings.append(
        AttributeMapping(
            action_parameter="customer_id",
            variable=customer_variable,
            direction="input"
        )
    )
    
    # Map reservation_id output to current_reservation_id variable
    make_reservation_action.attribute_mappings.append(
        AttributeMapping(
            action_parameter="reservation_id",
            variable=reservation_id_variable,
            direction="output"
        )
    )

    # Set the actions for the topic
    topic.actions = [make_reservation_action]
    return topic


def main():
    # Initialize AgentForce client
    parser = argparse.ArgumentParser(
        description="Create an AgentForce agent from JSON file"
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

    # Create all variables first
    variables = create_agent_variables()

    # Create the agent
    agent = Agent(
        name="Order Management Agent",
        description="An agent that helps customers manage their orders and reservations",
        agent_type="External",
        company_name="Salesforce",
    )

    # Set sample utterances for the agent
    agent.sample_utterances = [
        "I want to place an order",
        "Check my order status",
        "I need to make a reservation",
        "What's my order tracking number?",
        "Can I modify my reservation?",
    ]

    # Set system messages for the agent
    agent.system_messages = [
        SystemMessage(
            message="You are a helpful order management assistant.", msg_type="system"
        ),
        SystemMessage(
            message="Always be professional and courteous.", msg_type="system"
        ),
    ]

    # Set variables for the agent using the pre-defined variables
    agent.variables = list(variables.values())

    # Create topics with the pre-defined variables
    order_topic = create_order_management_topic(variables)
    reservation_topic = create_reservation_management_topic(variables)

    # Set topics for the agent
    agent.topics = [order_topic, reservation_topic]

    try:
        # Create the agent in Salesforce
        print(f"Attempting to create agent: {agent.name}...")
        auth = BasicAuth(
            username=args.username,
            password=args.password,
            security_token=args.security_token,
        )
        agentforce = Agentforce(auth=auth)
        result = agentforce.create(agent)

        # --- Check if create() returned None (early failure) ---
        if result is None:
            raise RuntimeError(
                f"Agent '{agent.name}' creation failed before deployment could start. Check logs for authentication or setup errors."
            )

        # --- Check deployment status ---
        deployment_status = result.get("deployResult", {}).get("status")
        deployment_id = result.get("id", "N/A")

        if deployment_status == "Succeeded":
            print(
                f"Agent '{agent.name}' deployed successfully. Deployment ID: {deployment_id}"
            )
        else:
            error_message = f"Agent '{agent.name}' deployment did not succeed. Status: {deployment_status}. Full Result: {result}"
            raise RuntimeError(error_message)  # Raise exception on failure

    except Exception as e:
        # Catch and re-raise other exceptions during the process
        raise RuntimeError(f"Error during agent creation process: {str(e)}")


if __name__ == "__main__":
    main()
