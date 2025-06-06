from lazy_loading.lazy_vectorstore import LazyVectorStore
from langchain.prompts import PromptTemplate
from rag.retrieval import RerankRetriever
from lazy_loading.lazy_llm import LazyMainLLM
from rag.reranker import single_block_structured_reranker
from utils.prompts import Abstract_Prompt, Zhibo_Shannona_Prompt
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationSummaryMemory
lazyLLM = LazyMainLLM()
llm = lazyLLM.get_llm()

manager = LazyVectorStore()
vectorstore = manager.get_vectorstore()
embedding_model = manager.get_embedding_model()
Zhibo_Shannona_system_template = Zhibo_Shannona_Prompt.memory_system_prompt

prompt = PromptTemplate(
    template=Zhibo_Shannona_system_template,
    input_variables=["chat_history", "question"]
)
custom_retriever = RerankRetriever(
    vectorstore=vectorstore,
    reranker=single_block_structured_reranker,
    top_k=30,
    rerank_k=10
)

abstract_prompt = PromptTemplate(
    template=Abstract_Prompt.system_prompt,
    input_variables=['summary', 'new_lines'],
)
memory = ConversationSummaryMemory(
    llm=llm,
    memory_key="chat_history",
    return_messages=True,
    prompt=abstract_prompt,
)
rag_chain_with_memory = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=custom_retriever,
    memory=memory,
    combine_docs_chain_kwargs={"prompt": prompt},
)

def clear_history():
    rag_chain_with_memory.memory.clear()

if __name__ == "__main__":
    query = "我叫田乐蒙"

    result = rag_chain_with_memory.invoke(query)
    print(result)
    # print(get_answer(query))
    # exit(0)
    query = "我叫什么名字"
    result = rag_chain_with_memory.invoke(query)
    print(result)

    query = "我上一个问答中说了我的名字"
    result = rag_chain_with_memory.invoke(query)
    print(result)