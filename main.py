import os 
from openai import OpenAI
from dotenv import load_dotenv

from src.orchestrator import AgentOrchestrator
from src.schemas import Agent
from src.utils import AgentConfig
from src.tools import tool_registry
from src.agents import agent_registry

base_agent = Agent(
    name="MultiToolAgent",
    instructions="""
        You are a helpful agent that assist a users in completing tasks using multiple tools available to you
    """,
    functions=[tool_registry['calculator'], agent_registry['wiki_search']]
)

load_dotenv()

model = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


if __name__ == "__main__":

    query = "Why is the sky blue"

    agent_config = AgentConfig()

    agent_config.with_model_client(model)

    agent_config.with_token_limit(1000)

    agent_config.with_max_interactions(5)

    orchestrator = AgentOrchestrator(agent_config, base_agent)

    orchestrator.execute(query)