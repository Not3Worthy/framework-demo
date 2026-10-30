import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sentence_transformers import SentenceTransformer
#from pgvector.sqlalchemy import CosineDistance
from framework_demo.database import get_db
from framework_demo.model.diagnostic_services import *

router = APIRouter(prefix="/diagnostic", tags=["Diagnostic RAG Copilot"])

# Load the lightweight local embedding model
encoder = SentenceTransformer("all-MiniLM-L6-v2")

class DiagnosticQueryRequest(BaseModel):
    query: str
    top_k: int = 2  # Number of relevant service manual snippets to retrieve

class DiagnosticQueryResponse(BaseModel):
    query: str
    retrieved_manuals: list[str]
    ai_recommendation: str

@router.post("/rag", response_model=DiagnosticQueryResponse)
async def diagnostic_rag_copilot(
    payload: DiagnosticQueryRequest,
    db: AsyncSession = Depends(get_db)
):
    # 1. Convert technician query into a 384-dimension vector embedding
    query_vector = encoder.encode(payload.query).tolist()

    # 2. Perform lightning-fast cosine similarity search using pgvector
    stmt = (
        select(ServiceManual)
        .order_by(ServiceManual.embedding.cosine_distance(query_vector))
        .limit(payload.top_k)
    )
    result = await db.execute(stmt)
    matches = result.scalars().all()

    if not matches:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="No matching service manuals found for this query."
        )

    # 3. Assemble the retrieved context chunks from the database
    context_texts = []
    retrieved_titles = []
    for manual in matches:
        retrieved_titles.append(manual.title)
        context_texts.append(
            f"Manual Title: {manual.title}\n"
            f"DTC Code: {manual.dtc_code}\n"
            f"Category: {manual.category}\n"
            f"Procedure: {manual.content}"
        )
    
    combined_context = "\n\n---\n\n".join(context_texts)

    # 4. Construct the prompt for your local Ollama LLM
    prompt = f"""You are an expert Ford automotive diagnostic copilot. Use the following official service manual procedures to answer the technician's question accurately and safely. Do not extrapolate outside the provided manual data.

Official Service Manual References:
{combined_context}

Technician Diagnostic Query: {payload.query}

Provide a clear, step-by-step diagnostic recommendation based strictly on the retrieved service manual references above:"""

    # 5. Send request to local Ollama instance (ensure Ollama is running with `ollama run llama3` or `mistral`)
    ollama_url = "http://localhost:11434/api/generate"
    ollama_payload = {
        "model": "llama3",  # Or your preferred local model (e.g., mistral, phi3)
        "prompt": prompt,
        "stream": False
    }

    async with httpx.AsyncClient(timeout=45.0) as client:
        try:
            response = await client.post(ollama_url, json=ollama_payload)
            response.raise_for_status()
            ollama_data = response.json()
            ai_response = ollama_data.get("response", "No response generated from local LLM.")
        except httpx.HTTPError as e:
            ai_response = (
                f"Error communicating with local Ollama instance at {ollama_url}. "
                f"Ensure Ollama is running locally. Details: {str(e)}"
            )

    return DiagnosticQueryResponse(
        query=payload.query,
        retrieved_manuals=retrieved_titles,
        ai_recommendation=ai_response
    )