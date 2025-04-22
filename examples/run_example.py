#!/usr/bin/env python3
"""Helper script to run any example without needing to install the package."""

import os
import sys
import argparse
import importlib.util
from typing import Optional

def import_example_module(example_name: str) -> Optional[object]:
    """Import an example module by name."""
    # Add parent directory to Python path
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sys.path.insert(0, parent_dir)
    
    # Construct the full path to the example file
    if not example_name.endswith('.py'):
        example_name += '.py'
    example_path = os.path.join(os.path.dirname(__file__), example_name)
    
    if not os.path.exists(example_path):
        print(f"Error: Example file '{example_name}' not found")
        return None
    
    # Import the module
    spec = importlib.util.spec_from_file_location(example_name, example_path)
    if not spec or not spec.loader:
        print(f"Error: Could not load example '{example_name}'")
        return None
        
    module = importlib.util.module_from_spec(spec)
    sys.modules[example_name] = module
    spec.loader.exec_module(module)
    return module

def list_examples() -> None:
    """List all available examples."""
    examples_dir = os.path.dirname(__file__)
    examples = [f for f in os.listdir(examples_dir) 
               if f.endswith('.py') and f not in ['__init__.py', 'run_example.py']]
    
    print("\nAvailable examples:")
    for example in examples:
        # Load the module to get its docstring
        module = import_example_module(example)
        if module and module.__doc__:
            description = module.__doc__.split('\n')[0]
        else:
            description = "No description available"
        print(f"  {example[:-3]:<30} {description}")

def main():
    """Main function to run examples."""
    parser = argparse.ArgumentParser(description='Run AgentForce SDK examples')
    parser.add_argument('example', nargs='?', help='Name of the example to run (without .py)')
    parser.add_argument('--list', '-l', action='store_true', help='List available examples')
    parser.add_argument('args', nargs=argparse.REMAINDER, help='Arguments to pass to the example')
    
    args = parser.parse_args()
    
    if args.list:
        list_examples()
        return 0
    
    if not args.example:
        parser.print_help()
        print("\nUse --list to see available examples")
        return 1
    
    # Import and run the example
    module = import_example_module(args.example)
    if not module:
        return 1
    
    # Run the example's main function with any additional arguments
    if hasattr(module, 'main'):
        # Replace sys.argv with the example's arguments
        sys.argv = [sys.argv[0]] + args.args
        return module.main()
    else:
        print(f"Error: Example '{args.example}' has no main() function")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 