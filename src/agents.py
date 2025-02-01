from .schemas import Agent
from utils import ToolBuilder
from .tools import tool_registry


wiki_search_agent = Agent(
    name="wiki_agent",
    instructions="you are a helpful wikipedia search agent that find information based on a provided task and wikipedia contents",
    functions=[tool_registry['calculator'] ]

)


# Turn an agent into a tool to be used else where
wiki_search_tool = ToolBuilder(name="wiki_search",func=wiki_search_agent,desc="To search wikipedia information")


agent_registry = {
    'wiki_search': wiki_search_tool
}