from agent_sdk.models.agent import Agent
from agent_sdk.core.agentforce import  Agentforce
from ai_assist.models import DeploymentState




def deploy_agent(agent: Agent, username: str, password: str) -> DeploymentState:
    """Deploy an agent in Salesforce"""
    # Initialize AgentForce client
    # auth = BasicAuth(username=username, password=password)
    agent_force = Agentforce(username=username, password=password)
    try:
        status = agent_force.create(agent)
        return DeploymentState(
            agent=agent,
            deployment_result=status,
        )
    except Exception as e:
        return DeploymentState(
            agent=agent,
            deployment_result=str(e)
        )