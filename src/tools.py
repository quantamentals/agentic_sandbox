import datetime
import wikipedia
from .utils import ToolBuilder

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

def query_wiki(query):
    try:
        res = wikipedia.page(query)
        content = res.content[:1000]
        print('WIKI content: ',content)
    except Exception as e:
        return (f"Search query: {query} is invalid or not found, try another query")
    
    return content

def current_date(param):
    """
    Returns the current date as a string.

    Args:
        param: Arbitrary parameter (not used)

    Returns:
        str: The current date in YYYY-MM-DD format
    """
    return datetime.date.today().strftime("%Y-%m-%d")

calculator_tool = ToolBuilder(name="calculator", func=calculator, desc="Tool to perform math operation")

wiki_query_tool = ToolBuilder(name="wiki_query", func=query_wiki, desc="Too query for a wikipedia page")

current_date_tool = ToolBuilder(name="Date_of_today", func=current_date, desc="The current date")

tool_registry = {
    'calculator': calculator_tool,
    'wiki_query': wiki_query_tool,
    'Date_of_today':current_date_tool
}
