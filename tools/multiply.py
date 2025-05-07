from langchain.tools import Tool

def multiply_nums(input: str) -> str:
    "Multiply two numbers together"
    try:
        n1 = input.split("*")[0].strip()
        n2 = input.split("*")[1].strip()
        n1 = float(n1)
        n2 = float(n2)
        result = n1 * n2
        return f"{input} = {result}"
    except Exception as e:
        return "Format error. Please use x * y format."
    

multiply_nums_tool = Tool(
    name="Multiply Numbers",
    func=multiply_nums,
    description="Multiply two numbers together in form x * y",
    return_direct=True,             # so that the result is returned directly to the user, instead of being checked by the agent
)