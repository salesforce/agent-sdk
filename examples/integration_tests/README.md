# Integration Tests

This directory contains integration tests for the AgentForce SDK examples. The tests run in an isolated Docker environment to ensure consistency and reproducibility.

## Prerequisites

- Docker installed and running (only if using Docker method)
- Python 3.11 or higher
- Access to a Salesforce org with appropriate credentials
- Bash shell (for Unix/Linux/macOS) or Git Bash (for Windows)

## Quick Start

1. Copy the environment file template:
```bash
cp .env.example .env
```

2. Edit `.env` with your Salesforce credentials:
```bash
vim .env
# or use any text editor to modify the file with your credentials:
# SF_USERNAME=your.email@example.com
# SF_PASSWORD=your_password
```

3. Run the tests (choose one method):
```bash
# Using Docker (recommended)
./run_test.sh

# Direct Python execution (without Docker)
python -u examples/integration_tests/run_tests_custom.py  # for custom tests
pytest -v -s examples/integration_tests/run_tests_pytest.py  # for pytest
```

## Running Options

### 1. Docker Method (Recommended)

The test script supports several running modes and test types:

#### Custom Tests (Default)
Uses our custom testing framework:
```bash
./run_test.sh --test-type custom
```

#### Pytest
Uses pytest framework with more detailed reporting:
```bash
./run_test.sh --test-type pytest
```

#### Running Specific Tests
Run a specific test by name:
```bash
# For custom tests
./run_test.sh --test create_agent_programmatically

# For pytest
./run_test.sh --test-type pytest --test create_agent_programmatically
```

### 2. Build Options

#### Build and Run (Default)
Builds a fresh Docker image and runs the tests:
```bash
./run_test.sh
# or explicitly with test type
./run_test.sh --build --test-type custom
./run_test.sh --build --test-type pytest
```

#### Run Existing Image
Uses an existing Docker image without rebuilding:
```bash
./run_test.sh --no-build
# or with specific test type
./run_test.sh --no-build --test-type custom
./run_test.sh --no-build --test-type pytest
```

### 3. Using Environment Variables Directly
You can also pass credentials directly without using an `.env` file:
```bash
SF_USERNAME=your.email@example.com SF_PASSWORD=your_password ./run_test.sh --test-type pytest
```

### 2. Direct Python Execution

You can run the tests directly without Docker if you have Python installed locally.

#### Setup
1. Install required dependencies:
```bash
pip install -e ".[all]"
```

2. Set up environment variables:

You can create a `.env` file in the `examples/integration_tests` directory from .env.example

#### Running Custom Tests
```bash
# Basic run
python -u examples/integration_tests/run_tests_custom.py

# Run specific test
python -u examples/integration_tests/run_tests_custom.py --test create_agent_programmatically
```

#### Running Pytest Tests
```bash
# Basic run
pytest -v -s examples/integration_tests/run_tests_pytest.py

# With more detailed output
pytest -v -s --tb=long --showlocals examples/integration_tests/run_tests_pytest.py

# Run specific test
pytest -v -s examples/integration_tests/run_tests_pytest.py -k "test_create_agent_programmatically"

```

## Directory Structure

- `.env.example` - Template for environment variables
- `.env` - Your local environment variables (git-ignored)
- `run_test.sh` - Main script to run the tests with Docker
- `run_tests_custom.py` - Custom test implementation
- `run_tests_pytest.py` - Pytest test implementation
- `Dockerfile` - Defines the Docker test environment (only needed for Docker method)

## Test Environment

When running with Docker:
- Python 3.11
- All required dependencies installed
- Isolated environment for reproducibility
- Real-time test output to terminal

When running directly:
- Uses your local Python installation
- Requires manual dependency installation
- Faster execution (no Docker overhead)
- Better for debugging and development
