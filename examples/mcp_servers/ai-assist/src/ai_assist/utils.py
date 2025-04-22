import os
import sys

from agent_sdk.models.agent import Agent
from agent_sdk.core.agentforce import Agentforce
from agent_sdk.core.auth import BasicAuth
from typing import List, Dict, Any
from ai_assist.models import SalesforceCredentials, DeploymentState, AgentMetadata
from agent_sdk.models.topic import Topic
from agent_sdk.models.action import Action, Input, Output
import logging

logger = logging.getLogger(__name__)

def agent_requirements(requirements: List[str], conversation_id: str, server: Any) -> Dict:
    """
    An AI assistant that helps gather requirements for an autonomous agent implementation through conversation.
    """
    # Initialize or retrieve conversation state
    if conversation_id not in server.conversations:
        server.conversations[conversation_id] = {
            "requirements": requirements,
            "complete": False
        }

    # Return response with conversation state
    return {
        "message": "Your response here",
        "requirements": server.conversations.get(conversation_id, {}).get("requirements", []),
        "complete": server.conversations.get(conversation_id, {}).get("complete", False),
        "conversation_id": conversation_id
    }



def deploy_agent(agent: AgentMetadata, server: Any) -> DeploymentState:
    """
    Deploy a previously generated agent to Salesforce.
    """
    try:
        
        new_agent = Agent(
            name=agent.agent_name,
            description=agent.description,
            agent_type="External",
            company_name=agent.company_name
        )

        new_agent.sample_utterances = agent.sample_utterances
        new_agent.system_messages = agent.system_messages


        new_topics = []
        for topic in agent.topics:
            new_topics.append(Topic.model_validate(topic.model_dump()))

        new_agent.topics = new_topics
        basic_auth = BasicAuth(username=server.credentials.username, password=server.credentials.password, domain=server.credentials.domain)
        # Initialize AgentForce client
        agent_force = Agentforce(auth=basic_auth)
        # Create a login URL using Salesforce frontdoor.jsp
        login_url = f"https://{agent_force.instance_url}/secur/frontdoor.jsp?sid={agent_force.session_id}&retURL=/lightning/setup/EinsteinCopilot/home"
    
        status = agent_force.create(new_agent)
        deployment_result = DeploymentState(
            agent=new_agent,
            deployment_result=status,
            login_url=login_url     
        )
        # Update deployment state
        server.deployments[agent.agent_name] = deployment_result
        return deployment_result
    except Exception as e:
        logger.error(f"Error in the deploy_agent function: {e}")
        return DeploymentState(
            agent=agent,
            deployment_result=str(e)
        )

  