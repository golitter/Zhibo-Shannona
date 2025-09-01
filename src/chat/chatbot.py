import getpass
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from lazy_loading.lazy_llm import LazyRerankLLM
from langchain_core.prompts import ChatPromptTemplate

# 加载环境变量
load_dotenv()

if not os.getenv('deep_seek_api_key'):
    os.environ['deep_seek_api_key'] = getpass.getpass('Enter your DeepSeek API key: ')


# pip install -U langchain-deepseek
lazy_rerank_llm = LazyRerankLLM()
llm = lazy_rerank_llm.get_llm()
# llm = init_chat_model(
#     model_provider='openai',
#     model='qwen-turbo-latest',
#     base_url='https://dashscope.aliyuncs.com/compatible-mode/v1',
#     api_key=os.getenv('DASHSCOPE_API_KEY'),
#     max_retries=3,
# )
def chat_with_llm(prompt):
    response = llm.invoke(prompt)
    return response.content
# answer = chat_with_llm("What is the capital of France?")
# print(f"Answer: {answer}")


system_template = """
你叫陕珂娜（Zhibot），是一个专注于陕西科技大学信息的智能助手。你以轻小说《魔女之旅》的主角——旅途中的魔女伊雷娜的口吻来回答问题。

你的语气轻松、优雅，略带一点俏皮与自信，却始终保持理性与智慧。就像一位陪伴旅人走过城市街巷的向导，你善于将复杂的现实问题，用清晰又富有韵味的语言娓娓道来。

{{不能使用虚构世界的魔法或幻想设定}}，而是专注于现实社会中的问题解答，例如高校政策、奖助学金、课程设置、就业信息、校园生活、社会实践、科研方向等。
"""


prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_template), ("user", "{text}")]
)
prompt = prompt_template.invoke({"text": "什么是陕西科技大学？"})
response = llm.invoke(prompt)
print(response.content)