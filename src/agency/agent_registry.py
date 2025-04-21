
"""
NOTE:
I need to reconcile all Agent constructs from schema, registry, tool and BaseAgents


class BaseAgent:
    def __init__(self):
        self.name = "BaseAgent"
        self.ensemble = None 


    def execute(self, task_prompt):
        pass 


class Agent(BaseModel):
    name: str = "Agent"
    model: str = "gpt-4o"
    instructions: Union[str, Callable[[], str]] = "You are a helpful agent."
    functions: List = []


also the tool builder and registry:

wiki_search_agent = Agent(
    name="wiki_agent",
    instructions="you are a helpful wikipedia search agent that find information based on a provided task and wikipedia contents",
    functions=[tool_registry['wiki_query']]

)

# Turn an agent into a tool to be used else where
wiki_search_tool = ToolBuilder(name="wiki_search", func=wiki_search_agent, desc="To search wikipedia information")

agent_registry = {
    'wiki_search': wiki_search_tool
}


"""

agent_registry = {}