from fastapi import FastAPI, HTTPException, Request
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from pydantic import BaseModel
import logging
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
import time
from collections import defaultdict

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

app = FastAPI()
llm = ChatOllama(model="qwen3:1.7b")

rate_limit_store = defaultdict(list)
RATE_LIMIT_REQUESTS = 10
RATE_LIMIT_WINDOW = 60

def check_rate_limit(client_ip: str) -> bool:
    now = time.time()
    
    rate_limit_store[client_ip] = [
        req_time for req_time in rate_limit_store[client_ip]
        if now - req_time < RATE_LIMIT_WINDOW
    ]
    
    if len(rate_limit_store[client_ip]) >= RATE_LIMIT_REQUESTS:
        return False
    
    rate_limit_store[client_ip].append(now)
    return True

class ChatRequest(BaseModel):
    message: str = Field(...,min_length=1, max_length=1000)

    @field_validator('message')
    def validate_message(cls, v):
        if not v.strip():
            raise ValueError('Message cannot be empty or whitespace')
        return v.strip()

class ChatResponse(BaseModel):
    response: str
    timestamp: str
    model: str = "qwen3:1.7b"

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat")
async def chat(chat_request: ChatRequest, request: Request) -> ChatResponse:

    client_ip = request.client.host
    if not check_rate_limit(client_ip):
        logger.warning(f"Rate limit exceeded for IP: {client_ip}")
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again later.")

    try:
        logger.info(f"Received message: {chat_request.message}")
        res = llm.invoke([HumanMessage(content=chat_request.message)])
        logger.info("Response generated successfully")
        return ChatResponse(
            response=res.content,
            timestamp= datetime.now().isoformat(),
        )
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)