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
    "Please provide a clear, detailed explanation of your step-by-step plan to address the following challenge:\n\n"
    "{task}\n\nBegin by identifying key factors that will inform your decision-making process.\n\nNext, evaluate potential approaches using the available tools below:\n\nAvailable Tools:\n{tools}\n\nConsider how each tool can be effectively utilized as you refine your strategy, make sure to identify on appropriate tool or a;ert to appropriate tool not being available. IF THE APPROPRIATE TOOL IS NOT AVAILABLE SAY SWITCH AGENT \n\nContinuously assess and adjust your approach based on insights and new information emerging during the process.\n\nFinally, summarize your thought process and the strategy employed in resolving the challenge.\n\nEnsure that your explanation is thorough and reflects a dynamic problem-solving mindset.\n\n--- Context history inserted below: "
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
    "Is the following context finally enough to solve the task {task}?,\n\n"

    "Assign a quality confidence score  between 0.0 and 1. to guide the approach:\n"
    """

    0.8+: Continue with current approach towards solution
    0.5-0.7: Consider the outcomes of taking a new approach
    Below 0.5: try again with new approach

    if the confidence score is below 0.6 try do not or label as finish stop

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