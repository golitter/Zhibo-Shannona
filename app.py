from fastapi import APIRouter, Request, FastAPI
from src.chat.chatbot import prompt_template
from src.chat.ragchatbot import rag_qa_chain
from src.chat.ragmemory import rag_chain_with_memory
from src.models.lazy_llm import LazyRerankLLM

lazy_rerank_llm = LazyRerankLLM()
llm = lazy_rerank_llm.get_llm()

LLM_Router = APIRouter()

@LLM_Router.get("/test/", tags=["测试"])
async def test():
    return {"status": "ok"}

@LLM_Router.post("/api/v1/chat/completions", tags=["llm_chat"], summary="普通大模型接口")
async def chat_completions(query: str):
    prompt = prompt_template.invoke({"text": query})
    result = llm.invoke(prompt)
    return {"response": result.content}

@LLM_Router.post("/api/v1/ragchat/completions", tags=["ragllm_chat"], summary="带RAG的大模型接口")
async def ragchat_completions(query: str):
    result = rag_qa_chain.invoke(query)
    return {"response": result['result']}


@LLM_Router.post("/api/v1/ragmemorychat/completions", tags=["ragmemoryllm_chat"], summary="带RAG、memory的大模型接口")
async def ragmemorychat_completions(query: str):
    result = rag_chain_with_memory.invoke(query)
    return {"response": result["answer"]}


app = FastAPI()
app.include_router(LLM_Router)

# 运行应用
if __name__ == "__main__":
    import uvicorn
    # uvicorn.run(app, host="0.0.0.0", port=8000)
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
