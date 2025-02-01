from utils import ToolBuilder

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
    

calculator_tool = ToolBuilder(name="calculator", func=calculator, desc="Tool to perform math operation")


tool_registry = {
    'calculator': calculator_tool
}