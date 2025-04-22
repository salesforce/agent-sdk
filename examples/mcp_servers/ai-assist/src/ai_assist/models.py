from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from agent_sdk.models.agent import Agent
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
    login_url: Optional[str] = Field(default=None, description="The login URL of the Salesforce instance")


# Agent Metadata

class InputModel(BaseModel):
    """Input parameter for an action."""
    
    name: str = Field(..., description="Name of the input parameter")
    description: str = Field("", description="Description of the input parameter")
    data_type: str = Field("String", description="Data type of the input parameter")
    required: bool = Field(True, description="Whether the input parameter is required")


class OutputModel(BaseModel):
    """Output parameter or response from an action."""
    
    name: Optional[str] = Field(None, description="Name of the output parameter")
    description: Optional[str] = Field(None, description="Description of the output parameter")
    data_type: Optional[str] = Field(None, description="Data type of the output parameter")
    required: Optional[bool] = Field(None, description="Whether the output parameter is required")
    
    # Example output fields
    status: Optional[str] = Field(None, description="Status of the example output")
    details: Optional[Dict[str, Any]] = Field(None, description="Details of the example output")


class ActionModel(BaseModel):
    """Action class for agent."""
    
    name: str = Field(..., description="Name of the action")
    description: str = Field(..., description="Description of the action")
    inputs: List[InputModel] = Field(default_factory=list, description="List of input parameters")
    outputs: List[OutputModel] = Field(default_factory=list, description="List of output parameters")
    example_output: Optional[Dict[str, Any]] = Field(None, description="Example output for the action")


class TopicModel(BaseModel):
    """Topic class for categorizing actions in an agent."""
    
    name: str = Field(..., description="Name of the topic")
    description: str = Field(..., description="Description of the topic")
    scope: str = Field(..., description="Scope of the topic")
    actions: List[ActionModel] = Field(default_factory=list, description="List of actions in the topic")
    instructions: List[str] = Field(default_factory=list, description="Instructions for the topic")



class AgentMetadata(BaseModel):
    """Represents the metadata of an agent."""
    description: str = Field(description="The description of the agent")
    sample_utterances: List[str] = Field(description="The sample utterances of the agent")
    topics: List[TopicModel] = Field(description="The topics of the agent")
    company_name: str = Field(description="The name of the company the agent belongs to")
    agent_name: str = Field(description="The name for the agent created in the get_agent_requirements tool")
    system_messages: List[SystemMessage] = Field(description="The system messages of the agent")
    


class AgentResponsibilitiesPayload(BaseModel):
    """Payload for agent responsibilities generation"""

    primary_audience: str = Field(
        ...,
        description="Primary audience for the agent. Suggested values: 'internal employees', 'external customers'",
    )
    company_name: str = Field(..., description="Name of the company")
    agent_description: str = Field(..., description="Description of the AI agent")
    domain: Optional[str] = Field(None, description="Industry/domain of the company")
    company_website: Optional[str] = Field(None, description="Company website URL")
    business_requirements: Optional[str] = Field(None, description="Business challenges the company is facing and goals the company wants to achieve")
