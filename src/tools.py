import datetime
import wikipedia
from .utils import ToolBuilder

def calculator(operation:str, a, b):
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

def query_wiki(query):
    try:
        res = wikipedia.page(query)
        content = res.content
    except Exception as e:
        return (f"Search query: {query} is invalid or not found, try another query")
    
    return content[:1000]

def current_datetime():
    return datetime.date.today()

calculator_tool = ToolBuilder(name="calculator", func=calculator, desc="Tool to perform math operation")

wiki_query_tool = ToolBuilder(name="wiki_query", func=query_wiki, desc="Too query for a wikipedia page")

current_datetime_tool = ToolBuilder(name="current_datetime", func=current_datetime, desc="The current datetime")

tool_registry = {
    'calculator': calculator_tool,
    'wiki_query': wiki_query_tool,
    'current_datetime':current_datetime_tool
}
