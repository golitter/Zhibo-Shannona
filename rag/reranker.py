from lazy_loading.lazy_llm import LazyRerankLLM
from langchain_core.prompts import ChatPromptTemplate
from utils.prompts import RerankingPrompt
lazy_rerank_llm = LazyRerankLLM()
llm = lazy_rerank_llm.get_llm()

system_prompt_rerank_single_block = RerankingPrompt.system_prompt_rerank_single_block
prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_prompt_rerank_single_block), ("user", "你收到的查询和文本块如下：\n\
查询：{query}\n\
文本块：{text_block}\n\
由于你是qwen模型，不支持结构化输出，所以请你最后只用给出以下json数据 'score': 0-10之间的数字，表示查询和文本块的相关性分数，0表示完全无关，10表示完全相关。请不要输出其他内容。")],
)
# prompt = prompt_template.invoke({"query": "你好吗？", "text_block": "我很好，谢谢！"})
# print(prompt)

from typing_extensions import Annotated, TypedDict

class Score(TypedDict):
    """Fruit to tell user."""

    score: Annotated[float,..., "查询和文本块的相关性分数，0-10之间，0表示完全无关，10表示完全相关。"]
structured_llm = llm.with_structured_output(Score)


single_block_structured_reranker = prompt_template | structured_llm
if __name__ == "__main__":
    # Example usage
    reps = single_block_structured_reranker.invoke({"query": "你好吗？", "text_block": "我很好，谢谢！"})
    print(reps)

    reps = single_block_structured_reranker.invoke({"query": "你好吗？", "text_block": "我是伊雷娜"})
    print(reps)
