import streamlit as st
from ragflow_sdk import RAGFlow
from dotenv import load_dotenv
import os

load_dotenv()
RAGFlow_API_KEY = os.getenv("RAGFLOW_API_KEY")
BASE_URL = os.getenv("BASE_URL")

rag_object = RAGFlow(api_key=RAGFlow_API_KEY, base_url=BASE_URL)
assistant = rag_object.list_chats(name="智博陕珂娜")
assistant = assistant[0]
session = assistant.create_session()    

# 初始化RAGFlow对象
rag_object = RAGFlow(api_key=RAGFlow_API_KEY, base_url=BASE_URL)
assistant = rag_object.list_chats(name="智博陕珂娜")[0]

# 创建会话
session = assistant.create_session()

col1, col2, col3 = st.columns([1, 5, 1])

with col1:
    st.image("Shannona.png", width=60)  # 替换为头像路径，调整宽度以适配布局

with col2:
    st.markdown("<h1 style='font-size: 2em; line-height:1.6;'>智博陕珂娜</h1>", unsafe_allow_html=True)

with col3:
    if st.button("刷新", key="refresh"):
        session = assistant.create_session()
        st.session_state["input"] = ""
        st.balloons()


# 创建一个文本输入框，用于用户输入问题
question = st.text_input("你好！我是陕珂娜，有任何校园事务问题都可以向我咨询！", key="input")

# 当用户输入问题并按下Enter键时
if question:
    # 创建一个用于显示回答的文本区域
    answer_area = st.empty()

    # 初始化一个空字符串来存储之前的回答内容
    cont = ""
    # 假设session.ask是一个生成器函数，循环获取回答并实时显示
    for ans in session.ask(question, stream=True):
        # 更新回答内容，只显示新的一部分
        answer_area.markdown(ans.content[len(cont):])
        # 更新cont为最新的完整回答内容
        cont = ans.content
    # 清空之前的回答内容
    answer_area.empty()
    # 显示最后一次的回答内容
    st.markdown(cont)