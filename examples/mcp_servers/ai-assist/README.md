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

## Configuration

To deploy an agent, you need to configure the server with your Salesforce credentials. Use the following configuration template, replacing placeholders with your actual credentials:

```json
"ai-assist": {
    "command": "uv",
    "args": [
        "--directory",
        "/path/to/your/mcp/server",
        "run",
        "ai-assist"
    ],
    "env": {
        "SALESFORCE_USERNAME": "your_username",
        "SALESFORCE_PASSWORD": "your_password"
    }
}
```

## Quickstart

### Install

#### Claude Desktop

On MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`
On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

You can also install this server in [Claude Desktop](https://claude.ai/download) and interact with it right away by running:
```bash
mcp install server.py
```

Alternatively, you can test it with the MCP Inspector:
```bash
mcp dev server.py
```.com/jlowin/fastmcp


### Debugging

For debugging, use the [MCP Inspector](https://github.com/modelcontextprotocol/inspector) to visualize and troubleshoot the server's operations. Launch it with:

```bash
npx @modelcontextprotocol/inspector uv --directory /path/to/your/project run ai-assist -e SALESFORCE_USERNAME your_username -e SALESFORCE_PASSWORD your_password
```

Upon launching, the Inspector will display a URL that you can access in your browser to begin debugging.