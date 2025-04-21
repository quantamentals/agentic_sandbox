from src.model import Model
from typing import Optional, Type
from pydantic import BaseModel
from src.schemas import Agent

class Ensemble:
    """A collection of models, agents and methods for coordination, structuring, concurrent use, and long-running processes.
    
    NOTE: I need to make a an Ensemble more generalizable to be used with multi agent CLI or inference api. Ensembles should be useful for Orchestrators of various patterns and pure api use with a specific agent. All multi agent activity must happen via an Orchestrator

    
    Ensembles should be able to fire off stand alone completion and embeddings 
    via all models in the Ensemble for now: Ollama, OpenAi and eventually OpenRouter and Claude

    Ensembles should be able to work with CSV, in memory, transactional, analytical and vectordb 

    I should be able to  inject the ensemble with agents into to interact with collection of models and other agents / tools???

    """

    BASE_SYSTEM_PROMPT = """You are a helpful assistant that assists the user in completing a task. Don't ask for user input. 
Important! You don't know the date of today, therefore you must use the Date_of_today tool to get the date of today. 
Important! You don't know math, therefore you must use the Calculator tool for math operations       
Given the following information from the context history provide for the user's task using only this information.
"""

    def __init__(self, config=None):
        """
        Initialize the Ensemble with the given configuration.
        """
        self.config = config
        self.models = Model() 
        self.messages = list()

    def store(self, message):
        """Store a message in the history."""
        self.messages.append(message)

    def history(self):
        """Retrieve the message history as a concatenated string."""
        return self.messages

    def build_system_prompt(self, agent):
        """Build the system prompt for the agent."""
        system_prompt = self.BASE_SYSTEM_PROMPT
        system_prompt += agent.instructions
        return system_prompt

    def build_user_prompt(self, prompt):
        """Build the user prompt."""
        # NOTE: allows me to insert base user prompt additions
        return prompt  # Placeholder implementation; customize as needed

    def build_message(self, role, content, agent):
        return {"role": role, "content":content, "agent":agent.name}

    def build_chat_messages(self, agent, prompt):
        """Build the chat messages for the model."""
        return [
            {"role": "system", "content": self.build_system_prompt(agent)},
            {"role": "user", "content": self.build_user_prompt(prompt)}
        ]

    def evaluate(self, prompt: str, agent: Agent, output_schema: Optional[Type[BaseModel]] = None, model="gpt-4o-mini"):
        """
        Execute the prompt using the specified model.

        Args:
            prompt (str): The user prompt to execute.
            agent (Agent): The agent providing context and instructions.
            output_schema (Optional[Type[BaseModel]]): The schema for the response format.
            model (str): The model to use for execution.

        Returns:
            str: The response from the model.
        """
        # NOTE: I need to build a model registry and then use to retrieve appropriate models by str or list

        # Build chat messages
        chat_messages = self.build_chat_messages(agent, prompt)

        if model == "llama3.2":
            response = self.models.ollama.chat.completions.create(
                model=model,
                messages=chat_messages
            )
            return response.choices[0].message.content

        elif model == "gpt-4o-mini":
            params = {
                "model": agent.model,
                "temperature": 0.1,
                "max_tokens": self.config.token_limit,
                "messages": chat_messages,
            }

            if output_schema:
                params["response_format"]=output_schema
                # Use parse with corrected schema structure
                response = self.models.gpt4omini.beta.chat.completions.parse(**params)
                return response
            else:
                # Standard completion without schema
                response = self.models.gpt4omini.chat.completions.create(**params)
                return response.choices[0].message.content
            
        elif model == "gpt-4o":
            params = {
                "model": agent.model,
                "temperature": 0.1,
                "max_tokens": self.config.token_limit,
                "messages": chat_messages,
            }

            if output_schema:
                params["response_format"]=output_schema
                # Use parse with corrected schema structure
                response = self.models.gpt4omini.beta.chat.completions.parse(**params)
                return response
            else:
                # Standard completion without schema
                response = self.models.gpt4omini.chat.completions.create(**params)
                return response.choices[0].message.content                   

        elif model == "deepseek-r1:7b":
            response = self.models.ollama.chat.completions.create(
                model=model,
                messages=chat_messages
            )
            return response.choices[0].message.content

        else:
            raise ValueError(f"Unsupported model: {model}")
        
    def evaluate_daemon(self,model:str):
        pass 

    def get_embedding(self):
        pass 

    
    def retrieve_from_storage(self):
        pass 

    def similarity_search(self):
        pass 