from src.models.lazy_vectorstore import LazyVectorStore
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from src.utils.retrieval import RerankRetriever
from src.models.lazy_llm import LazyMainLLM
from src.models.reranker import single_block_structured_reranker
from src.config import load_prompt_templates

custom_prompt_templates = load_prompt_templates()
lazyLLM = LazyMainLLM()
llm = lazyLLM.get_llm()

manager = LazyVectorStore()
vectorstore = manager.get_vectorstore()
embedding_model = manager.get_embedding_model()
Zhibo_Shannona_system_template = custom_prompt_templates.get('zhibo_shannona_prompt', {}).get('rag_system_prompt')

prompt = PromptTemplate(
    template=Zhibo_Shannona_system_template,
    input_variables=[ "question"]
)
custom_retriever = RerankRetriever(
    vectorstore=vectorstore,
    reranker=single_block_structured_reranker,
    top_k=5,
    rerank_k=2
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

    # print(prompt)
    # exit(0)
    query = "我叫田乐蒙"
    result = rag_qa_chain.invoke(query)


    print(result)

    query = "我叫什么名字"
    result = rag_qa_chain.invoke(query)
    print(result)