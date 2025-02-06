import inspect
import json
from src.utils import AgentConfig, ToolBuilder
from src.schemas import Agent, AgentObservation,  ActiveTool
from src.prompts import get_thought_prompt, get_best_tool_prompt, get_observation_prompt
from src.ensemble import Ensemble

class AgentOrchestrator:
    """
    In this architecture the Orchestrater executes a specific agentic pattern, this base agent executes ReACt 
    """
    def __init__(self, config: AgentConfig, agent: Agent) -> None:
        self.main_agent = agent
        self.config = config
        self.ensemble= Ensemble(config=config)
        self.task = ""

    def __retrieve_tools(self, agent) -> str:
        """NOTE: change this to extract agent details and turn to dict with name and tools"""
        tools = [tool for tool in agent.functions if isinstance(tool, ToolBuilder)]
        str_tools = [tool.name + " - " + tool.desc for tool in tools]
        return "\n".join(str_tools)

    def __thought(self, agent) -> None:
        """
        The Agent should reason about the most effective action to take.
        
        This thought process involves iterative planning, continuous evaluation,
        and adaptive strategy adjustment. The goal is to demonstrate a thorough,
        self-reflective, and dynamic problem-solving approach.
        """
        tools = self.__retrieve_tools(agent)        
        thought_prompt = get_thought_prompt(self.task, tools)
        if not self.ensemble.history():
            print("No previous messages available.")
        message_history=self.ensemble.history()
        thought_prompt += message_history
        response = self.ensemble.evaluate(thought_prompt, agent, model=self.config.model)
        print(f'Agent {agent.name} THE THOUGHT RESP: ', response)
        message=self.ensemble.build_message(role="assistant", content=response, agent=agent)
        self.ensemble.store(message)

    def __action(self, agent:Agent) -> tuple[Agent, bool]:
        """The Agent should decide on the action to take"""

        # get the tools of of the main_agent: tools could be functional or agentic tools
        tool_builder = self.__choose_action(agent)

        # handle the age if agent is present the execute agents tool
        if tool_builder:
            if isinstance(tool_builder.func, Agent):
                agent=tool_builder.func # the tool builder returns an agent 
                print(f"Action <switching agent>: Now utilizing sub agent {agent.name}\n")
                return agent, True
            
            # if not an agent, the execute the action itself witht base agent 
            self.__execute_action(tool_builder, agent)
        else:
            print("Recommended Active Tool is not Found", "\n")
            agent = self.main_agent
            print(f"Action <switching agent>: Now utilizing Main Agent: {agent.name} \n")
            return agent, True
        return agent, False
    
    def __choose_action(self, agent:Agent) -> ToolBuilder:
        tools = self.__retrieve_tools(agent=agent)

        # choose appropriate prompt agent action request build
        choose_best_tool_prompt = get_best_tool_prompt(task=self.task, tools=tools)
        prompt = choose_best_tool_prompt + self.ensemble.history()

        # given  current agent use LLM choose and action the appropriate tool 
        # execute LLM reps to either OpenRouter, OpenAI, Ollama or Claude via Model Factory / Registry
        # NOTE: can a simple ML or NLP model achieve this more efficiently than LLM call???
        # the resp from the LLM should come back as pydantic class the schemas the active tool
        # tool_choice_resp: ActiveTool = ActiveTool(tool_name="wiki_search", reason_of_choice="hard coded resp TBU")
        tool_choice_resp = self.ensemble.evaluate(prompt=prompt, agent=agent, output_schema=ActiveTool)
        
        message = self.ensemble.build_message(role="assistant", 
                                              content=f"Please use the following tool: {tool_choice_resp.tool_name} Reason: {tool_choice_resp.reason} ", 
                                              agent=agent)
        
        self.ensemble.store(message=message)
        # search through the agents functions for appropriate to tool builder
        active_tool_builder = [tool for tool in agent.functions if tool.name == tool_choice_resp.tool_name]
        return active_tool_builder[0] if active_tool_builder else None


    def __execute_action(self, tool:ToolBuilder, agent: Agent):
        print("Execute FIred")
        
        get_tools_prompt = get_tools_prompt()

        if tool is None:
            return
        
        parameters = inspect.signature(tool.func).parameters

        print("TOOL Params: ", parameters)

        #TODO: have the LLM evaluate choose and set the params

        llm_resp = f"""
        {{
            {', '.join([f'"{param}": <function parameter value>' for param in parameters])}
        }}
        """
        try:
            resp = json.loads(llm_resp)
            print(resp)
        except:
            print("Error obtaining tool params")
            print(f"Invalid response: {resp} ")
            return
    
        task_result = tool.func(**resp)
        print(f"Task Result: {task_result}")

    def __observation(self, agent) -> AgentObservation:
        """Execute an action and observe feedback from action"""
        prompt = get_observation_prompt(task=self.task, 
                                        history=self.ensemble.history())
        observation_resp:AgentObservation = self.ensemble.evaluate(prompt=prompt, agent=agent, output_schema=AgentObservation)
        print("*"*50)
        message = self.ensemble.build_message(role="assistant", content=observation_resp.final_answer, agent=agent)
        self.ensemble.store(message=message)
        print(f"Agent <{agent.name}> Observation")
        print(f"Observation: {observation_resp.final_answer}")
        print(f"Confidence Interval: {observation_resp.confidence}")

        return observation_resp

    def execute(self, task):
        print("*"*50)
        print(f"The Task: {task}", "\n")
        self.task=task
        total_interactions = 0
        agent = self.main_agent
        while True:
            total_interactions += 1

            if self.config.max_interactions <= total_interactions:
                print("Max interactions reached. Exiting")
                print("*"*50)
                return ""

            print("The Current Agent: ", agent.name, "\n")
            self.__thought(agent)

            agent, skip = self.__action(agent)

            if skip:
                continue

            observation = self.__observation(agent)

            if observation.stop:
                print("Though: I know the final answer. \n")
                print(f"Final Answer: {observation.final_answer}")
                return observation.final_answer
            

        
