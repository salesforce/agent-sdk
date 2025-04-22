from . import server
import sys

def main():
    """Main entry point for the package."""
    # This will let Click handle the command-line arguments
    server.main(standalone_mode=False)

# Optionally expose other important items at package level
__all__ = ['main', 'server']