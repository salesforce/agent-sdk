#!/usr/bin/env python3
"""Example script demonstrating how to generate a prompt template with Apex invocable actions."""

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

def print_field_info(field_name, salesforce_object=None):
    """Print information about a field in a consistent format."""
    if salesforce_object == "apex":
        print(f"  - {field_name} (Apex Action)")
    else:
        print(f"  - {field_name} ({salesforce_object})")

def main():
    """Main function demonstrating prompt template generation with Apex actions."""
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Generate a prompt template with Apex actions')
    parser.add_argument('--username', required=True, help='Salesforce username')
    parser.add_argument('--password', required=True, help='Salesforce password')
    parser.add_argument('--security_token', required=True, help='Salesforce security token')
    parser.add_argument('--output_dir', default='templates', help='Output directory for templates')
    parser.add_argument('--model', default='gpt-4', help='Model to use for template generation')
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

        # Generate Account Opportunity Analysis Template with Apex actions
        template = prompt_utils.generate_prompt_template(
            name="Account Opportunity Analysis Template",
            description="""Create a comprehensive opportunity analysis for an account that includes:
1. Summary of recent opportunities (last 90 days)
2. Win/loss trends
3. Total pipeline value
4. Average deal size
5. Sales cycle analysis
6. Key opportunity stages distribution""",
            object_names=["Account", "Opportunity"],
            output_dir=args.output_dir,
            model=args.model
        )

        print("\nGenerated template fields:")
        for field in template.input_fields:
            print_field_info(field.name, field.salesforce_object)

        print("\nGenerated Apex classes:")
        apex_dir = os.path.join(args.output_dir, "apex")
        if os.path.exists(apex_dir):
            for file in os.listdir(apex_dir):
                if file.endswith(".cls"):
                    print(f"  - {file}")

        # Save the template
        template_path = prompt_utils.save_prompt_template(template, args.output_dir)
        print(f"\nTemplate saved to: {template_path}")

    except Exception as e:
        logger.error(f"Error generating template: {str(e)}")
        raise

if __name__ == "__main__":
    main() 