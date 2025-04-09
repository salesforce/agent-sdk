#!/usr/bin/env python3
"""Example script demonstrating how to export a Salesforce agent to modular format."""

import os
import sys
import argparse

# Add parent directory to Python path so we can import agent_sdk directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent_sdk import Agentforce
from agent_sdk.core.auth import BasicAuth

def main():
    """Main function demonstrating agent export."""
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Export Salesforce agent to modular format')
    parser.add_argument('--username', required=True, help='Salesforce username')
    parser.add_argument('--password', required=True, help='Salesforce password')
    parser.add_argument('--domain', default='login', help='Salesforce domain (login/test)')
    parser.add_argument('--agent_name', required=True, help='Name of the Salesforce bot/agent to export')
    parser.add_argument('--output_dir', required=False, help='Output directory for the generated agent')
    args = parser.parse_args()
    
    try:
        # Initialize the SDK
        auth = BasicAuth(
            username=args.username,
            password=args.password,
            domain=args.domain
        )
        agentforce = Agentforce(auth=auth)
        
        # Create output directory
        output_dir = args.output_dir if args.output_dir else os.path.join(os.path.dirname(__file__), "exported_agents")
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"\nExporting Salesforce agent '{args.agent_name}' to modular format...")
        
        # Export agent
        agent_dir = agentforce.export_agent_from_salesforce(
            agent_name=args.agent_name,
            output_dir=output_dir
        )
        
        print(f"\nAgent successfully exported to: {agent_dir}")
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 