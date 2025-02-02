from openai import OpenAI # create custom types

class ToolBuilder:

    """
    NOTE: add packs or specific functionality via depenedency injection and build a tool object HERE???
    """
    def __init__(self, name: str, func, desc) -> None:
        self.desc = desc
        self.name = name
        self.func = func

    def act(self, **kwargs) -> str:
        return self.func(**kwargs)
    
    def build(self):
        pass 
    
class AgentConfig:
    def __init__(self):
        self.max_interactions = 3
        self.model = None
        self.token_limit: int = 5000

    def with_model_client(self, model: OpenAI):
        self.model = model
        return self

    def with_token_limit(self, token_limit: int):
        self.token_limit = token_limit
        return self

    def with_max_interactions(self, max_int: int):
        self.max_interactions = max_int
