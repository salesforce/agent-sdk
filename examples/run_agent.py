#!/usr/bin/env python3
"""Example script demonstrating how to run an agent conversation."""

import os
import sys
import argparse

# Add parent directory to Python path so we can import agent_sdk directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent_sdk import Agentforce
from agent_sdk.core.auth import BasicAuth

def main():
    # Initialize the SDK with your credentials
    parser = argparse.ArgumentParser(description='Chat with an Agentforce agent')
    parser.add_argument('--username', required=True, help='Salesforce username')
    parser.add_argument('--password', required=True, help='Salesforce password')
    parser.add_argument('--security_token', required=False, help='Salesforce security token', default=None)
    args = parser.parse_args()
    
    # Initialize AgentForce client
    auth = BasicAuth(
        username=args.username,
        password=args.password,
        security_token=args.security_token
    )
    agent_force = Agentforce(auth=auth)
    
    # Start a conversation with the agent
    session_id = None
    agent_name = "OrderManagementAgent"  # Replace with your agent's API name
    
    # First message
    response = agent_force.send_message(
        agent_name=agent_name,
        user_message="Order number is 1234"
    )
    print("Agent:", response['agent_response'])
    session_id = response['session_id']
    
    # Follow-up message using the session ID
    response = agent_force.send_message(
        agent_name=agent_name,
        user_message="What's the order status?",
        session_id=session_id
    )
    print("Agent:", response['agent_response'])

if __name__ == "__main__":
    main() 