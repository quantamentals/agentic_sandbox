from src.ensemble import Ensemble

class BaseAgent:
    def __init__(self):
        self.name = "BaseAgent"
        self.ensemble = None
        self.instruction = None
        self.messages = []

    def set_system_instruction():
        pass 

    def set_user_message(self):
        pass 

    def execute(self, task_prompt):
        pass 
