import os 

from openai import OpenAI
from dotenv import load_dotenv

from src.schemas import Agent
from src.utils import AgentConfig
from src.ensemble import Ensemble
from src.tools import tool_registry
from src.agents import agent_registry
from src.orchestrator import AgentOrchestrator

base_agent = Agent(
    name="MultiToolAgent",
    instructions="""
        You are a helpful agent that assist a users in completing tasks using multiple tools available to you
    """,
    functions=[agent_registry['wiki_search'], tool_registry['calculator'], tool_registry['current_datetime']]
)

load_dotenv()

model = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

model_ensemble = Ensemble()

if __name__ == "__main__":

    query = "what is obama's age minus 2"

    agent_config = AgentConfig()

    agent_config.set_model_client(model)

    agent_config.set_model_ensemble(ensemble=model_ensemble)

    agent_config.set_token_limit(1000)

    agent_config.set_max_interactions(5)

    orchestrator = AgentOrchestrator(agent_config, base_agent)

    orchestrator.execute(query)