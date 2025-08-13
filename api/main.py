from fastapi import FastAPI
from api.routes.rag import router

app = FastAPI(title="RAG API", version="1.0.0")
app.include_router(router, prefix="/api/rag", tags=["RAG"])

# @app.get("/")
# async def root():
#     return {"message": "Welcome to RAG API"}