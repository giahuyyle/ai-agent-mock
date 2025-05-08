from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import chat


"""
CORSMiddleware:
- a mechanism that allows you to process requests and responses globally before
  they reach your route handlers or after they leave them
- useful for handling cross-origin requests, modifying headers, and other global
  tasks
- can be used to set up CORS (Cross-Origin Resource Sharing) policies
- CORS is a security feature implemented by web browsers to restrict web pages
  from making requests to a different domain than the one that served the web page
- CORS policies are defined by the server and specify which origins are allowed
  to access resources on the server
- CORS is important for web applications that need to interact with APIs or
  resources hosted on different domains
- CORS policies are defined by the server and specify which origins are allowed
  to access resources on the server
"""


app = FastAPI()

# Set up CORS middleware (allow front-end to connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (you can specify a list of allowed origins), should be configured to front-end URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Include the chat router
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])

"""
async def: Asynchronous function
- defines a coroutine that can be paused and resumed
- allow the program to perform other tasks while waiting for I/O operations
- requires await to pause execution
- does not block program while waiting
"""

@app.get("/")
# def root():
async def root():
    return {"message": "Hello, World! This is the backend for the chatbot."}