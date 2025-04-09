#!/usr/bin/env python3
"""Example script demonstrating how to create Apex classes for agent actions."""

import os
import sys
import json
import argparse

# Add parent directory to Python path so we can import agent_sdk directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent_sdk import Agentforce
from agent_sdk.core.auth import BasicAuth
from agent_sdk.models.action import Action, Input, Output
from agent_sdk.models.topic import Topic

def create_order_processing_example():
    """Example creating an Apex class for order processing."""
    
    # Create a topic for order management
    topic = Topic(
        name="OrderManagement",
        description="Handles all order-related operations",
        scope="Handles all order-related operations",
    )
    
    # Create an action with complex input/output schemas
    action = Action(
            name="processOrder",
            description="Processes an order and returns its status",
            inputs=[
                Input(
                    name="orderId",
                    description="ID of the order to process",
                    data_type="String",
                    required=True
                ),
                Input(
                    name="includeDetails",
                    description="Whether to include detailed information",
                    data_type="Boolean",
                    required=False
                )
            ],
            outputs=[
                Output(
                    name="orderStatus",
                    description="Current status of the order",
                    data_type="String",
                    required=True
                ),
                Output(
                    name="estimatedDelivery",
                    description="Estimated delivery date and time",
                    data_type="DateTime",
                    required=False
                ),
                Output(
                    name="orderDetails",
                    description="Detailed information about the order",
                    data_type="Map<String,Object>",
                    required=False
                )
            ],
            example_output=Output(
                status="success",
                details={
                    "orderStatus": "processing",
                    "estimatedDelivery": "2024-03-20T15:30:00Z",
                    "orderDetails": {
                        "items": [
                            {"id": "123", "quantity": 2, "price": 29.99}
                        ],
                        "totalAmount": 59.98,
                        "shippingMethod": "express"
                    }
                }
            )
        )
    
    return topic, action


def create_customer_verification_example():
    """Example creating an Apex class for customer verification."""
    
    topic = Topic(
        name="CustomerVerification",
        description="Handles customer verification and validation",
        scope="Customer identity and access management",
    )
    
    action = Action(
            name="verifyCustomer",
            description="Verifies customer identity and returns verification status",
            inputs=[
                Input(
                    name="customerId",
                    description="Unique identifier for the customer",
                    data_type="String",
                    required=True
                ),
                Input(
                    name="documentType",
                    description="Type of verification document provided",
                    data_type="String",
                    required=True
                ),
                Input(
                    name="documentNumber",
                    description="Document identification number",
                    data_type="String",
                    required=True
                )
            ],
            outputs=[
                Output(
                    name="isVerified",
                    description="Whether the customer is verified",
                    data_type="Boolean",
                    required=True
                ),
                Output(
                    name="verificationScore",
                    description="Confidence score of the verification",
                    data_type="Decimal",
                    required=True
                ),
                Output(
                    name="verificationDetails",
                    description="Detailed verification results",
                    data_type="Map<String,Object>",
                    required=False
                )
            ],
            example_output=Output(
                status="success",
                details={
                    "isVerified": True,
                    "verificationScore": 0.95,
                    "verificationDetails": {
                        "documentStatus": "valid",
                        "matchScore": 0.95,
                        "verificationDate": "2024-03-27T10:00:00Z"
                    }
                }
            )
        )
    
    return topic, action


def main():
    """Main function demonstrating Apex class creation."""
    
    # Initialize the SDK
    parser = argparse.ArgumentParser(description='Create Apex classes from actions')
    parser.add_argument('--username', required=True, help='Salesforce username')
    parser.add_argument('--password', required=True, help='Salesforce password')
    parser.add_argument('--output_dir', required=False, help='Output directory for Apex classes')
    args = parser.parse_args()
    
    auth = BasicAuth(
        username=args.username,
        password=args.password
    )
    agentforce = Agentforce(auth=auth)
    
    # Create output directory
    output_dir = args.output_dir if args.output_dir else os.path.join(os.path.dirname(__file__), "apex_classes")
    os.makedirs(output_dir, exist_ok=True)
    
    # Example 1: Order Processing
    print("\nCreating Order Processing Apex Class...")
    topic, action = create_order_processing_example()
    try:
        class_path = agentforce.create_apex_class(topic, action, output_dir)
        print(f"Successfully created Apex class at: {class_path}")
    except Exception as e:
        print(f"Error creating Order Processing Apex class: {str(e)}")
    
    # Example 2: Customer Verification
    print("\nCreating Customer Verification Apex Class...")
    topic, action = create_customer_verification_example()
    try:
        class_path = agentforce.create_apex_class(topic, action, output_dir)
        print(f"Successfully created Apex class at: {class_path}")
    except Exception as e:
        print(f"Error creating Customer Verification Apex class: {str(e)}")
    
    
if __name__ == "__main__":
    main() 