#!/usr/bin/env python3
"""Example script demonstrating how to deploy a prompt template to Salesforce."""

import os
import sys
import json
import argparse
import logging

# Add parent directory to Python path so we can import agent_sdk directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent_sdk.core.prompt_template_utils import PromptTemplateUtils
from agent_sdk.core.auth import BasicAuth
from agent_sdk.core.base import AgentforceBase

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def print_deployment_status(status):
    """Print deployment status information in a consistent format."""
    print("\nDeployment Status:")
    print(f"  Status: {status.get('status', 'Unknown')}")
    print(f"  Success: {status.get('success', False)}")
    if status.get('errors'):
        print("\nErrors:")
        for error in status['errors']:
            print(f"  - {error}")
    if status.get('details'):
        print("\nDetails:")
        for detail in status['details']:
            print(f"  - {detail}")

def main():
    """Main function demonstrating prompt template deployment."""
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Deploy a prompt template to Salesforce')
    parser.add_argument('--username', required=True, help='Salesforce username')
    parser.add_argument('--password', required=True, help='Salesforce password')
    parser.add_argument('--security_token', required=True, help='Salesforce security token')
    parser.add_argument('--template_path', required=True, help='Path to the template JSON file')
    parser.add_argument('--validate_only', action='store_true', help='Only validate the deployment without actually deploying')
    args = parser.parse_args()
    
    try:
        # Initialize auth
        auth = BasicAuth(
            username=args.username,
            password=args.password,
            security_token=args.security_token
        )
        
        # Initialize AgentforceBase to get Salesforce connection
        base = AgentforceBase(auth=auth)
        
        # Initialize PromptTemplateUtils with Salesforce instance
        prompt_utils = PromptTemplateUtils(base.sf)

        # Load the template
        with open(args.template_path, 'r') as f:
            template_data = json.load(f)

        print(f"\nDeploying template: {template_data.get('name', 'Unknown')}")
        print(f"Description: {template_data.get('description', 'No description provided')}")

        # Deploy the template
        deployment_result = prompt_utils.deploy_prompt_template(
            template_path=args.template_path,
            validate_only=args.validate_only
        )

        # Print deployment status
        print_deployment_status(deployment_result)

        if deployment_result.get('success'):
            print("\nTemplate deployed successfully!")
            print(f"Template API Name: {template_data.get('api_name')}")
            print("\nDeployed Components:")
            print("  - Prompt Template Metadata")
            print("  - Generated Apex Classes")
            if template_data.get('custom_fields'):
                print("  - Custom Fields:")
                for field in template_data['custom_fields']:
                    print(f"    - {field['name']}")

    except Exception as e:
        logger.error(f"Error deploying template: {str(e)}")
        raise

if __name__ == "__main__":
    main() 