#!/usr/bin/env python3
"""
MCP Server Example
------------------
This example demonstrates how to use the AgentForce SDK REST API Server to create and interact with agents.
"""

import os
import sys
import json
import requests
import time
import argparse
from typing import Dict, Any, List, Optional
from http.server import HTTPServer

# Add parent directory to Python path so we can import agent_sdk directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent_sdk import Agentforce
from agent_sdk.core.auth import BasicAuth
from agent_sdk.server import AgentforceServer

# Define server URL
SERVER_URL = "http://localhost:8000"

class AgentforceClient:
    """
    A client for interacting with the AgentForce MCP Server.
    """
    
    def __init__(self, base_url: str = SERVER_URL, auth_token: Optional[str] = None):
        """
        Initialize the client.
        
        Args:
            base_url: The base URL of the MCP server
            auth_token: Optional authentication token
        """
        self.base_url = base_url
        self.auth_token = auth_token
        self.client_id = None
        
        # Set up headers
        self.headers = {"Content-Type": "application/json"}
        if auth_token:
            self.headers["Authorization"] = f"Bearer {auth_token}"
    
    def _make_request(self, method: str, path: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Make a request to the MCP server.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            path: The path on the server
            data: Optional data to send with the request
        
        Returns:
            The JSON response from the server
        """
        url = f"{self.base_url}{path}"
        
        # Add client_id to requests if available
        if data is None:
            data = {}
        
        if self.client_id:
            data["client_id"] = self.client_id
        
        # Make the request
        response = requests.request(
            method=method,
            url=url,
            headers=self.headers,
            json=data
        )
        
        # Parse the response
        if response.status_code >= 400:
            error_data = response.json() if response.text else {"error": "Unknown error"}
            raise Exception(f"Error {response.status_code}: {error_data.get('error', 'Unknown error')}")
        
        result = response.json()
        
        # Store client_id if provided
        if "client_id" in result:
            self.client_id = result["client_id"]
        
        return result
    
    def create_session(self, username: str, password: str, security_token: str = "") -> str:
        """
        Create a new session with the server.
        
        Args:
            username: Salesforce username
            password: Salesforce password
            security_token: Optional Salesforce security token
        
        Returns:
            The client_id for the session
        """
        result = self._make_request("POST", "/create", {
            "username": username,
            "password": password,
            "security_token": security_token,
            "name": "Example Agent",  # Include minimal agent data
            "description": "An example agent"
        })
        
        return self.client_id
    
    def create_agent(self, agent_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new agent.
        
        Args:
            agent_data: The agent data
        
        Returns:
            The result from the server
        """
        result = self._make_request("POST", "/create", agent_data)
        return result.get("result", {})
    
    def retrieve_agent(self, agent_id: str) -> Dict[str, Any]:
        """
        Retrieve an agent.
        
        Args:
            agent_id: The ID of the agent to retrieve
        
        Returns:
            The agent data
        """
        result = self._make_request("POST", "/retrieve", {"agent_id": agent_id})
        return result.get("agent", {})
    
    def update_agent(self, agent_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an agent.
        
        Args:
            agent_data: The updated agent data
        
        Returns:
            The result from the server
        """
        result = self._make_request("POST", "/update", agent_data)
        return result.get("result", {})
    
    def delete_agent(self, agent_id: str) -> Dict[str, Any]:
        """
        Delete an agent.
        
        Args:
            agent_id: The ID of the agent to delete
        
        Returns:
            The result from the server
        """
        result = self._make_request("POST", "/delete", {"agent_id": agent_id})
        return result.get("result", {})
    
    def run_agent(self, agent_id: str, input_text: str) -> Dict[str, Any]:
        """
        Run an agent.
        
        Args:
            agent_id: The ID of the agent to run
            input_text: The input text to send to the agent
        
        Returns:
            The result from the server
        """
        result = self._make_request("POST", "/run", {
            "agent_id": agent_id,
            "input_text": input_text
        })
        return result.get("result", {})
    
    def export_agent(self, agent_id: str, export_path: str) -> Dict[str, Any]:
        """
        Export an agent.
        
        Args:
            agent_id: The ID of the agent to export
            export_path: The path to export the agent to
        
        Returns:
            The result from the server
        """
        result = self._make_request("POST", "/export", {
            "agent_id": agent_id,
            "export_path": export_path
        })
        return result.get("result", {})
    
    def import_agent(self, agent_path: str) -> Dict[str, Any]:
        """
        Import an agent.
        
        Args:
            agent_path: The path to import the agent from
        
        Returns:
            The result from the server
        """
        result = self._make_request("POST", "/import", {"agent_path": agent_path})
        return result.get("result", {})
    
    def retrieve_metadata(self, metadata_type: str, agent_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Retrieve metadata.
        
        Args:
            metadata_type: The type of metadata to retrieve
            agent_name: Optional agent name
        
        Returns:
            The result from the server
        """
        data = {"metadata_type": metadata_type}
        if agent_name:
            data["agent_name"] = agent_name
        
        result = self._make_request("POST", "/retrieve_metadata", data)
        return result.get("result", {})

def create_simple_agent(client: AgentforceClient) -> str:
    """
    Create a simple agent using the client.
    
    Args:
        client: The AgentforceClient instance
    
    Returns:
        The ID of the created agent
    """
    agent_data = {
        "name": "Hello World Agent",
        "description": "A simple agent that says hello",
        "agent_type": "External",
        "agent_template_type": "Einstein",
        "company_name": "Salesforce",
        "topics": [
            {
                "name": "Greetings",
                "description": "Handle greetings",
                "scope": "Handle greeting requests",
                "actions": [
                    {
                        "name": "SayHello",
                        "description": "Say hello to the user",
                        "inputs": [
                            {
                                "name": "name",
                                "description": "Name of the person to greet",
                                "data_type": "String",
                                "required": True
                            }
                        ],
                        "example_output": {
                            "status": "success",
                            "details": {"message": "Hello, World!"}
                        }
                    }
                ]
            }
        ]
    }
    
    result = client.create_agent(agent_data)
    agent_id = result.get("id")
    
    if not agent_id:
        raise Exception("Failed to create agent")
    
    print(f"Created agent with ID: {agent_id}")
    return agent_id

def main():
    """Main entry point for the example."""
    parser = argparse.ArgumentParser(description="AgentForce SDK REST API Server Example")
    parser.add_argument("--username", help="Salesforce username")
    parser.add_argument("--password", help="Salesforce password")
    parser.add_argument("--token", help="Salesforce security token")
    parser.add_argument("--server", default=SERVER_URL, help="API server URL")
    parser.add_argument("--auth", help="API server authentication token")
    
    args = parser.parse_args()
    
    # Create a client
    client = AgentforceClient(args.server, args.auth)
    
    # Create a session
    if args.username and args.password:
        print("Creating session...")
        client.create_session(args.username, args.password, args.token or "")
    else:
        print("No credentials provided. Some operations may fail.")
    
    try:
        # Create a simple agent
        agent_id = create_simple_agent(client)
        
        # Retrieve the agent
        print(f"Retrieving agent {agent_id}...")
        agent = client.retrieve_agent(agent_id)
        print(f"Retrieved agent: {agent['name']}")
        
        # Run the agent
        print(f"Running agent {agent_id}...")
        result = client.run_agent(agent_id, "Hello, AgentForce!")
        print(f"Agent response: {result}")
        
        # Delete the agent
        print(f"Deleting agent {agent_id}...")
        client.delete_agent(agent_id)
        print(f"Deleted agent {agent_id}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 