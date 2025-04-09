from mcp.server.fastmcp import FastMCP
from agent_sdk.models.agent import Agent 
from agent_sdk.models.system_message import SystemMessage
from typing import Dict, List
import os
from dotenv import load_dotenv
from ai_assist.models import SalesforceCredentials, DeploymentState, AgentMetadata
from ai_assist.utils import deploy_agent

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
        An AI assistant that helps gather requirements for an autonomous agent implementation through conversation.
        
        # Job
        Have a friendly conversation with the user to understand what kind of AI assistant they need. Keep the conversation simple and focused on understanding their needs.

        # Questions Guide
        Use these simple questions to guide the conversation adn gather the business requirements for the AI:

        1. "What business problem are you trying to solve?"
        2. "What would make this AI successful for you?"
        3. "What is the name of the company you work for?"
        4. "What is the name of the agent you want to create?"
        5. "What is the name of the company you work for?"
        Keep the conversation natural - focus on understanding what the user needs.

        Once you understand their needs well enough, ask if they'd like to see your suggested topics and actions for the AI.


        Args:
            requirements: The requirements for the agent
            conversation_id: Optional ID to maintain conversation state
            company_name: The name of the company the agent belongs to
            agent_name: The name for the agent
        Returns:
            dict: Response containing assistant's message and any generated topics
        """
        # Initialize or retrieve conversation state
        if conversation_id and conversation_id not in server.conversations:
            server.conversations[conversation_id] = {
                "requirements": requirements,
                "complete": False
            }
        
        # Process message and update conversation state 
        
        # Return response with conversation state
        return {
            "message": "Your response here",
            "requirements": server.conversations.get(conversation_id, {}).get("requirements", []),
            "complete": server.conversations.get(conversation_id, {}).get("complete", False),
            "conversation_id": conversation_id
        }
        
@server.tool()
def generate_agent_metadata(agent_metadata: AgentMetadata):
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
        a. Use the topic name as provided in the list for the "Topic" field.  The topic name must only use ASCII characters and _, if there are any other characters (accents, emojis, etc...), please convert them to plain ASCII or a _ if its a space.
        b. Use the classification description provided in the ClassificationDescription field. Do not change the classification description.
        c. Use the scope provided in the scope field. Do not change the scope.
        d. Include all of the instructions provided in the instructions list. Do not change any of the instructions
        e. Generate a list of actions for the "Actions" field, following the format described in step 5. Do not change any of the action properties. 
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
        
        # Generate the system messages for the agent
        - Generate a ystem messages, such as welcome and error messages that are sent when your users begin using an agent and if they encounter system errors.
        - The system messages should be in the format of a JSON object with the following fields:
            - name: The name of the system message
            - content: The content of the system message
            - description: The description of the system message
        
        Args:
            agent_metadata: The agent metadata to generate
        Returns:
            The generated agent metadata
        """
    server.agents[agent_metadata.agent_name] = agent_metadata
    return agent_metadata


@server.tool()
def deploy_agent_tool(agent_name: str):
        """
        Deploy a previously generated agent to Salesforce.
        
        # Rules:
        - The agent must be generated by the generate_agent_metadata tool
        - Use the agent_name generated by the generate_agent_metadata tool to deploy the agent
        
        If the deployment fails, return the error message from the deploy_agent tool
        If there is no deployment result, return "Deployment failed"
        
        Args:   
            agent_name: The name of the agent to deploy that was generated by the generate_agent_metadata tool
        Returns:
            dict: The deployment status from Salesforce
        """
        # Retrieve the agent from server state
        agent: AgentMetadata = server.agents.get(agent_name)
        if not agent:
            raise ValueError(f"No agent found with name: {agent_name}")

        new_agent = Agent(
            name=agent_name,
            description=agent.description,
            agent_type="External",
            company_name=agent.company_name
        )
        
        new_agent.sample_utterances = agent.sample_utterances
        new_agent.system_messages = agent.system_messages
        new_agent.topics = agent.topics
        # Deploy the agent
        result = deploy_agent(new_agent, server.credentials.username, server.credentials.password)
        
        # Update deployment state
        server.deployments[agent_name] = result
        
        # Return the deployment status
        return result



def main():
    server.run()

