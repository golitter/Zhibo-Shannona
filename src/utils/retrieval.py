from src.models.lazy_vectorstore import LazyVectorStore
from src.models.reranker import single_block_structured_reranker
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm


from langchain.schema import BaseRetriever
from langchain_core.documents import Document
from typing import Any, List
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

########### 类实现 ###########

class RerankRetriever(BaseRetriever):
    vectorstore: Any 
    reranker: Any
    top_k: int = 5
    rerank_k: int = 2
    # def __init__(self, vectorstore, reranker, top_k=5, rerank_k=2):
    #     self.vectorstore = vectorstore
    #     self.reranker = reranker
    #     self.top_k = top_k
    #     self.rerank_k = rerank_k

    def _get_relevant_documents(self, query: str) -> List[Document]:
        # 第一步：向量召回
        docs = self.vectorstore.similarity_search(query, k=self.top_k)
        
        # 第二步：多线程 rerank
        with ThreadPoolExecutor() as executor:
            futures_to_doc = {}
            for doc in docs:
                future = executor.submit(self.reranker.invoke, {
                    "query": query,
                    "text_block": doc.page_content
                })
                futures_to_doc[future] = doc

            results = []
            for future in tqdm(as_completed(futures_to_doc), total=len(futures_to_doc), desc="Reranking documents"):
                result = future.result()
                results.append({
                    'doc': futures_to_doc[future],
                    'score': result['score']
                })

        sorted_results = sorted(
            results,
            key=lambda x: (x['score'], len(x['doc'].page_content)),
            reverse=True
        )

        top_docs = [item['doc'] for item in sorted_results[:self.rerank_k]]
        # print(sorted_results[:self.rerank_k])
        return top_docs

########### 函数实现 ###########
manager = LazyVectorStore()
vectorstore = manager.get_vectorstore()
embedding_model = manager.get_embedding_model()

def retrieve_relevant_docs(query, top_k=5):
    docs = vectorstore.similarity_search(query, k=top_k)
    return docs

def rerank_retrieve_relevant_docs(query:str, docs:list[Document], top_k=5, rerank_k=2):
    with ThreadPoolExecutor() as executor:
        futures_to_doc = {}
        for doc in docs:
            future = executor.submit(single_block_structured_reranker.invoke, {"query": query, "text_block": doc.page_content})
            futures_to_doc[future] = doc

        results = []
        for future in tqdm(as_completed(futures_to_doc), total=len(futures_to_doc), desc="Reranking documents"):
            result = future.result()
            results.append({'doc': futures_to_doc[future], 'score': result['score']})
    sorted_results = sorted(
        results,
        key=lambda x: (x['score'], len(x['doc'].page_content)),
        reverse=True
    )
    print(sorted_results)
    return sorted_results[:rerank_k]

if __name__ == "__main__":
    query = "陕西科技大学好吗"
    docs = retrieve_relevant_docs(query)
    rerank_retrieve_relevant_docs(query, docs)
