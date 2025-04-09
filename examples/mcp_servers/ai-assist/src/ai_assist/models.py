from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from agent_sdk.models.agent import Agent
from agent_sdk.models.topic import Topic
from agent_sdk.models.system_message import SystemMessage
# Salesforce Credentials

class SalesforceCredentials(BaseModel):
    """Represents Salesforce credentials."""
    username: str = Field(description="The username of the Salesforce user")
    password: str = Field(description="The password of the Salesforce user")
    domain: str = Field(description="The domain of the Salesforce user", default="login")


class DeploymentState(BaseModel):
    """Tracks the deployment state of an agent including its metadata and credentials."""
    agent: Agent = Field(description="The deployed agent")
    deployment_result: Optional[Any] = Field(default=None, description="Result of the deployment")

class AgentMetadata(BaseModel):
    """Represents the metadata of an agent."""
    description: str = Field(description="The description of the agent")
    sample_utterances: List[str] = Field(description="The sample utterances of the agent")
    topics: List[Topic] = Field(description="The topics of the agent")
    company_name: str = Field(description="The name of the company the agent belongs to")
    agent_name: str = Field(description="The name for the agent created in the get_agent_requirements tool")
    system_messages: List[SystemMessage] = Field(description="The system messages of the agent")
