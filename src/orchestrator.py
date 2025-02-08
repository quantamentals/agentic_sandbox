import inspect
import json
from src.utils import AgentConfig, ToolBuilder
from src.schemas import Agent, AgentObservation,  ActiveTool
from src.prompts import get_thought_prompt, get_best_tool_prompt, get_observation_prompt, get_execute_action_prompt
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

            if observation:
                content_dict = json.loads(observation.choices[0].message.content)

                if content_dict.get('stop'):
                    print("Thought: I know the final answer. \n")
                    final_answer = content_dict.get('final_answer', '')
                    print(f"Final Answer: {final_answer}")
                    return final_answer
        

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
            print("No previous messages available ", "\n")

        content_history = "\n".join(message['content'] for message in self.ensemble.history())

        thought_prompt += "\n" + content_history

        response = self.ensemble.evaluate(thought_prompt, agent, model=self.config.model)

        # response = "Response"

        print(f"*******************Thoughts*****************")
        print(f"{agent.name} Agent Thoughts: {response}")

        message=self.ensemble.build_message(role="assistant", content=response, agent=agent)
        
        self.ensemble.store(message)

    def __action(self, agent:Agent) -> tuple[Agent, bool]:
        """The Agent should decide on the action to take"""

        # get the tools of the agent: tools could be functional or agentic tools
        tool_builder = self.__choose_action(agent)

        # # handle the age if agent is present the execute agents tool
        if tool_builder:
            if isinstance(tool_builder.func, Agent):
                agent=tool_builder.func # the tool builder returns an agent 
                print(f"Action <switching agent>: Now utilizing sub agent {agent.name}\n")
                return agent, True
            
            self.__execute_action(tool_builder, agent)
        else:
            print("Recommended Active Tool is not Found", "\n")
            agent = self.main_agent
            print(f"Action <switching agent>: Now utilizing Main Agent: {agent.name} \n")
            return agent, True
        return agent, False
    
    def __choose_action(self, agent: Agent) -> ToolBuilder:

        tools = self.__retrieve_tools(agent=agent)

        choose_best_tool_prompt = get_best_tool_prompt(task=self.task, tools=tools)

        content_history = "\n".join([message['content'] for message in self.ensemble.history()])

        prompt = choose_best_tool_prompt + "\n" + content_history

        tool_choice_resp = self.ensemble.evaluate(prompt=prompt, agent=agent, output_schema=ActiveTool)

        res = tool_choice_resp.choices[0].message.parsed

        message = self.ensemble.build_message(
            role="assistant", 
            content=f"Please use the following tool: {res.tool_name} Reason: {res.reason_of_choice} ", 
            agent=agent
        )

        self.ensemble.store(message=message)

        active_tool_builder = [tool for tool in agent.functions if tool.name == res.tool_name]

        print('The active tool chosen: ', active_tool_builder, '\n')

        return active_tool_builder[0] if active_tool_builder else None

    def __execute_action(self, tool:ToolBuilder, agent: Agent):
        if tool is None:
            return
        
        print(f"Executing the Agent tool: {tool.name}")
        
        execute_prompt = get_execute_action_prompt(task=self.task, tool=tool)

        message_history = "\n".join([message['content'] for message in self.ensemble.history()])

        prompt = execute_prompt + message_history

        parameters = inspect.signature(tool.func).parameters

        if len(parameters)>0:
            prompt +="""RESPONSE FORMAT:
            {{
                {', '.join([f'"{param}": <function parameter value>' for param in parameters])}
            }}
        """
        resp = self.ensemble.evaluate(prompt=prompt, agent=agent)

        message = self.ensemble.build_message(role="assistant",
                                                content=resp, 
                                                agent=agent)
        self.ensemble.store(message=message)


        print("THE RESP for task exec: ", resp)

        task_result = tool.func(resp)

        print(f"Task Result: {task_result}")

        message = self.ensemble.build_message(role="assistant",
                                              content=task_result, 
                                              agent=agent)
        self.ensemble.store(message=message)

    def __observation(self, agent) -> AgentObservation:
        """Execute an action and observe feedback from action"""

        # observe responses for confidence of achieving with available info
        # if confidence is less than certain threshold switch to main agent
        # use main agent to identify the appropriate agent  / tool 
        # take the previous context into consideration to find where you are in the process
        pass 

    def __retrieve_tools(self, agent) -> str:
        """NOTE: change this to extract agent details and turn to dict with name and tools"""
        tools = [tool for tool in agent.functions if isinstance(tool, ToolBuilder)]
        str_tools = [tool.name + " - " + tool.desc for tool in tools]
        return "\n".join(str_tools)

