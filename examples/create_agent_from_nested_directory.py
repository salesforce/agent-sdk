#!/usr/bin/env python3

"""
Example: Create an agent using modular JSON files
"""

import os
import sys
import argparse

# Add parent directory to Python path so we can import agent_sdk directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent_sdk import Agentforce
from agent_sdk.utils.agent_utils import AgentUtils
from agent_sdk.core.auth import BasicAuth

def main():
    parser = argparse.ArgumentParser(description='Create an AgentForce agent from modular files')
    parser.add_argument('--username', required=True, help='Salesforce username')
    parser.add_argument('--password', required=True, help='Salesforce password')
    parser.add_argument('--agent_directory', required=True, help='Directory containing the agent files')
    parser.add_argument('--agent_name', required=True, help='Name of the agent')
    args = parser.parse_args()
    
    try:
        # Initialize the AgentForce client
        auth = BasicAuth(
            username=args.username,
            password=args.password
        )
        client = Agentforce(auth=auth)
        
        # Create the agent from modular files using AgentUtils
        print(f"Loading agent '{args.agent_name}' from nested directory: {args.agent_directory}")
        agent = AgentUtils.create_agent_from_directory_structure(args.agent_directory, args.agent_name)
        
        # Print the agent configuration
        print("Agent Configuration Loaded:")
        print(agent.to_json())
        
        # Create the agent in Salesforce
        print(f"Attempting to create agent: {agent.name}...")
        result = client.create(agent)

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
        raise RuntimeError(f"Error during agent creation process: {str(e)}")

if __name__ == "__main__":
    main() 