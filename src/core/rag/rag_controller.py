from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Document
from src.dataset_loader import DatasetLoader
from src.core.rag.rag_methods.bm25_search import BM25
from src.core.rag.rag_methods.semantic_search import SemanticSearch
from src.core.rag.rag_methods.hybrid_search import HybridSearch


class RagController:

    def __init__(self):
        self.__instances = {}
        self.methods = {
            "bm25": self.__get_bm25,
            "semantic": self.__get_semantic,
            "hybrid": self.__get_hybrid
        }


    async def search_best(
            self,
            query: str,
            session: AsyncSession,
            best_num: int = 3,
            method: str = "semantic"
    ):
        method = method.lower()
        if method not in self.methods:
            raise ValueError(f"Unknown method '{method}'. "
                             f"Available: {list(self.methods.keys())}")

        documents = await session.execute(select(Document))
        documents = documents.scalars().all()
        return await self.methods[method]().search_best(query, documents, session, best_num)


    def __get_bm25(self):
        if "bm25" not in self.__instances:
            self.__instances["bm25"] = BM25()
            print("Created BM25")
        return self.__instances["bm25"]


    def __get_semantic(self):
        if "semantic" not in self.__instances:
            self.__instances["semantic"] = SemanticSearch()
            print("Created SS")
        return self.__instances["semantic"]


    def __get_hybrid(self):
        if "hybrid" not in self.__instances:
            self.__instances["hybrid"] = HybridSearch()
            print("Created Hybrid")
        return self.__instances["hybrid"]

    
