from lazy_loading.lazy_vectorstore import LazyVectorStore
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from rag.retrieval import RerankRetriever
from lazy_loading.lazy_llm import LazyMainLLM
from rag.reranker import single_block_structured_reranker
from utils.prompts import Zhibo_Shannona_Prompt

lazyLLM = LazyMainLLM()
llm = lazyLLM.get_llm()

manager = LazyVectorStore()
vectorstore = manager.get_vectorstore()
embedding_model = manager.get_embedding_model()
Zhibo_Shannona_system_template = Zhibo_Shannona_Prompt.system_prompt

prompt = PromptTemplate(
    template=Zhibo_Shannona_system_template,
    input_variables=[ "question"]
)
custom_retriever = RerankRetriever(
    vectorstore=vectorstore,
    reranker=single_block_structured_reranker,
    top_k=30,
    rerank_k=10
)
rag_qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=custom_retriever,
    chain_type_kwargs={"prompt": prompt}
)
if __name__ == "__main__":
    # query = "陕西科技大学的研究生奖学金有哪些？"
    # print(f"开始回答问题：{query}")

    # result = rag_qa_chain.invoke(query)
    # print(result)

    query = "我叫田乐蒙"
    result = rag_qa_chain.invoke(query)
    print(result)

    query = "我叫什么名字"
    result = rag_qa_chain.invoke(query)
    print(result)