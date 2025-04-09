#!/usr/bin/env python3
"""Example script demonstrating how to tune an existing prompt template for different models."""

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
    """Main function demonstrating prompt template tuning."""
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Tune a prompt template for different models')
    parser.add_argument('--username', required=True, help='Salesforce username')
    parser.add_argument('--password', required=True, help='Salesforce password')
    parser.add_argument('--security_token', required=True, help='Salesforce security token')
    parser.add_argument('--template_path', required=True, help='Path to the template JSON file')
    parser.add_argument('--output_dir', default='templates', help='Output directory for tuned templates')
    parser.add_argument('--model', default='gpt-4', help='Model to tune for (gpt-4, gpt-4o, llama-2)')
    parser.add_argument('--description', help='Additional context or requirements for tuning')
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

        # Load and tune the template
        description = args.description or """Enhance the template by:
1. Optimizing for one-shot responses
2. Adding more explicit instructions
3. Including validation rules
4. Improving error handling guidance"""

        tuned_template = prompt_utils.tune_prompt_template(
            template_path=args.template_path,
            description=description,
            model=args.model,
            output_dir=args.output_dir
        )

        print("\nTuned template fields:")
        for field in tuned_template.input_fields:
            print_field_info(field.name, field.salesforce_object)

        print("\nGenerated Apex classes:")
        apex_dir = os.path.join(args.output_dir, "apex")
        if os.path.exists(apex_dir):
            for file in os.listdir(apex_dir):
                if file.endswith(".cls"):
                    print(f"  - {file}")

        # Save the tuned template
        template_path = prompt_utils.save_prompt_template(tuned_template, args.output_dir)
        print(f"\nTuned template saved to: {template_path}")

    except Exception as e:
        logger.error(f"Error tuning template: {str(e)}")
        raise

if __name__ == "__main__":
    main() 