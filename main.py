from fastapi import FastAPI, HTTPException
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from pydantic import BaseModel
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()
llm = ChatOllama(model="qwen3:1.7b")

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat")
async def chat(chat_request: ChatRequest) -> ChatResponse:
    try:
        logging.info(f"Received message: {chat_request.message}")
        res = llm.invoke([HumanMessage(content=chat_request.message)])
        return {"response": res.content}
    except Exception as e:
        logging.error(f"Error processing message: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)