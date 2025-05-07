from langchain.tools import tool

@tool
def multiply_nums(input: str) -> str:
    """Multiply two numbers together in form x * y"""
    try:
        result = eval(input)
        return f"{input} = {result}"
    except:
        return "Format error. Please use x * y format."