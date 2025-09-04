from src.models.lazy_vectorstore import LazyVectorStore
from langchain.prompts import PromptTemplate
from src.utils.retrieval import RerankRetriever
from src.models.lazy_llm import LazyMainLLM
from src.models.reranker import single_block_structured_reranker
from langchain.chains import ConversationalRetrievalChain, LLMChain
from langchain.memory import ConversationSummaryMemory
from src.config import load_prompt_templates

custom_prompt_templates = load_prompt_templates()

lazyLLM = LazyMainLLM()
llm = lazyLLM.get_llm()

manager = LazyVectorStore()
vectorstore = manager.get_vectorstore()
embedding_model = manager.get_embedding_model()
Zhibo_Shannona_system_template = custom_prompt_templates.get('zhibo_shannona_prompt', {}).get('rag_memory_system_prompt')


## RerankRetriever 
custom_retriever = RerankRetriever(
    vectorstore=vectorstore,
    reranker=single_block_structured_reranker,
    top_k=5,
    rerank_k=2
)

# 摘要总结 llm
abstract_prompt = PromptTemplate(
    template=custom_prompt_templates.get('abstract_prompt', {}).get('system_prompt'),
    input_variables=['summary', 'new_lines'],
)
memory = ConversationSummaryMemory(
    llm=llm,
    memory_key="chat_history",
    return_messages=True,
    prompt=abstract_prompt,
)


## JudgeOfRetriever
# 判断query是否需要进行文本检索
decision_rerank_prompt = PromptTemplate(
    template=custom_prompt_templates.get('reranking_prompt', {}).get('decision_rerank_prompt'),
    input_variables=["query"],
)
decision_rerank_chain = LLMChain(llm=llm, prompt=decision_rerank_prompt)

class QueryOnlyConversationalRetrievalChain(ConversationalRetrievalChain):
    def _get_docs(self, question: str, chat_history: list):
        decision = decision_rerank_chain.invoke({"query": question})
        print(decision)
        if "YES" in decision["text"].strip().upper():
            return self.retriever.get_relevant_documents(question)
        else:
            return []

prompt = PromptTemplate(
    template=Zhibo_Shannona_system_template,
    input_variables=["chat_history", "question"]
)
rag_chain_with_memory = QueryOnlyConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=custom_retriever,
    memory=memory,
    combine_docs_chain_kwargs={"prompt": prompt},
)

def clear_history():
    rag_chain_with_memory.memory.clear()

if __name__ == "__main__":
    # print(Zhibo_Shannona_system_template)
    # print(abstract_prompt)
    # exit(0)
    query = "什么是推免"

    result = rag_chain_with_memory.invoke(query)
    print(result)

    exit(0)
    # print(get_answer(query))
    # exit(0)
    query = "我叫什么名字"
    result = rag_chain_with_memory.invoke(query)
    print(result)

    query = "我上一个问答中说了我的名字"
    result = rag_chain_with_memory.invoke(query)
    print(result)