from src.schemas import Agent
from src.utils import AgentConfig
from src.tools import tool_registry
from src.agents import agent_registry
from src.orchestrator import AgentOrchestrator

model = "gpt-4o"

base_agent = Agent(
    name="MultiToolAgent",
    instructions="""
        You are a helpful agent that assist a users in completing tasks using multiple tools available to you
    """,
    functions=[agent_registry['wiki_search'], 
               tool_registry['calculator'], 
               tool_registry['Date_of_today'],
    ]
)

if __name__ == "__main__":

    query = "what is obama's age minus 2"

    agent_config = AgentConfig()

    agent_config.set_model_client(model)

    agent_config.set_token_limit(1000)

    agent_config.set_max_interactions(10)

    orchestrator = AgentOrchestrator(agent_config, base_agent)

    orchestrator.execute(query)