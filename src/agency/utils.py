from .base_agent import BaseAgent
from src.ensemble import Ensemble

class UserIntentAgent(BaseAgent):

    def __init__(self, name, ensemble):
        super().__init__(name, ensemble)
        self.config = {}
        self.ensemble = Ensemble(config=self.config) # can inject this agent into the ensemble with the collection of models and other agents / tools
        self.instructions= """You are a n helpful assistant for discovering a users prompt intent"""
        self.messages = []

    def execute(self, task_prompt):

        # NOTE: reconcile how I want to build the prompt and execute on ensemble

        chat_message = self.ensemble.build_chat_messages(agent=self,prompt=task_prompt)
        
        return self.ensemble.evaluate(prompt=task_prompt, agent=self)
    


class JSONAgent(BaseAgent):

    def __init__(self, name, ensemble):
        super().__init__(name, ensemble)
        self.config = {}
        self.ensemble = Ensemble(config=self.config) # can inject this agent into the ensemble with the collection of models and other agents / tools
        self.instructions= """You are a helpful assistant for fixing json of llm responses to appropriate use ready structure. Other agents use you to correctly format their outputs in their return statement or in api endpoints"""

    def execute(self, task_prompt):

        # NOTE: reconcile how I want to build the prompt and execute on ensemble

        chat_message = self.ensemble.build_chat_messages(agent=self,prompt=task_prompt)
        
        return self.ensemble.evaluate(prompt=task_prompt, agent=self)