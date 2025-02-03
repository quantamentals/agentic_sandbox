from src.model import Model
from typing import Optional, Type
from pydantic import BaseModel
from src.schemas import Agent

class Ensemble:
    """A collection of models and methods for coordination, structuring, concurrent use, and long-running processes."""

    BASE_SYSTEM_PROMPT = """ """

    def __init__(self, config):
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
        return "\n".join(self.messages)

    def build_system_prompt(self, agent):
        """Build the system prompt for the agent."""
        system_prompt = self.BASE_SYSTEM_PROMPT
        system_prompt += agent.instructions
        return system_prompt

    def build_user_prompt(self, prompt):
        """Build the user prompt."""
        # NOTE: allows me to insert base user prompt additions
        return prompt  # Placeholder implementation; customize as needed

    def build_chat_messages(self, agent, prompt):
        """Build the chat messages for the model."""
        return [
            {"role": "system", "content": self.build_system_prompt(agent)},
            {"role": "user", "content": self.build_user_prompt(prompt)}
        ]

    def execute(self, prompt: str, agent: Agent, output_schema: Optional[Type[BaseModel]] = None, model="gpt-4o-mini"):
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
                "messages": chat_messages
            }

            if output_schema:
                params['response_format'] = output_schema

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
        
    def execute_daemon(self,model:str):
        pass 