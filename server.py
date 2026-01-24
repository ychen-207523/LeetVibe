
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
# The graph import must happen AFTER load_dotenv()
from graph import app

# Initialize API
server = FastAPI()
server.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins (simplest for development)
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods
    allow_headers=["*"], # Allows all headers
)

# Define the Data Model (What React sends us)
class ChatRequest(BaseModel):
    message: str
    thread_id: str = "user_1"  # Keeps track of ONE conversation


@server.post("/chat")
def chat_endpoint(req: ChatRequest):
    """
    Receives a message from React, runs the Agent, returns the response.
    """
    # 1. Prepare inputs for the Graph
    inputs = {
        "messages": [HumanMessage(content=req.message)]
    }

    # 2. Config for memory (so it remembers previous chats)
    config = {"configurable": {"thread_id": req.thread_id}}

    # 3. Run the Graph
    # This runs Manager -> Interviewer -> Grader automatically
    result = app.invoke(inputs, config=config)

    # 4. Extract the response
    last_msg = result["messages"][-1].content

    # Check if the Grader added any specific flags (optional)
    problem_desc = result.get("problem_description", "")

    return {
        "response": last_msg,
        "problem": problem_desc
    }


if __name__ == "__main__":
    import uvicorn

    # Run on port 8000
    print("🚀 Server running on http://localhost:8000")
    uvicorn.run(server, host="0.0.0.0", port=8000)