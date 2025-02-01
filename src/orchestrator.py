from src.utils import AgentConfig
from src.schemas import Agent, AgentObservation, Tool

class AgentOrchestrator:
    def __init__(self, config: AgentConfig, agent: Agent) -> None:
        self.main_agent = agent
        self.config = config
        self.task = ""

    def __thought(self):
        """The Agent should reason about the appropriate actiont to take"""
        pass 

    def __action(self) -> tuple[Agent, bool]:
        """The Agent should decide on the action to take"""
        pass 

    def __observation(self) -> AgentObservation:
        """Execute an action and observe feedback from action"""
        pass 

    def execute(self, task):
        print(f"The Task: {task}")
        self.task=task
        total_interactions = 0
        agent = self.main_agent
        while True:
            total_interactions += 1

            if self.config.max_interactions <= total_interactions:
                
                print("Max interactions reached. Exiting")
                return ""

            self.__thought(agent)

            agent, skip = self.__action(agent)

            if skip:
                continue

            observation = self.__observation(agent)
            
            if observation.stop:
                print("Though: I know the final answer. \n")
                print(f"Final Answer: {observation.final_answer}")
                return observation.final_answer
            

        
