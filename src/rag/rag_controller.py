from src.rag.rag_methods import BM25, SemanticSearch, HybridSearch


class RagController:
    def __init__(self, df):
            self.df = df
            self.__instances = {}

            self.methods = {
                "bm25": self.__get_bm25,
                "semantic": self.__get_semantic,
                "hybrid": self.__get_hybrid
            }

    def search_best(self, query: str, method: str):
        method = method.lower()
        if method not in self.methods:
            raise ValueError(f"Unknown method '{method}'. "
                             f"Available: {list(self.methods.keys())}")
        
        return self.methods[method]().search_best(query)

    def __get_bm25(self):
        if "bm25" not in self.__instances:
            self.__instances["bm25"] = BM25(self.df)
            print("Created BM25")
        return self.__instances["bm25"]

    def __get_semantic(self):
        if "semantic" not in self.__instances:
            self.__instances["semantic"] = SemanticSearch(self.df)
            print("Created SS")
        return self.__instances["semantic"]

    def __get_hybrid(self):
        if "hybrid" not in self.__instances:
            self.__instances["hybrid"] = HybridSearch(self.df)
            print("Created Hybrid")
        return self.__instances["hybrid"]

    
