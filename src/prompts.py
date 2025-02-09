import inspect

# THOUGHT PROMPTS:
THOUGHT_PROMPT = """
        Please provide a clear, detailed explanation of your step-by-step plan to address the following challenge:

        {self.request}

        Begin by identifying key factors that will inform your decision-making process.

        Next, evaluate potential approaches using the available tools below:

        Available Tools:
        {tools}

        Consider how each tool can be effectively utilized as you refine your strategy.

        Continuously assess and adjust your approach based on insights and new information emerging during the process.

        Finally, summarize your thought process and the strategy employed in resolving the challenge.

        Ensure that your explanation is thorough and reflects a dynamic problem-solving mindset.

        --- Context history inserted below:

    """

THOUGHT_PROMPT_STRING = (
    "Please provide a clear, detailed explanation of your step-by-step plan to address the following:\n\n"
    "{task}\n\nBegin by identifying key factors that will inform your decision-making process.\n\nNext, evaluate potential approaches using the available tools below:\n\nAvailable Tools:\n{tools}\n\nConsider how each tool can be effectively utilized as you refine your strategy, make sure to identify on appropriate tool or a;ert to appropriate tool not being available. IF THE APPROPRIATE TOOL IS NOT AVAILABLE SAY SWITCH AGENT \n\nContinuously assess and adjust your approach based on insights and new information emerging during the process.\n\nFinally, summarize your thought process and the strategy employed in resolving the challenge.\n\nEnsure that your explanation is thorough and reflects a dynamic problem-solving mindset.\n\n\nAvailable Tools:\n{tools}--- Context history inserted below: "
)

def get_thought_prompt(task, tools):
    """Generates a detailed thought prompt with provided request and available tools."""
    return THOUGHT_PROMPT_STRING.format(
        task=task,
        tools=tools
    )

# Best Tool 
BEST_TOOL_PROMPT_STRING = (
    "To solve the following task {task}. Select the best tool of the available from list below: {tools}.\n If there is not a suitable tool available please return no suitable tool available "
    "\nAvailable Tools:\n{tools}"
    "Please use the context history below to inform your decision \n"
    "Context History:"
)

def get_best_tool_prompt(task, tools):
    """Generates a detailed thought prompt with provided request and available tools."""
    return BEST_TOOL_PROMPT_STRING.format(
        task=task,
        tools=tools
    )


# Observation prompts
OBSERVATION_PROMPT_STRING = (
    "Is the following context history finally enough to solve the task {task}?,\n\n"

    "Assign a quality confidence score  between 0.0 and 1. to guide the approach:\n"
    """

    0.8+: Continue with current approach towards solution

    0.5-0.7: Consider the outcomes of taking a new approach

    Below 0.5: change to main agent and try again with new approach

    if the confidence score is below 0.6 do not label as
    finished or stop.

    please return an indication to switch from the current agent to main agent or no tool available if confidence is below .6

    MESSAGE HISTORY: 
    -----------------
    {history}
    """
)

def get_observation_prompt(task, history):
    """Generates a detailed thought prompt with provided request and available tools."""
    return OBSERVATION_PROMPT_STRING.format(
        task=task,
        history=history
)

EXECUTE_ACTION_PROMPT_STRING = (
    "In pursuit of achieving the following task: \n"
    "{task}"
    """
    Determine the parameter to envoke and utilize the following tool: {tool_name}

    Given that the tool has the following signature: {signature}

    If using the wiki_query make sure to return on a noun as the string param 

    if using the calculator please pass the params seperated by comma to avoid:
        Traceback (most recent call last):
    File "/home/mab07/code/sandbox/fullstack_ai/agentic_play/main.py", line 34, in <module>
        orchestrator.execute(query)
    File "/home/mab07/code/sandbox/fullstack_ai/agentic_play/src/orchestrator.py", line 36, in execute
        agent, skip = self.__action(agent)
    File "/home/mab07/code/sandbox/fullstack_ai/agentic_play/src/orchestrator.py", line 99, in __action
        self.__execute_action(tool_builder, agent)
    File "/home/mab07/code/sandbox/fullstack_ai/agentic_play/src/orchestrator.py", line 164, in __execute_action
        task_result = tool.func(resp)
    TypeError: calculator() missing 2 required positional arguments: 'a' and 'b'

    def calculator(input_str):

    parsed = input.split(",")
    operation = parsed[0]
    a = parsed[1]
    b = parsed[2]
    if operation == "add":
        return a + b
    
    elif operation == "subract":
        return a-b 
    elif operation == "multiply":
        return a * b 
    
    elif operation == "divide":
        return a / b 
    else:
        return "Invalid operation type"
    
    Return only tool param as text string, no other content, no other formatting including json, or paranthesis etc

    MESSAGE HISTORY
    ---------------

    """
)

def get_execute_action_prompt(task, tool):
    return EXECUTE_ACTION_PROMPT_STRING.format(
        task=task,
        tool_name=tool.name,
        signature=inspect.signature(tool.func)

    )