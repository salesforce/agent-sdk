#!/usr/bin/env python3

"""
Example: Create an agent from a JSON file
"""

import os
import sys
import argparse

# Add parent directory to Python path so we can import agent_sdk directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent_sdk import Agentforce
from agent_sdk.models.agent import Agent
from agent_sdk.core.auth import BasicAuth
from agent_sdk.utils.agent_utils import AgentUtils

def main():
    parser = argparse.ArgumentParser(description='Create an AgentForce agent from JSON file')
    parser.add_argument('--username', required=True, help='Salesforce username')
    parser.add_argument('--password', required=True, help='Salesforce password')
    parser.add_argument('--json_file', required=True, help='Path to the JSON file containing agent configuration')
    args = parser.parse_args()
    
    try:
        # Initialize AgentForce client
        auth = BasicAuth(
            username=args.username,
            password=args.password
        )
        agentforce = Agentforce(auth=auth)
        
        # Create agent object from JSON file
        print(f"Loading agent definition from: {args.json_file}")
        agent = AgentUtils.create_agent_from_file(args.json_file)
        print(f"Agent Definition: {agent.to_json()}") # Useful for debugging

        # Create the agent in Salesforce
        print(f"Attempting to create agent: {agent.name}...")
        result = agentforce.create(agent)

        # --- Check if create() returned None (early failure) ---
        if result is None:
            raise RuntimeError(f"Agent '{agent.name}' creation failed before deployment could start. Check logs for authentication or setup errors.")

        # --- Inspect the result from agentforce.create() which contains deploy status ---
        deployment_status = result.get('deployResult', {}).get('status')
        deployment_id = result.get('id', 'N/A')

        if deployment_status == 'Succeeded':
            print(f"Agent '{agent.name}' deployed successfully. Deployment ID: {deployment_id}")
        else:
            # Simplified: Deployment failed or status is unexpected
            error_message = f"Agent '{agent.name}' deployment did not succeed. Status: {deployment_status}. Full Result: {result}"
            raise RuntimeError(error_message) # Raise exception on failure

    except Exception as e:
        # Catch errors from Agentforce client initialization or agent loading
        raise RuntimeError(f"Error during agent creation process for file {args.json_file}: {e}")

if __name__ == "__main__":
    main() 