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