from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from document_processor import DocumentProcessor
from vector_store import VectorStoreManager
from chat_engine import ChatEngine
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Research Copilot API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
lecturas_path = r"C:\Users\vgonzales\Documents\Tarea 1 - Prompt\Lecturas"
processor = DocumentProcessor(lecturas_path)
v_store_manager = VectorStoreManager()
chat_engine = None

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    answer: str
    sources: List[dict]

@app.get("/status")
async def get_status():
    return {"status": "online", "indexed": chat_engine is not None}

@app.post("/initialize")
async def initialize():
    global chat_engine
    try:
        docs = processor.load_documents()
        v_store = v_store_manager.create_or_load_store(docs)
        chat_engine = ChatEngine(v_store)
        return {"status": "success", "message": f"Indexed {len(docs)} documents"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    global chat_engine
    if not chat_engine:
        # Try to auto-initialize
        try:
            v_store = v_store_manager.create_or_load_store([])
            chat_engine = ChatEngine(v_store)
        except:
            raise HTTPException(status_code=400, detail="Engine not initialized. Please call /initialize first.")
    
    try:
        result = chat_engine.ask(request.message)
        return ChatResponse(answer=result["answer"], sources=result["sources"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/documents")
async def get_documents():
    return processor.documents

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
