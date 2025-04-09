#!/usr/bin/env python3
"""Integration tests for AgentForce SDK examples using pytest."""

import os
import sys
import uuid
import logging
import importlib.util
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime
import pytest
from dotenv import load_dotenv

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

# Test configuration and fixtures
@pytest.fixture(scope="session")
def test_config():
    """Initialize test configuration from environment variables."""
    # Load environment variables
    env_path = Path(__file__).parent / ".env"
    load_dotenv(env_path)
    
    return {
        # Required credentials
        "username": os.getenv("SF_USERNAME"),
        "password": os.getenv("SF_PASSWORD"),
        "security_token": os.getenv("SF_SECURITY_TOKEN"),
        
        # Optional credentials
        "client_id": os.getenv("SF_CLIENT_ID"),
        "client_secret": os.getenv("SF_CLIENT_SECRET"),
        "domain": os.getenv("SF_DOMAIN", "login.salesforce.com"),
        "private_key_path": os.getenv("SF_PRIVATE_KEY_PATH"),
        "custom_domain": os.getenv("SF_CUSTOM_DOMAIN"),
        
        # API server configuration
        "api_server_url": os.getenv("API_SERVER_URL", "http://localhost:8000"),
        "api_auth_token": os.getenv("API_AUTH_TOKEN"),
        
        # Agent configuration
        "agent_name_prefix": os.getenv("DEFAULT_AGENT_NAME", "TestAgent"),
        "company_name": os.getenv("AGENT_COMPANY_NAME", "TestCompany"),
        "fixed_agent_name_for_export": os.getenv("FIXED_AGENT_NAME_FOR_EXPORT", "Order_Management_Agent"),
    }

@pytest.fixture(scope="session")
def test_paths():
    """Initialize test paths."""
    examples_dir = Path(__file__).parent.parent
    return {
        "examples_dir": examples_dir,
        "assets_dir": examples_dir / "assets",
        "output_dir": Path(__file__).parent / os.getenv("OUTPUT_DIRECTORY", "test_results"),
        "template_dir": examples_dir / "assets" / "templates",
        "modular_agent_dir": examples_dir / "assets" / "modular_agent_dir",
    }

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment(test_paths):
    """Set up test environment before running tests."""
    # Create output directory
    test_paths["output_dir"].mkdir(parents=True, exist_ok=True)
    
    # Create timestamped directory for this test run
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    test_results_dir = test_paths["output_dir"] / timestamp
    test_results_dir.mkdir(parents=True, exist_ok=True)
    
    # Add to test paths
    test_paths["results_dir"] = test_results_dir
    
    # Add parent directory to Python path temporarily
    parent_dir = str(test_paths["examples_dir"].parent)
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    
    yield
    
    # Cleanup if needed
    if parent_dir in sys.path:
        sys.path.remove(parent_dir)

def import_example_module(example_path: Path) -> object:
    """Import an example module by path."""
    spec = importlib.util.spec_from_file_location(
        example_path.stem, str(example_path)
    )
    if not spec or not spec.loader:
        raise ImportError(f"Could not load example: {example_path}")
        
    module = importlib.util.module_from_spec(spec)
    sys.modules[example_path.stem] = module
    spec.loader.exec_module(module)
    return module

def generate_unique_agent_name(prefix: str) -> str:
    """Generate a unique agent name to avoid conflicts."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    prefix_clean = prefix.replace(" ", "_")
    return f"{prefix_clean}_{timestamp}_{unique_id}"

# Basic agent creation tests
@pytest.mark.dependency()
def test_create_agent_programmatically(test_config, test_paths):
    """Test creating an agent programmatically."""
    example_path = test_paths["examples_dir"] / "create_agent_programmatically.py"
    module = import_example_module(example_path)
    
    args = [
        "--username", test_config["username"],
        "--password", test_config["password"],
        "--security_token", test_config["security_token"]
    ]
    
    # Save original argv and patch with our args
    original_argv = sys.argv
    sys.argv = [original_argv[0]] + args
    
    try:
        result = module.main()
        assert result == 0 or result is None, "Example failed"
    finally:
        sys.argv = original_argv

@pytest.mark.dependency()
def test_create_agent_from_description(test_config, test_paths):
    """Test creating an agent from description."""
    example_path = test_paths["examples_dir"] / "create_agent_from_description.py"
    module = import_example_module(example_path)
    
    output_dir = test_paths["results_dir"] / "generated_agents" / "techmart_assistant"
    args = [
        "--username", test_config["username"],
        "--password", test_config["password"],
        "--output_dir", str(output_dir)
    ]
    
    original_argv = sys.argv
    sys.argv = [original_argv[0]] + args
    
    try:
        result = module.main()
        assert result == 0 or result is None, "Example failed"
    finally:
        sys.argv = original_argv

@pytest.mark.dependency()
def test_create_agent_from_json_file(test_config, test_paths):
    """Test creating an agent from JSON file."""
    example_path = test_paths["examples_dir"] / "create_agent_from_json_file.py"
    module = import_example_module(example_path)
    
    args = [
        "--username", test_config["username"],
        "--password", test_config["password"],
        "--json_file", str(test_paths["assets_dir"] / "input.json")
    ]
    
    original_argv = sys.argv
    sys.argv = [original_argv[0]] + args
    
    try:
        result = module.main()
        assert result == 0 or result is None, "Example failed"
    finally:
        sys.argv = original_argv

@pytest.mark.dependency()
def test_create_agent_from_modular_directory(test_config, test_paths):
    """Test creating an agent from modular directory."""
    example_path = test_paths["examples_dir"] / "create_agent_from_modular_directory.py"
    module = import_example_module(example_path)
    
    args = [
        "--username", test_config["username"],
        "--password", test_config["password"],
        "--agent_directory", str(test_paths["modular_agent_dir"]),
        "--agent_name", "Order_Management_Agent"
    ]
    
    original_argv = sys.argv
    sys.argv = [original_argv[0]] + args
    
    try:
        result = module.main()
        assert result == 0 or result is None, "Example failed"
    finally:
        sys.argv = original_argv

@pytest.mark.dependency()
def test_create_agent_from_nested_directory(test_config, test_paths):
    """Test creating an agent from nested directory."""
    example_path = test_paths["examples_dir"] / "create_agent_from_nested_directory.py"
    module = import_example_module(example_path)
    
    args = [
        "--username", test_config["username"],
        "--password", test_config["password"],
        "--agent_directory", str(test_paths["assets_dir"] / "nested_agent_dir"),
        "--agent_name", "order_management_agent"
    ]
    
    original_argv = sys.argv
    sys.argv = [original_argv[0]] + args
    
    try:
        result = module.main()
        assert result == 0 or result is None, "Example failed"
    finally:
        sys.argv = original_argv

# Advanced examples
@pytest.mark.dependency()
def test_create_apex_class(test_config, test_paths):
    """Test creating Apex class example."""
    example_path = test_paths["examples_dir"] / "create_apex_class_example.py"
    module = import_example_module(example_path)
    
    args = [
        "--username", test_config["username"],
        "--password", test_config["password"],
        "--output_dir", str(test_paths["results_dir"] / "apex_classes")
    ]
    
    original_argv = sys.argv
    sys.argv = [original_argv[0]] + args
    
    try:
        result = module.main()
        assert result == 0 or result is None, "Example failed"
    finally:
        sys.argv = original_argv

@pytest.mark.dependency()
def test_generate_prompt_template(test_config, test_paths):
    """Test generating prompt template."""
    example_path = test_paths["examples_dir"] / "generate_prompt_template_example.py"
    module = import_example_module(example_path)
    
    args = [
        "--username", test_config["username"],
        "--password", test_config["password"],
        "--output_dir", str(test_paths["results_dir"]),
        "--model", "gpt-4"
    ]
    
    original_argv = sys.argv
    sys.argv = [original_argv[0]] + args
    
    try:
        result = module.main()
        assert result == 0 or result is None, "Example failed"
    finally:
        sys.argv = original_argv

@pytest.mark.dependency(depends=["test_generate_prompt_template"])
def test_deploy_prompt_template(test_config, test_paths):
    """Test deploying prompt template."""
    if not test_config["security_token"]:
        pytest.skip("Security token not provided")
        
    template_path = test_paths["results_dir"] / "Account_Health_Analysis_Template.promptTemplate"
    if not template_path.exists():
        pytest.skip("Template file not found")
        
    example_path = test_paths["examples_dir"] / "deploy_prompt_template_example.py"
    module = import_example_module(example_path)
    
    args = [
        "--username", test_config["username"],
        "--password", test_config["password"],
        "--security_token", test_config["security_token"],
        "--template_path", str(template_path)
    ]
    
    original_argv = sys.argv
    sys.argv = [original_argv[0]] + args
    
    try:
        result = module.main()
        assert result == 0 or result is None, "Example failed"
    finally:
        sys.argv = original_argv

@pytest.mark.dependency(depends=["test_generate_prompt_template"])
def test_tune_prompt_template(test_config, test_paths):
    """Test tuning prompt template."""
    if not test_config["security_token"]:
        pytest.skip("Security token not provided")
        
    template_path = test_paths["results_dir"] / "Account_Health_Analysis_Template.promptTemplate"
    if not template_path.exists():
        pytest.skip("Template file not found")
        
    example_path = test_paths["examples_dir"] / "tune_prompt_template_example.py"
    module = import_example_module(example_path)
    
    args = [
        "--username", test_config["username"],
        "--password", test_config["password"],
        "--security_token", test_config["security_token"],
        "--template_path", str(template_path),
        "--output_dir", str(test_paths["results_dir"] / "tuned_templates"),
        "--model", "gpt-4"
    ]
    
    original_argv = sys.argv
    sys.argv = [original_argv[0]] + args
    
    try:
        result = module.main()
        assert result == 0 or result is None, "Example failed"
    finally:
        sys.argv = original_argv

# Token flow examples
@pytest.mark.skipif(
    not (os.getenv("SF_CLIENT_ID") and os.getenv("SF_CLIENT_SECRET")),
    reason="Client credentials not provided"
)
def test_deploy_agent_token_flow(test_config, test_paths):
    """Test deploying agent with token flow."""
    example_path = test_paths["examples_dir"] / "deploy_agent_token_flow.py"
    module = import_example_module(example_path)
    
    args = [
        "--domain", test_config["domain"],
        "--auth_type", "client-credentials",
        "--client_id", test_config["client_id"],
        "--client_secret", test_config["client_secret"],
        "--custom_domain", test_config["custom_domain"]
    ]
    
    original_argv = sys.argv
    sys.argv = [original_argv[0]] + args
    
    try:
        result = module.main()
        assert result == 0 or result is None, "Example failed"
    finally:
        sys.argv = original_argv

# API server example
@pytest.mark.skipif(
    not os.getenv("API_AUTH_TOKEN"),
    reason="API auth token not provided"
)
def test_api_server(test_config, test_paths):
    """Test API server example."""
    example_path = test_paths["examples_dir"] / "api_server_example.py"
    module = import_example_module(example_path)
    
    args = [
        "--username", test_config["username"],
        "--password", test_config["password"],
        "--server", test_config["api_server_url"],
        "--auth", test_config["api_auth_token"]
    ]
    
    original_argv = sys.argv
    sys.argv = [original_argv[0]] + args
    
    try:
        result = module.main()
        assert result == 0 or result is None, "Example failed"
    finally:
        sys.argv = original_argv

@pytest.mark.dependency(depends=["test_create_agent_from_modular_directory"])
def test_export_salesforce_agent(test_config, test_paths):
    """Test exporting Salesforce agent."""
    example_path = test_paths["examples_dir"] / "export_salesforce_agent_example.py"
    module = import_example_module(example_path)
    
    args = [
        "--username", test_config["username"],
        "--password", test_config["password"],
        "--domain", test_config["domain"],
        "--agent_name", test_config["fixed_agent_name_for_export"],
        "--output_dir", str(test_paths["results_dir"] / "exported_agents")
    ]
    
    original_argv = sys.argv
    sys.argv = [original_argv[0]] + args
    
    try:
        result = module.main()
        assert result == 0 or result is None, "Example failed"
    finally:
        sys.argv = original_argv

def test_run_agent(test_config, test_paths):
    """Test running an agent."""
    if not test_config["security_token"]:
        pytest.skip("Security token not provided")
        
    example_path = test_paths["examples_dir"] / "run_agent.py"
    module = import_example_module(example_path)
    
    args = [
        "--username", test_config["username"],
        "--password", test_config["password"],
        "--security_token", test_config["security_token"]
    ]
    
    original_argv = sys.argv
    sys.argv = [original_argv[0]] + args
    
    try:
        result = module.main()
        assert result == 0 or result is None, "Example failed"
    finally:
        sys.argv = original_argv