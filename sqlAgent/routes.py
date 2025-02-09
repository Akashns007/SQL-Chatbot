from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services import process_query
from fastapi.responses import StreamingResponse
from typing import AsyncIterable

router = APIRouter()

# Health Check
@router.get("/ping")
def ping():
    return {"message": "Server is running"}

# Request Model
class QueryRequest(BaseModel):
    question: str

# Streaming generator
async def stream_response(question: str) -> AsyncIterable[str]:
    try:
        async for chunk in process_query(question):
            yield chunk
    except Exception as e:
        yield f"Error: {str(e)}"

# Query Endpoint (Streaming)
@router.post("/query")
async def query_database(request: QueryRequest):
    return StreamingResponse(stream_response(request.question), media_type="text/plain")

# Chat Endpoint (Streaming)
@router.post("/chat")
async def chat_with_agent(request: QueryRequest):
    return StreamingResponse(stream_response(request.question), media_type="text/plain")
