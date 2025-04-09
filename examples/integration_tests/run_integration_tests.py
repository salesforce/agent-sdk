#!/usr/bin/env python3
"""Integration tests for AgentForce SDK examples."""

import os
import sys
import uuid
import logging
import asyncio
import importlib.util
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from dotenv import load_dotenv
from tabulate import tabulate
import textwrap

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ANSI color codes for prettier output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
BOLD = "\033[1m"
RESET = "\033[0m"

class IntegrationTests:
    def __init__(self):
        """Initialize the test runner with configuration from environment variables."""
        # Load environment variables
        env_path = Path(__file__).parent / ".env"
        load_dotenv(env_path)
        
        # Required credentials
        self.username = os.getenv("SF_USERNAME")
        self.password = os.getenv("SF_PASSWORD")
        self.security_token = os.getenv("SF_SECURITY_TOKEN")
        
        if not all([self.username, self.password]):
            raise ValueError("SF_USERNAME and SF_PASSWORD must be set in .env file")
        
        # Optional credentials
        self.client_id = os.getenv("SF_CLIENT_ID")
        self.client_secret = os.getenv("SF_CLIENT_SECRET")
        self.domain = os.getenv("SF_DOMAIN", "login.salesforce.com")
        self.private_key_path = os.getenv("SF_PRIVATE_KEY_PATH")
        self.custom_domain = os.getenv("SF_CUSTOM_DOMAIN")
        
        # API server configuration
        self.api_server_url = os.getenv("API_SERVER_URL", "http://localhost:8000")
        self.api_auth_token = os.getenv("API_AUTH_TOKEN")
        
        # Agent configuration
        self.agent_name_prefix = os.getenv("DEFAULT_AGENT_NAME", "TestAgent")
        self.company_name = os.getenv("AGENT_COMPANY_NAME", "TestCompany")
        self.fixed_agent_name_for_export = os.getenv("FIXED_AGENT_NAME_FOR_EXPORT", "Order_Management_Agent")
        
        # Directories
        self.examples_dir = Path(__file__).parent.parent
        self.assets_dir = self.examples_dir / "assets"
        self.output_dir = Path(__file__).parent / os.getenv("OUTPUT_DIRECTORY", "test_results")
        self.template_dir = Path(os.getenv("TEMPLATE_DIRECTORY", self.assets_dir / "templates"))
        self.modular_agent_dir_relative = "assets/modular_agent_dir"
        
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Test results dictionary: {example_name: (status, message)} where status can be 'passed', 'failed', 'skipped'
        self.results: Dict[str, Tuple[str, Optional[str]]] = {}
        
        # Define fixed names/paths for dependent tests
        self.modular_agent_test_name = "create_agent_from_modular_directory.py"
        self.modular_agent_name_internal = "Order_Management_Agent"
        self.generator_test_name = "generate_prompt_template_example.py"
        self.deployer_test_name = "deploy_prompt_template_example.py"
        self.tuner_test_name = "tune_prompt_template_example.py"
        self.generated_template_filename = "Account_Health_Analysis_Template.promptTemplate"

    def generate_unique_agent_name(self, prefix: str = None) -> str:
        """Generate a unique agent name to avoid conflicts."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        prefix = prefix or self.agent_name_prefix
        # Ensure name is API compliant (no spaces, etc.)
        prefix_clean = prefix.replace(" ", "_")
        return f"{prefix_clean}_{timestamp}_{unique_id}"

    def import_example_module(self, example_path: Path) -> object:
        """Import an example module by path."""
        # Add parent directory to Python path temporarily
        parent_dir = str(self.examples_dir.parent)
        if parent_dir not in sys.path:
            sys.path.insert(0, parent_dir)
            
        try:
            spec = importlib.util.spec_from_file_location(
                example_path.stem, str(example_path)
            )
            if not spec or not spec.loader:
                raise ImportError(f"Could not load example: {example_path}")
                
            module = importlib.util.module_from_spec(spec)
            sys.modules[example_path.stem] = module
            spec.loader.exec_module(module)
            return module
        finally:
            if parent_dir in sys.path:
                sys.path.remove(parent_dir)

    def run_example(self, example_path: Path, args: List[str]) -> Tuple[bool, Optional[str]]:
        """Run a single example with the given arguments."""
        try:
            logger.info(f"\n{BOLD}========================================\n=== Running example: {example_path.name} ===\n========================================{RESET}")
            
            # Import and run the example
            module = self.import_example_module(example_path)
            
            # Patch sys.argv with the provided arguments
            original_argv = sys.argv
            sys.argv = [original_argv[0]] + args
            
            try:
                result = module.main()
                if result != 0 and result is not None:
                    raise RuntimeError(f"Example {example_path.name} failed with exit code {result}")
                return True, None
            except Exception as e:
                # Try to capture specific error types if needed
                return False, str(e)
            finally:
                sys.argv = original_argv
                
        except Exception as e:
            # Capture errors during import or setup
            return False, str(e)

    def run_tests(self) -> bool:
        """Run all integration tests."""
        # Create a timestamped directory for test results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_results_dir = self.output_dir / timestamp
        test_results_dir.mkdir(parents=True, exist_ok=True)

        examples_to_test = [
            # Basic agent creation examples
            (
                "create_agent_programmatically.py",
                lambda: [
                    "--username", self.username,
                    "--password", self.password,
                    "--security_token", self.security_token
                ]
            ),
            (
                "create_agent_from_description.py",
                lambda: [
                    "--username", self.username,
                    "--password", self.password,
                    "--output_dir", str(test_results_dir / "generated_agents" / "techmart_assistant")
                ]
            ),
            (
                "create_agent_from_json_file.py",
                lambda: [
                    "--username", self.username,
                    "--password", self.password,
                    "--json_file", str(self.assets_dir / "input.json")
                ]
            ),
            (
                self.modular_agent_test_name,
                lambda: [
                    "--username", self.username,
                    "--password", self.password,
                    "--agent_directory", str(self.examples_dir / self.modular_agent_dir_relative),
                    "--agent_name", self.modular_agent_name_internal
                ]
            ),
            (
                "create_agent_from_nested_directory.py",
                lambda: [
                    "--username", self.username,
                    "--password", self.password,
                    "--agent_directory", str(self.assets_dir / "nested_agent_dir"),
                    "--agent_name", "order_management_agent"
                ]
            ),
            
            # Advanced examples
            (
                "create_apex_class_example.py",
                lambda: [
                    "--username", self.username,
                    "--password", self.password,
                    "--output_dir", str(test_results_dir / "apex_classes")
                ]
            ),
            (
                self.deployer_test_name,
                lambda: [
                    "--username", self.username,
                    "--password", self.password,
                    "--security_token", self.security_token,
                    "--template_path", str(test_results_dir / self.generated_template_filename)
                ] if self.security_token else []
            ),
            (
                self.generator_test_name,
                lambda: [
                    "--username", self.username,
                    "--password", self.password,
                    "--output_dir", str(test_results_dir),
                    "--model", "gpt-4"
                ]
            ),
            (
                self.tuner_test_name,
                lambda: [
                    "--username", self.username,
                    "--password", self.password,
                    "--security_token", self.security_token,
                    "--template_path", str(test_results_dir / self.generated_template_filename),
                    "--output_dir", str(test_results_dir / "tuned_templates"),
                    "--model", "gpt-4"
                ] if self.security_token else []
            ),
            
            # Token flow examples
            (
                "deploy_agent_token_flow.py",
                lambda: [
                    "--domain", self.domain,
                    "--auth_type", "client-credentials",
                    "--client_id", self.client_id,
                    "--client_secret", self.client_secret,
                    "--custom_domain", self.custom_domain
                ] if all([self.client_id, self.client_secret]) else []
            ),
            
            # API server example
            (
                "api_server_example.py",
                lambda: [
                    "--username", self.username,
                    "--password", self.password,
                    "--server", self.api_server_url,
                    "--auth", self.api_auth_token
                ] if self.api_auth_token else []
            ),
            
            # Export example (DEPENDENT TEST)
            (
                "export_salesforce_agent_example.py",
                lambda: [
                    "--username", self.username,
                    "--password", self.password,
                    "--domain", self.domain,
                    "--agent_name", self.fixed_agent_name_for_export,
                    "--output_dir", str(test_results_dir / "exported_agents")
                ]
            ),
            
            # Run agent example
            (
                "run_agent.py",
                lambda: [
                    "--username", self.username,
                    "--password", self.password,
                    "--security_token", self.security_token
                ]
            )
        ]
        
        for example_name, get_args in examples_to_test:
            example_path = self.examples_dir / example_name
            skip_reason = None

            if not example_path.exists():
                logger.warning(f"{YELLOW}Skipping {example_name} - file not found{RESET}")
                self.results[example_name] = ('skipped', 'File not found')
                continue

            # === Dependency Checks ===
            # Export depends on Modular Agent creation
            if example_name == "export_salesforce_agent_example.py":
                dependency_status, _ = self.results.get(self.modular_agent_test_name, ('failed', 'Dependency not run yet'))
                if dependency_status != 'passed':
                    skip_reason = f"Skipped due to failure in dependency: {self.modular_agent_test_name}"
                    logger.warning(f"{YELLOW}{skip_reason}{RESET}")
                    self.results[example_name] = ('skipped', skip_reason)
                    continue

            # Deployer and Tuner depend on Generator
            if example_name == self.deployer_test_name or example_name == self.tuner_test_name:
                dependency_status, _ = self.results.get(self.generator_test_name, ('failed', 'Dependency not run yet'))
                if dependency_status != 'passed':
                    skip_reason = f"Skipped due to failure/skip in dependency: {self.generator_test_name}"
                    logger.warning(f"{YELLOW}{skip_reason}{RESET}")
                    self.results[example_name] = ('skipped', skip_reason)
                    continue
                # Check if the generated file actually exists (optional but good practice)
                expected_template_path = test_results_dir / self.generated_template_filename
                if not expected_template_path.exists():
                    skip_reason = f"Skipped because expected template file was not found: {expected_template_path}"
                    logger.warning(f"{YELLOW}{skip_reason}{RESET}")
                    self.results[example_name] = ('skipped', skip_reason)
                    continue
            # === End Dependency Checks ===

            args = get_args()
            # Recalculate args for deployer/tuner here to ensure correct path after checks
            if example_name == self.deployer_test_name and self.security_token:
                 args = [
                     "--username", self.username,
                     "--password", self.password,
                     "--security_token", self.security_token,
                     "--template_path", str(test_results_dir / self.generated_template_filename)
                 ]
            elif example_name == self.tuner_test_name and self.security_token:
                 args = [
                     "--username", self.username,
                     "--password", self.password,
                     "--security_token", self.security_token,
                     "--template_path", str(test_results_dir / self.generated_template_filename),
                     "--output_dir", str(test_results_dir / "tuned_templates"),
                     "--model", "gpt-4"
                 ]

            if not args:
                skip_reason = "Missing required credentials/arguments for this test"
                logger.warning(f"{YELLOW}Skipping {example_name} - {skip_reason}{RESET}")
                self.results[example_name] = ('skipped', skip_reason)
                continue

            if skip_reason:
                self.results[example_name] = ('skipped', skip_reason)
                continue

            success, error = self.run_example(example_path, args)

            if success:
                self.results[example_name] = ('passed', None)
                logger.info(f"{GREEN}✓ {example_name} passed{RESET}")
            else:
                self.results[example_name] = ('failed', error)
                logger.error(f"{RED}✗ {example_name} failed: {error}{RESET}")
        
        # Print summary
        total = len(self.results)
        passed = sum(1 for status, _ in self.results.values() if status == 'passed')
        failed = sum(1 for status, _ in self.results.values() if status == 'failed')
        skipped = sum(1 for status, _ in self.results.values() if status == 'skipped')
        
        print(f"\n{BOLD}========================================\n=== Test Summary ===\n========================================{RESET}")
        print(f"Total tests defined: {len(examples_to_test)}")
        print(f"Total tests run: {total}")
        print(f"{GREEN}Passed: {passed}{RESET}")
        print(f"{RED}Failed: {failed}{RESET}")
        print(f"{BLUE}Skipped: {skipped}{RESET}")
        
        if passed > 0:
            print(f"\n{BOLD}========================================\n=== Successful tests: ===\n========================================{RESET}")
            successful_tests = [name for name, (status, _) in self.results.items() if status == 'passed']
            for test in successful_tests:
                print(f"{GREEN}{test}{RESET}")
        
        if failed > 0:
            print(f"\n{BOLD}========================================\n=== Failed tests: ===\n========================================{RESET}")
            failed_tests_data = [
                (name, textwrap.fill(message or "Unknown error", width=80))
                for name, (status, message) in self.results.items() if status == 'failed'
            ]
            print(tabulate(failed_tests_data, headers=["Test Name", "Error"], tablefmt="fancy_grid", stralign="left"))
        
        if skipped > 0:
            print(f"\n{BOLD}========================================\n=== Skipped tests: ===\n========================================{RESET}")
            skipped_tests_data = [
                (name, textwrap.fill(message or "No reason provided", width=80))
                for name, (status, message) in self.results.items() if status == 'skipped'
            ]
            print(tabulate(skipped_tests_data, headers=["Test Name", "Reason"], tablefmt="fancy_grid", stralign="left"))
        
        return failed == 0

def main():
    try:
        runner = IntegrationTests()
        success = runner.run_tests()
        sys.exit(0 if success else 1)
    except Exception as e:
        logger.error(f"{RED}Error during test execution: {str(e)}{RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()