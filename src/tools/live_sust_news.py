import requests
from bs4 import BeautifulSoup

import requests
from bs4 import BeautifulSoup
import re

def get_latest_school_news() -> str:
    """
    爬取陕西科技大学主页最新的新闻信息，并提取中文内容。
    返回去重后的中文新闻内容。
    """
    url = "https://ulster.sust.edu.cn/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'

        if response.status_code != 200:
            return f"请求失败，状态码: {response.status_code}"

        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        for tag in soup(['script', 'style']):
            tag.decompose()

        full_text = soup.get_text(separator='\n')

        chinese_texts = re.findall(r'[\u4e00-\u9fa5，。！？、《》“”：（）【】]+', full_text)

        unique_lines = list(set(chinese_texts))
        result = '\n'.join(unique_lines)

        return result.strip() if result else "未找到中文新闻内容。"

    except Exception as e:
        return f"获取新闻失败：{str(e)}"


if __name__ == "__main__":
    news_content = get_latest_school_news()
    print(news_content)
