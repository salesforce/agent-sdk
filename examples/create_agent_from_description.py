#!/usr/bin/env python3
"""Example script demonstrating how to create an agent from a description."""

import os
import sys
import argparse

# Add parent directory to Python path so we can import agent_sdk directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent_sdk import Agentforce
from agent_sdk.core.auth import BasicAuth
from agent_sdk.utils.agent_utils import AgentUtils

def main():
    parser = argparse.ArgumentParser(description='Create an AgentForce agent from JSON file')
    parser.add_argument('--username', required=True, help='Salesforce username')
    parser.add_argument('--password', required=True, help='Salesforce password')
    parser.add_argument('--output_dir', required=False, help='Output directory for the generated agent')
    
    args = parser.parse_args()
    
    """Main function demonstrating e-commerce agent generation."""
    
    # Agent details
    description = """
    A comprehensive customer service agent for an e-commerce platform that can:
    1. Handle order tracking and status inquiries
    2. Process returns and refunds
    3. Answer product-related questions
    4. Manage shipping and delivery inquiries
    5. Handle account-related issues
    6. Process customer feedback and complaints
    7. Provide inventory and stock information
    The agent should be able to communicate professionally and empathetically,
    following company policies while ensuring customer satisfaction.
    """
    
    company_name = "TechMart Solutions"
    agent_name = "TechMart Customer Service Assistant"  
    # Create output directory
    output_dir = args.output_dir if args.output_dir else os.path.join(os.path.dirname(__file__), "generated_agents", "techmart_assistant")
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Generate agent information
        print("\nGenerating TechMart Customer Service Assistant...")
        AgentUtils.generate_agent_info(
            description=description,
            company_name=company_name,
            agent_name=agent_name,
            output_dir=output_dir
        )
        print(f"\nAgent information generated successfully in: {output_dir}")
        
        # Load and validate the generated agent
        agent = AgentUtils.create_agent_from_directory_structure(output_dir + "/agents", "agent")
        auth = BasicAuth(
            username=args.username,
            password=args.password
        )
        agentforce = Agentforce(auth=auth)
        
        print(f"Attempting to create agent: {agent.name}...")
        result = agentforce.create(agent)

        # --- Check if create() returned None (early failure) ---
        if result is None:
            raise RuntimeError(f"Agent '{agent.name}' creation failed before deployment could start. Check logs for authentication or setup errors.")

        # --- Check deployment status ---
        deployment_status = result.get('deployResult', {}).get('status')
        deployment_id = result.get('id', 'N/A')

        if deployment_status == 'Succeeded':
            print(f"Agent '{agent.name}' deployed successfully. Deployment ID: {deployment_id}")
            # Return 0 on successful deployment
            return 0 
        else:
            error_message = f"Agent '{agent.name}' deployment did not succeed. Status: {deployment_status}. Full Result: {result}"
            raise RuntimeError(error_message) # Raise exception on deployment failure
      
    except Exception as e:
        # Raise exception on other errors (generation, auth, etc.)
        raise RuntimeError(f"\nError during agent generation or deployment: {str(e)}")

if __name__ == "__main__":
    try:
        main()
        sys.exit(0) # Explicitly exit with 0 on success
    except Exception as e:
        # Catch any exception raised from main() and print it
        print(f"Script failed: {e}", file=sys.stderr)
        sys.exit(1) # Exit with 1 on any failure caught here 