#!/bin/bash

# Function to show usage
show_usage() {
    echo "Usage:"
    echo "  Build and run: $0 [--build] [--test-type <type>] [--test <test_name>]"
    echo "  Run existing: $0 --no-build [--test-type <type>] [--test <test_name>]"
    echo ""
    echo "Options:"
    echo "  --test-type    Type of tests to run (custom|pytest). Default: custom"
    echo "  --test         Run a specific test by name"
    echo ""
    echo "Environment variables should be set in .env file"
    echo "Required variables:"
    echo "  SF_USERNAME - Salesforce username"
    echo "  SF_PASSWORD - Salesforce password"
    echo ""
    echo "Optional variables (see .env.example for full list):"
    echo "  SF_SECURITY_TOKEN - Salesforce security token"
    echo "  SF_CLIENT_ID - OAuth2 client ID"
    echo "  SF_CLIENT_SECRET - OAuth2 client secret"
    echo "  SF_DOMAIN - Salesforce domain"
}

# Function to load .env file if it exists
load_env() {
    ENV_FILE="$1"
    if [ -f "$ENV_FILE" ]; then
        echo "Loading environment from $ENV_FILE"
        export $(cat "$ENV_FILE" | grep -v '^#' | xargs)
    fi
}

# Get the root directory of the project
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
ENV_FILE="$ROOT_DIR/examples/integration_tests/.env"

# Load .env file if it exists
load_env "$ENV_FILE"

# Default values
BUILD=true
TEST_TYPE="custom"
SPECIFIC_TEST=""

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --no-build)
            BUILD=false
            shift
            ;;
        --build)
            BUILD=true
            shift
            ;;
        --test-type)
            if [ -z "$2" ] || [[ ! "$2" =~ ^(custom|pytest)$ ]]; then
                echo "Error: --test-type must be either 'custom' or 'pytest'"
                exit 1
            fi
            TEST_TYPE="$2"
            shift 2
            ;;
        --test)
            if [ -z "$2" ]; then
                echo "Error: --test requires a test name"
                exit 1
            fi
            SPECIFIC_TEST="$2"
            shift 2
            ;;
        -h|--help)
            show_usage
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

# Check if required environment variables are set
if [ -z "$SF_USERNAME" ] || [ -z "$SF_PASSWORD" ]; then
    echo "Error: Required environment variables not set"
    echo "Please create a .env file from .env.example with the required variables"
    exit 1
fi

# Echo some debug information
echo "Running from directory: $ROOT_DIR"
echo "Test type: $TEST_TYPE"
if [ -n "$SPECIFIC_TEST" ]; then
    echo "Running specific test: $SPECIFIC_TEST"
fi

cd "$ROOT_DIR"

# Build the image if requested
if [ "$BUILD" = true ]; then
    echo "Building Docker image..."

    # Clean up any previous builds if they exist
    docker rmi salesforce-agent-tests 2>/dev/null || true

    # Build with no cache to ensure fresh dependencies
    docker build --progress=plain \
        -t salesforce-agent-tests \
        -f examples/integration_tests/Dockerfile .

    # Check if build was successful
    if [ $? -ne 0 ]; then
        echo "Error: Docker build failed"
        exit 1
    fi
else
    echo "Skipping build, using existing Docker image..."

    # Check if the image exists
    if ! docker image inspect salesforce-agent-tests >/dev/null 2>&1; then
        echo "Error: Docker image 'salesforce-agent-tests' not found"
        echo "Please run with --build first or ensure the image exists"
        exit 1
    fi
fi

echo "Running integration tests..."

# Choose the test command based on TEST_TYPE
if [ "$TEST_TYPE" = "pytest" ]; then
    TEST_COMMAND="pytest -v -s examples/integration_tests/run_tests_pytest.py"
    # Add specific test if provided
    if [ -n "$SPECIFIC_TEST" ]; then
        TEST_COMMAND="$TEST_COMMAND -k $SPECIFIC_TEST"
    fi
else
    TEST_COMMAND="python -u examples/integration_tests/run_tests_custom.py"
    # Add specific test if provided
    if [ -n "$SPECIFIC_TEST" ]; then
        TEST_COMMAND="$TEST_COMMAND --test $SPECIFIC_TEST"
    fi
fi

# Run the tests with interactive terminal and remove container after completion
docker run --rm -it \
    --env-file "$ENV_FILE" \
    -e PYTHONUNBUFFERED=1 \
    -v "$ROOT_DIR/examples/assets:/app/examples/assets:ro" \
    -v "$ROOT_DIR/examples/test_results:/app/examples/test_results" \
    salesforce-agent-tests \
    $TEST_COMMAND

# Capture the exit code
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "Integration tests completed successfully"
else
    echo "Integration tests failed with exit code: $EXIT_CODE"
fi

# Exit with the same code as the tests
exit $EXIT_CODE
