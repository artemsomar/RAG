from fastapi import FastAPI
import uvicorn
from app.routers.rag_router import router 

app = FastAPI(title="RAG API", version="1.0.0")
app.include_router(router, prefix="/api/rag", tags=["RAG"])

# @app.get("/")
# async def root():
#     return {"message": "Welcome to RAG API"}
if __name__ == '__main__':
    uvicorn.run("src.app:app", host="127.0.0.1", port=8000, reload=True)