#!/usr/bin/env python3
"""Example script demonstrating how to generate and deploy prompt templates for Salesforce agents."""

import os
import sys
import json
import argparse
import time
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
    """Main function demonstrating prompt template generation and deployment."""
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Generate a prompt template example')
    parser.add_argument('--username', required=True, help='Salesforce username')
    parser.add_argument('--password', required=True, help='Salesforce password')
    parser.add_argument('--output_dir', default='templates', help='Output directory for templates')
    parser.add_argument('--model', default='gpt-4', help='Model to use for template generation')
    args = parser.parse_args()
    
    try:
        # Initialize auth
        auth = BasicAuth(
            username=args.username,
            password=args.password
        )
        
        # Initialize AgentforceBase to get Salesforce connection
        base = AgentforceBase(auth=auth)
        
        # Initialize PromptTemplateUtils with Salesforce instance
        prompt_utils = PromptTemplateUtils(base.sf)

        # Generate Account Health Analysis Template
        health_template = prompt_utils.generate_prompt_template(
            name="Account Health Analysis Template",
            description="""Create a comprehensive account health analysis that includes basic information such as industry and type. 
Summarize recent opportunities from the last 90 days, open cases with their status, and recent activities. 
Highlight key metrics and trends based on the activities and interactions.""",
            output_dir=args.output_dir,
            model=args.model
        )

        print("\nGenerated template fields:")
        for field in health_template.fields:
            print_field_info(field.name, field.salesforce_object)

        # Save the template
        template_path = prompt_utils.save_prompt_template(health_template, args.output_dir)
        print(f"\nTemplate saved to: {template_path}")

    except Exception as e:
        logger.error(f"Error generating template: {str(e)}")
        raise

if __name__ == "__main__":
    main() 