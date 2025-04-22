import click
from mcp.server.fastmcp import FastMCP
from agent_sdk.models.agent import Agent 
from agent_sdk.models.system_message import SystemMessage
from typing import Dict, List
import os
import asyncio
import mcp.server.stdio
from dotenv import load_dotenv
from ai_assist.models import SalesforceCredentials, DeploymentState, AgentMetadata
from ai_assist.utils import (
    agent_requirements,
    deploy_agent
)
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(filename='server.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

# Store notes as a simple key-value dict to demonstrate state management
notes: dict[str, str] = {}

server = FastMCP("ai-assist")

# Dictionary to store generated agents and their metadata
server.agents = {}
# Dictionary to store conversation state
server.conversations = {}
# Dictionary to store deployment states
server.deployments: Dict[str, DeploymentState] = {}


# Get environment variables with default values
salesforce_username = os.getenv("SALESFORCE_USERNAME")
salesforce_password = os.getenv("SALESFORCE_PASSWORD")

if not salesforce_username or not salesforce_password:
    raise ValueError("SALESFORCE_USERNAME and SALESFORCE_PASSWORD environment variables must be set")

server.credentials = SalesforceCredentials(
    username=salesforce_username,
    password=salesforce_password,
    domain="login"
)


@server.tool()
def get_agent_requirements(requirements: List[str], conversation_id: str):
        """
        ### 🧠 **Prompt: Discovery Conversation for Agent Requirements**

        You are an AI Salesforce Solution Architect that helps gather requirements for an autonomous agent implementation through friendly, conversational discovery. The goal is to understand the user's business needs in depth so that we can define what kind of AI assistant to build and how it should behave.

        ---

        ### 🌟 **Job**

        Have a friendly, open conversation with the user to understand what kind of AI assistant they need. Keep it simple and helpful. Your goal is to **gather clear requirements** for their assistant — including business challenges, desired capabilities, and how success should be measured.

        ---

        ### 🛍️ **Conversation Guide**

        Use these simple guiding questions to explore the user's needs. Ask follow-ups based on their responses and validate your understanding along the way.

        #### ✅ Suggested questions to ask throughout the conversation with the user:
        1. "What business problem are you trying to solve?"
        2. "What would make this AI assistant successful for you?"
        3. "What kind of interactions or tasks should the agent handle?"
        4. "What's the name of the company you work for?"
        5. "Can you tell me a little about what your company does?"
        6. "Do you have a name in mind for the AI assistant?"

        ---

        ### 📜 **Conversation Rules**

        - Ask follow-up questions to dig deeper into challenges, goals, and processes.
        - Keep the conversation focused on **the user's needs** — not tech features.
        - Summarize along the way to **validate your understanding**.
        - Make sure to gather:
        - The user's **business problem(s)**
        - Their **desired outcomes**
        - The **channels** the agent should live on (e.g., website, mobile, email)
        - Whether it should **integrate with Salesforce**, and how (e.g., Service Cloud, Knowledge)
        - Their **company name and what the company does**
        - Whether they have a **name for the AI agent**
        - Avoid jumping into solutions or features until the business context is clear.

        ---

        ### 💬 **Example Conversation**

        **User**: I need an AI assistant for my Salesforce Commerce website.  
        **AI**: Great! I'd love to help with that. Before we dive into building the agent, I'll ask a few questions to understand your goals and business a bit better.  

        To start — could you tell me the name of your company and what you do?

        **User**: We're called *StyleNest*. We sell mid-range fashion and accessories online — mostly shoes, bags, and seasonal clothing.

        **AI**: Thanks! So *StyleNest* is an e-commerce company focused on fashion and accessories — got it.  

        What kind of challenge are you hoping this AI assistant will help solve?

        **User**: Our CSAT scores have dropped. Customers say they struggle to get quick answers, especially for order-related stuff or returns.

        **AI**: I see — so the core issue is that customers are having trouble finding the information they need, especially around orders and returns.  

        Quick question: how do customers typically reach out for support today?

        **User**: Mostly through email and live chat. We also have help articles on the website, but they're kind of buried and hard to search.

        **AI**: That helps. So it sounds like the AI assistant could help by:
        - Handling common support queries (orders, returns, delivery info)
        - Searching and summarizing help articles
        - Reducing reliance on live agents for repetitive questions

        Would you want it to escalate to a human agent when needed?

        **User**: Yes, especially for account-specific or complex questions.

        **AI**: Makes sense. A couple more things to paint the full picture:
        - Are you using Salesforce Service Cloud for customer support?
        - And is your knowledge base stored in Salesforce Knowledge?

        **User**: Yes to both.

        **AI**: Got it. And where do you want this AI to live? On your website, in the mobile app, or somewhere else?

        **User**: Just the website for now.

        **AI**: Perfect. Just to recap what I've gathered so far:

        - Company: *StyleNest*, an e-commerce fashion retailer.
        - Challenge: Customers struggle to get quick support; CSAT is dropping.
        - Existing setup: Email/live chat support, help articles in Salesforce Knowledge.
        - Goal: AI assistant to help answer routine questions, intelligently search articles, and escalate complex issues.
        - Desired outcome: Reduce ticket volume and improve CSAT.
        - Deployment: Website chatbot, integrated with Service Cloud and Knowledge.

        Before we move on to designing the assistant, one last thing — do you already have a name in mind for the AI assistant, or shall we come up with one together?

        **User**: Let's call it "Nyla" — kind of goes with the fashion theme.

        **AI**: Love it — "Nyla" it is! That gives us everything we need to start mapping out her capabilities.

        ---

        ### 🔄 **Using the Tool**

        - Use the same `conversation_id` to keep adding more requirements to the same conversation or agent. This ensures that all gathered requirements are associated with the correct context and can be referenced or updated as needed.
        - When new requirements are identified, simply call the tool again with the existing `conversation_id` and the new requirements to append them to the ongoing conversation.
        """
        return agent_requirements(requirements, conversation_id, server)
        
@server.tool()
def generate_agent_metadata(agent_metadata: dict):
    """
        Your job is to create a description of an AI Agent, generating sample utterances, and convert a list of topics into a specific JSON format. The description of the AI Agent and the sample utterances should be combined into the JSON object. The description and sample utterances should be grounded in the context of the conversation provided. 
        Always ask for the company name first and what the name of the agent should be if we don't have it already.
        
        # Rules:
        - When converting the Topics, description, scope, instructions and actions to JSON, DO NOT MODIFY any of the properties or language. 
        - Never use or include emojis
        - Use the requirements gathered from the conversation to generate the agent metadata

        # Guidelines
        Follow these instructions carefully to complete the task:

        1. First, review the context of the conversation if provided, we provided the requirements for the agent. Come up with a name for the agent.

        2. Now, examine the list of topics to be converted:
        3. Convert each topic into the required JSON format 

        4. For each topic:
        a. Use the topic name as provided in the list for the "name" field.  The topic name must only use ASCII characters and _, if there are any other characters (accents, emojis, etc...), please convert them to plain ASCII or a _ if its a space.
        b. Use the description provided in the description field. Do not change the description.
        c. Use the scope provided in the scope field. Do not change the scope.
        d. Include all of the instructions provided in the instructions list. Do not change any of the instructions
        e. Generate a list of actions for the "actions" field, following the format described in step 5. Do not change any of the action properties. 
        f. Ensure you do not change the fields from the Topics 
        g. Remove all '/' from the actions.  
        h. Remove any actions that do Knowledge Lookups or search knowledge action. This includes but is not limited to: Knowledge_Lookup, Search_Knowledge... etc. If an instruction includes the "Knowledge_Lookup" action, modify the instruction to something like "search the knowledge base".

        5. For each action, generate an example_output as a JSON object that demonstrates its full capabilities. Rules for the example output:
        a. Provide a detailed and realistic return value
        b. Include any relevant metadata or additional information that the function might reasonably return.

        6. Generate only 1 or 2 topics if possible.

        7. Given the Topics and the Context of the conversation, generate a 1-2 description of the AI Agent and what it does. The description should start with: "You are an AI Agent whose job is to help <COMPANY> customers...."

        8. Given the Topics, Instructions, and actions, generate 4-5 sample utterances a user might use to engage with the AI Agent. These sample utterances should tie directly back to an instruction or an action. When including IDs in the sample utterances, make the IDs realistic. Do not include any utterances about escalating or speaking to a human.

        9. Ensure that all JSON is properly formatted and valid. Always return only JSON.

        ## Rules for Instructions: 
        - Each instruction should be a single topic-specific guideline, usually phrased as but not limited to "If x, then y…", "As a first step,…", "Once the customer does...", "When a customer...". 
        - Instructions should be non-deterministic and should not include sensitive or deterministic business rules. 
        - Instructions should also provide as much context as possible, which is derived from the transcript, so that the AI Agent can have a better understanding of the use case. 
        - When writing instructions, ensure that they do not conflict with each other within a topic. 
        - When writing instructions, include instructions to ask for the input of the actions in order to run the action.
        - Also use absolutes such as "Must, "Never", or "Always" sparingly -- instead use verbiage that allows more flexibility.
        - In every topic, except for an "Escalation" topic, include an instruction that enables the AI Agent to search knowledge to help the customer with their questions related to the <topic>. 

        Provide relevant actions to support the Topic, scope, and instructions. 
        ## Rules for actions: 
        - Actions are effectively the function that gets invoked to do things for the topic. 
        - Actions can have multiple inputs if needed. 
        - Outputs represent what properties are sent as a response of the action
        - When writing action descriptions, include in the action description what inputs are needed. Example: "Retrieve the current status and tracking information of a customer's order for a given an orderId"
        - Input descriptions are 1-2 sentences that describe the input and how it is used.
        - Output descriptions are 1-2 sentences that describe the output and how it is used.
        - Action descriptions should provide context of when the action should be used and also what information is needed from the customer.
        - The AI Agent has access to the internet through an action. If there is an action that could be answered through a web search on company's website, such as troubleshooting steps or questions, company policy information, policy guidance, technical support or general company information, then always generate an action called "Knowledge_Lookup".

        # Generate the sample utterances for the agent
        - Generate 4-5 sample utterances for the agent based on the topics and instructions.
        - The sample utterances should tie directly back to an instruction or an action.

        # Generate the description of the agent
        - Generate a 1-2 sentence description of the agent based on the topics and instructions.
        - The description should start with: "You are an AI Agent whose job is to help ...."
        
        # Always generate some system messages for the agent
        - Generate a System messages, such as welcome and error messages that are sent when your users begin using an agent and if they encounter system errors.
        - The system messages should be in the format of a JSON object with the following fields:
            - name: The name of the system message
            - content: The content of the system message
            - description: The description of the system message
        
        Args:
            agent_metadata: The agent metadata as a dictionary
        Returns:
            The generated agent metadata
        """
    try:
        # Convert dict to AgentMetadata object by validating against schema
        metadata_obj = AgentMetadata.model_validate(agent_metadata)
        server.agents[metadata_obj.agent_name] = metadata_obj
        return agent_metadata
    except Exception as e:
        raise ValueError(f"Invalid agent_metadata: {e}")

generate_agent_metadata.inputSchema = {
    "type": "object",
    "properties": {
        "agent_metadata": AgentMetadata.model_json_schema(),
    },
    "required": ["agent_metadata"],
}


@server.tool()
def deploy_agent_tool(agent_metadata: dict):
        """
        Deploy a previously generated agent to Salesforce.
        
        # Rules:
        - The agent must be generated by the generate_agent_metadata tool
        - Always ask the user first if they want to deploy the agent to their Salesforce org first
        
        If the deployment fails, return the error message from the deploy_agent tool
        If there is no deployment result, return "Deployment failed"
        If the deployment Status is None, also return "Deployment failed", but keep the login URL so user can inspect the deployment logs
        In the deployment result, include the login URL of the Salesforce instance so the user can login to the agent.
        
        Args:   
            agent_metadata: The agent metadata to deploy as a dictionary
        Returns:
            dict: The deployment status from Salesforce
        """
        try:
            # Convert dict to AgentMetadata object by validating against schema
            metadata_obj = AgentMetadata.model_validate(agent_metadata)
            result = deploy_agent(metadata_obj, server)
            
            # Update deployment state
            server.deployments[metadata_obj.agent_name] = result
            
            # Return the deployment status
            return result
        except Exception as e:
            raise ValueError(f"Invalid agent_metadata: {e}")

deploy_agent_tool.inputSchema = {
    "type": "object",
    "properties": {
        "agent_metadata": AgentMetadata.model_json_schema(),
    },
    "required": ["agent_metadata"],
}


@click.command()
@click.option("--port", default=8000, help="Port to listen on for SSE")
@click.option(
    "--transport",
    type=click.Choice(["stdio", "sse"]),
    default="stdio",
    help="Transport type",
)
def main(port=8000, transport="stdio"):
    # Update server settings if using SSE transport
    if transport == "sse":
        server.settings.port = port
    
    # Run the server with the specified transport
    server.run(transport=transport)


if __name__ == "__main__":
    main()


