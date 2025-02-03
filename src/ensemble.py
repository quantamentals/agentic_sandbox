from src.model import Model

class Ensemble:
    """An is a collections of models and their methods for coordination structuring and use
    
    """
    BASE_SYSTEM_PROMPT = """ """
    
    def __init__(self, url):
        """
        Create this Website object from the given url using the BeautifulSoup library
        """
        self.models = Model()

    def build_system_prompt(self):
        system_prompt = self.BASE_SYSTEM_PROMPT
        system_prompt += " Extract specific market-related information, including market trends and movements, correlative and causative factors, economic indicators and data releases, and company-specific news and announcements."
        system_prompt += " Analyze the extracted information to identify patterns, relationships, and anomalies that may impact market trends and movements."
        return system_prompt

    def build_user_prompt(self, prompt):
        pass

    def build_chat_messages(self):
        return [
            {"role": "system", "content": self.build_system_prompt()},
            {"role": "user", "content": self.build_user_prompt()}
        ]
    
    def execute(self, model="'gpt-4o-mini'"):
        """
        Get a market summary based on the webpage content.

        Returns:
            str: The market summary in markdown format.
        """

        if model=="llama3.2":
            response = self.models.ollama.chat.completions.create(
            model=model,
            messages=self.build_chat_messages()
            )
            return response.choices[0].message.content
    
        if model=="gpt-4o-mini":
            response = self.models.gpt4omini.chat.completions.create(
            model=model,
            messages=self.build_chat_messages()
            )
            return response.choices[0].message.content
        
        if model=="deepseek-r1:7b":
            response = self.models.ollama.chat.completions.create(
            model=model,
            messages=self.build_chat_messages()
            )
            return response.choices[0].message.content
        
    def execute_arena(self, models:list):
        # asyncio gather the call of multiple arena requests
        pass

    def execute_daemon(self,model:list ):
        pass 