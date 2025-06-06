import gradio as gr
from ragmemory import rag_chain_with_memory


def chat(message, history):
    # 将历史消息格式化为模型的输入格式
    formatted_history = []
    for user_msg, bot_msg in history:
        formatted_history.append(user_msg)
        formatted_history.append(bot_msg)

    # 调用模型生成响应
    response = rag_chain_with_memory.invoke(message)
    return {'text':response['answer']}


# 创建 ChatInterface
demo = gr.ChatInterface(
    fn=chat,
    title="智博陕珂娜（Zhibo-Shannona） RAG智能助手",
    description="与智能对话系统进行交互",
    examples=[["我叫田乐蒙"], ["我叫什么名字"], ["我上一个问答中说了我的名字"]]
)

# 启动 Gradio 应用
demo.launch()
