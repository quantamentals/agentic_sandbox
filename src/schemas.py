from pydantic import BaseModel, Field 
from typing import Callable, Union, List, Any

class ActiveTool(BaseModel):
    tool_name: str = Field(..., description="Name of the tool to use")
    reason_of_choice: str = Field(..., description="Reason for choosing the tool")

class AgentObservation(BaseModel):
    stop: bool = Field(..., description="True if the context is enough to answer the request else False")
    final_answer: str = Field(..., description="Final answer if the context is enough to answer the request")
    confidence: float = Field(..., description="Confidence score of the final answer")

class Agent(BaseModel):
    name: str = "Agent"
    model: str = "gpt-4o"
    instructions: Union[str, Callable[[], str]] = "You are a helpful agent."
    functions: List = []

class LLMResponse(BaseModel):
    tools: list[ActiveTool]
    message: str

class Task(BaseModel):
    context: Any
    input: str 
    output: LLMResponse

class Event(BaseModel):
    pass 