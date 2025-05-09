from langchain.agents import initialize_agent, AgentType
from langchain_community.llms import HuggingFaceHub
from langchain.memory import ConversationBufferMemory
from openai import OpenAI
from services.tools.multiply import multiply_nums_tool
from services.tools.weather import weather_by_address_tool, weather_by_coordinates_tool
from custom_llm import HFClientLLM
from dotenv import load_dotenv
import os

load_dotenv()

# Updated method using HuggingFaceEndpoint instead of HuggingFaceHub
from langchain_huggingface import HuggingFaceEndpoint

'''
llm = HuggingFaceEndpoint(
    endpoint_url=f"https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta",
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN2"),
    temperature=0.7,
    max_new_tokens=512,
)
'''

from langchain.chat_models import ChatOpenAI
# Using OpenAI's GPT-4o-mini model

llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name="gpt-4o-mini",
    temperature=0,
)         

# Alternative approach if you want to keep using HuggingFaceHub
# from langchain_huggingface import ChatHuggingFace
# llm = ChatHuggingFace(model_name="HuggingFaceH4/zephyr-7b-beta", 
#                      model_kwargs={"temperature": 0.7, "max_new_tokens": 512})

#llm = HFClientLLM()

tools = [
    multiply_nums_tool,
    weather_by_coordinates_tool,
    weather_by_address_tool
]

memory = ConversationBufferMemory(memory_key="chat_history")

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent_type=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    # agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    memory=memory
)

'''
DIFFERENCES BETWEEN AGENT TYPES

1. ZERO_SHOT_REACT_DESCRIPTION:
- focused on reasoning step-by-step, without *prior example*
- use "think-act" approach, where it reasons to choose which tool is most suitable
- more explicit reasoning process
- no prior examples to do well -> ZERO SHOT

2. CONVERSATIONAL_REACT_DESCRIPTION:
- designed for conversational interactions
- maintains history and context
- better at natural dialogue and memorizing previous exchanges
- more suitable for chatbots (hence the more user-friendly responses)

'''