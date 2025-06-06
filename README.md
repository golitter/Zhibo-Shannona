# 智博陕珂娜（Zhibo-Shannona） RAG智能助手

1. 下载嵌入模型`BAAI/bge-large-zh-v1.5`到`./Models/`内

```python
from huggingface_hub import snapshot_download

snapshot_download(repo_id="BAAI/bge-large-zh-v1.5", local_dir="./Models/BAAI-bge-large-zh-v1.5", allow_patterns=["*.json", "*.bin", "*.txt"], force_download=True)
```

2. 设置`.env`中的密钥。本项目使用deepseek-r1和qwen-max

```.env
deep_seek_api_key=<ds_api_key>
DASHSCOPE_API_KEY=<qwen_api_key>
```



- `chatbot.py`：普通chat
- `ragchatbot.py`：带RAG的chat
- `ragmenory.py`：带RAG和上下文记忆的chat
- `webUI.py`：简易UI界面

- `faiss_index/`：向量索引本地存储
- `lazy_loading/`：大模型、嵌入模型、向量索引的懒加载模块
- `rag/`：RAG实现
- `tools/`：function calling，项目未用
- `utils/`：pdf转markdown、prompts和分块并进行嵌入后以faiss形式保存本地

