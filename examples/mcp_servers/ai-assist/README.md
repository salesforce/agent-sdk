# ai-assist MCP Server

The `ai-assist` MCP server is designed to facilitate the creation and deployment of Agentforce. It interacts with users to gather requirements and generates agent metadata, which can then be deployed to a Salesforce organization.

## Usage Examples

When using the `ai-assist` server in Claude, you can:

- **Create an Agent**: The server will guide you through a series of questions to understand your needs, such as:
  - "What business problem are you trying to solve with this AI agent?"
  - "What would make this AI agent successful for you?"
  - "What is the name of the company you work for?"
  - "What would you like to name this agent?"

- **Generate and Deploy Agent Metadata**: After gathering the necessary information, the server generates the agent metadata and deploys it to your Salesforce organization.

## Quickstart

### Install

### Configuration Options

To deploy an agent, you need to configure the server with your Salesforce credentials. There are two transport methods available: STDIO and SSE.

#### Using STDIO Transport

STDIO runs on your local machine and is managed automatically by the MCP client. Use the following configuration template in your MCP configuration file, replacing placeholders with your actual credentials:

```json
"ai-assist": {
    "command": "uv",
    "args": [
        "--directory",
        "<github_repo_path>/agent_sdk/examples/mcp_servers/ai-assist",
        "run",
        "ai-assist"
    ],
    "env": {
        "SALESFORCE_USERNAME": "your_username",
        "SALESFORCE_PASSWORD": "your_password"
    }
}
```

#### Using SSE Transport

Server-Sent Events (SSE) transport can run locally or remotely and communicates over the network. This method is useful for viewing logs and sharing the server across machines.

1. Run the server with SSE transport:

```bash
SALESFORCE_USERNAME=your_username SALESFORCE_PASSWORD=your_password uv run ai-assist --transport sse
```

2. Alternatively, you can load environment variables from a `.env` file and then run:

```bash
uv run ai-assist --transport sse
```

3. You can specify a custom port (default is 8000):

```bash
uv run ai-assist --transport sse --port 8080
```

4. Add the following to your MCP configuration file:

```json
"ai-assist": {
    "url": "http://0.0.0.0:8000/sse"
}
```

Make sure the port in the URL matches the port you specified when starting the server.

#### Running in Claude Desktop

To set up the ai-assist MCP server in Claude Desktop, you need to add it to Claude's configuration file:

- On MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`
- On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

You can access this file by:
1. Open the Claude menu on your computer and select "Settings..."
2. Click on "Developer" in the left-hand bar
3. Click on "Edit Config"

You can use either STDIO or SSE transport when configuring the server:

**Using STDIO Transport (Runs Locally):**

```json
{
  "mcpServers": {
    "ai-assist": {
      "command": "uv",
      "args": [
        "--directory",
        "<github_repo_path>/agent_sdk/examples/mcp_servers/ai-assist",
        "run",
        "ai-assist"
      ],
      "env": {
        "SALESFORCE_USERNAME": "your_username",
        "SALESFORCE_PASSWORD": "your_password"
      }
    }
  }
}
```

**Using SSE Transport (Can Run Locally or Remotely):**

1. Start the server with SSE transport:
```bash
SALESFORCE_USERNAME=your_username SALESFORCE_PASSWORD=your_password uv run ai-assist --transport sse
```

2. Add this to your Claude Desktop configuration:
```json
{
  "mcpServers": {
    "ai-assist": {
      "url": "http://0.0.0.0:8000/sse"
    }
  }
}
```

3. After updating the configuration, restart Claude Desktop completely.

For more detailed instructions on setting up MCP servers in Claude Desktop, refer to the [official MCP documentation](https://modelcontextprotocol.io/quickstart/user).

### Running in Cursor

In Cursor the MCP server is experiencing some issues using STDIO, so it's recommended to use the SSE transport method instead. For detailed instructions on setting up MCP in Cursor, refer to the [Cursor MCP documentation](https://docs.cursor.com/context/model-context-protocol).

1. Run the server first using the SSE transport method as described in the section above.

2. Add the MCP configuration to Cursor's configuration file:
```json
"mcp-test": {
    "url": "http://0.0.0.0:8000/sse"
}
```

3. Make sure to use the correct port in the URL that matches your server configuration.

### Debugging

For debugging, use the [MCP Inspector](https://github.com/modelcontextprotocol/inspector) to visualize and troubleshoot the server's operations. Launch it with:

```bash
npx @modelcontextprotocol/inspector uv --directory <github_repo_path>/agent_sdk/examples/mcp_servers/ai-assist run ai-assist -e SALESFORCE_USERNAME your_username -e SALESFORCE_PASSWORD your_password
```

Upon launching, the Inspector will display a URL that you can access in your browser to begin debugging.

## Enhancing Results for Specific Clients

### Cursor

In Cursor, you can create custom rules to enhance the agent creation process. For example:

```
# After the generate_agent_metadata is called:
- Create a folder in our project root if it does not exist called: agents
- Store the JSON output in the agents folder: agent_name.json 
- Create a visual markdown of all the agent information including description, name, utterances, topics, and actions
- Generate a Mermaid diagram showing the Agent as a Node with Topics as sub-Nodes, and Actions as subnodes of the topics
- After it is generated, ask if the user wants to deploy the agent
```

### Claude

In Claude, you can create a project with instructions to use other MCP servers to enhance the agent creation process:

```
Please guide the user to creating their agentforce agent. Use the get_agent_requirements tool to help gather requirements. 
Once enough requirements have been collected, call generate_agent_metadata to generate the whole metadata. 
Please visualize the topics and agent metadata in the canvas with a nice React page showing the agent as a node, 
with topics as sub-nodes, and actions as sub-nodes of topics. 
Once the topics have been generated, call the deploy_agent to deploy the agent.
Check if the agent deployment status is successful.
```