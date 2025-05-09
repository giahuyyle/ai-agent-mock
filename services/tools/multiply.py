from langchain.tools import Tool

def multiply_nums(s: str) -> str:
    "Multiply two numbers together"
    try:
        a, b = s.split(",")
        a = a.strip()
        b = b.strip()
        a = float(a)
        b = float(b)
        return f"{a} * {b} = {a * b}"
    except Exception as e:
        return f"Error: {str(e)}"
    

multiply_nums_tool = Tool(
    name="Multiply Numbers",
    func=multiply_nums,
    description="Get the multiplication of two numbers x and y. Provide the numbers in the format x, y.",
    return_direct=True,             # so that the result is returned directly to the user, instead of being checked by the agent
)