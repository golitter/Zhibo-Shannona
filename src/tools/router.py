from src.tools.live_sust_news import get_latest_school_news as get_school_news
from langchain.tools import tool

@tool
def get_latest_school_news() -> str:
    """
    用于回答用户关于陕西科技大学官网最新新闻的请求。
    """
    return get_school_news()

def load_tools():
    tools = [get_latest_school_news]
    return tools
