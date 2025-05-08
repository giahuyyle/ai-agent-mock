"""
CHAT ROUTE:
1. Accept POST requests
2. Forward to LangChain agent
3. Return the response to front-end
"""

from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from agent import agent
from models.chat import ChatRequest, ChatResponse

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        agent_reply = agent.invoke(request.message)
        return {"response": agent_reply["output"]}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing the request: {str(e)}",
        )