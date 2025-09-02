import getpass
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from src.models.lazy_llm import LazyRerankLLM
from langchain_core.prompts import ChatPromptTemplate
from src.config import load_prompt_templates
custom_prompt_templates = load_prompt_templates()

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


system_template = custom_prompt_templates.get('zhibo_shannona_prompt', {}).get('naive_system_prompt')



prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_template), ("user", "{text}")]
)
if __name__ == "__main__":
    prompt = prompt_template.invoke({"text": "什么是陕西科技大学？"})
    response = llm.invoke(prompt)
    print(response.content)