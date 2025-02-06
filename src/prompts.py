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
    "{task}\n\nBegin by identifying key factors that will inform your decision-making process.\n\nNext, evaluate potential approaches using the available tools below:\n\nAvailable Tools:\n{tools}\n\nConsider how each tool can be effectively utilized as you refine your strategy.\n\nContinuously assess and adjust your approach based on insights and new information emerging during the process.\n\nFinally, summarize your thought process and the strategy employed in resolving the challenge.\n\nEnsure that your explanation is thorough and reflects a dynamic problem-solving mindset.\n\n--- Context history inserted below: "
)

def get_thought_prompt(task, tools):
    """Generates a detailed thought prompt with provided request and available tools."""
    return THOUGHT_PROMPT_STRING.format(
        task=task,
        tools=tools
    )


# Best Tool 
BEST_TOOL_PROMPT_STRING = (
    "To solve the following task {task}. Select the best to of the available to achieve, if there is a suitable tool in select. Please see the following tool for choice: {tools} "

)

def get_best_tool_prompt(task, tools):
    """Generates a detailed thought prompt with provided request and available tools."""
    return BEST_TOOL_PROMPT_STRING.format(
        task=task,
        tools=tools
    )


# Observation prompts
OBSERVATION_PROMPT_STRING = (
    "The following context enough to solve the following task: {task},\n\n"
    "Assign a confidence score on the quality of the llm response using the following rubric:\n"
    """
    0.8+: Continue with current sequence of consideration towards solution
    0.5-0.7: Consider the ramifications of taking a new sequence of consideration to achieve solution
    Below 0.5: Change thought sequence, backtrack and take a new way to reach soluton

    MESSAGE HISTORY: 
    -----------------
    {history}
    """
)

def get_observation_prompt(task, history):
    """Generates a detailed thought prompt with provided request and available tools."""
    return BEST_TOOL_PROMPT_STRING.format(
        task=task,
        history=history
)

EXECUTE_ACTION_PROMPT_STRING = (
    "In pursuit of achieving the following task: \n"
    "{task}"
    """
    Determine the parameters to envoke and utilize the following tool: {tool_name}

    The tool has the following signature: {signature}

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