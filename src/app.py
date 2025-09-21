import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.assistant.router import router as assistant_router
from src.retrieval.router import router as rag_router
from src.documents.router import router as documents_router
from src.auth.router import router as auth_router


app = FastAPI(title="RAG API", version="1.0.0")
app.include_router(assistant_router, prefix="/assistant", tags=["Assistant"])
app.include_router(rag_router, prefix="/rag", tags=["RAG"])
app.include_router(documents_router, prefix="/documents", tags=["Documents"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:3000",
    "http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "OK"}


if __name__ == "__main__":
    uvicorn.run("src.app:app", host="127.0.0.1", port=8000, reload=True)
