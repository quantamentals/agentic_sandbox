from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv(override=True)

class Model:
    """
    An accessor class for AI models.
    
    A Model is a wrapper for a given ML/AI models which can be utilized for its predictive or causal outcomes
    """
    # Define model names and API key
    OLLAMA_MODEL = "llama3.2"
    GPT_MODEL = 'gpt-4o-mini'

    def __init__(self) -> None:
        self.api_key = os.getenv('OPENAI_API_KEY')
        self._validate_api_key()

        self.ollama = OpenAI(base_url=os.getenv("OLLAMA_URL_BASE"), api_key="ollama")

        self.gpt4omini = OpenAI(api_key=self.api_key)

    def _validate_api_key(self):
        """
        Validate the API key.

        Check if the API key starts with 'sk-proj-' and has a length greater than 10.
        """
        if self.api_key and self.api_key.startswith('sk-proj-') and len(self.api_key) > 10:
            print("API key looks good so far")
        else:
            print("There might be a problem with your API key? Please visit the troubleshooting notebook!")

    def build_messages(self, system_prompt, user_prompt):
        """
        Build a list of message dictionaries.

        Args:
            system_prompt (str): The system prompt.
            user_prompt (str): The user prompt.

        Returns:
            list: A list of message dictionaries.
        """
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

