from dotenv import load_dotenv
import os
from openai import OpenAI
from prompt_schema import task_prompt

# 加载.env文件
load_dotenv()

# 获取环境变量
API_KEY = os.getenv('API_KEY')
# print(API_KEY)

client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com")
def get_message_dsr1() -> str:
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": task_prompt},
        ],
        stream=False
    )

    # print(response.choices[0].message.content)
    return response.choices[0].message.content
    