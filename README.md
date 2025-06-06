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

![img](images/d274fccb1720b885a48a14a4c2fab9fd.png)



webUI:

![img](images/2e2192e0e8ee9c5f599e4a888e805de7.png)



**项目具体实现**：

- 使用 docling 库实现 PDF 批量转换为 Markdown 文本，基于递归式文本拆分对文档进行分块处理；采用 BAAI-bge-large-zh-v1.5 预训练模型生成文本向量，构建 Faiss 本地向量索引，支持高效语义检索。 
- 设计提示词与结构化输出约束，实现查询与文档块的语义相关性评分模型。重写 RerankRetriever 类， 融合向量召回与大模型重排序机制，采用多线程并发评分，选取高相关文档块用于下游 RAG 推理。 
- 基于大模型实现模型的历史对话精简和记忆化；优化主模型的提示词进行模仿轻小说《魔女之旅》中 伊雷娜的对话风格。使用 gradio 的 ChatInterface 模块实现简易聊天界面，最终得到具有伊雷娜风格的 校园事务交互系统。 
- 对项目所用模型采用单例模式的模块级懒加载和缓存机制，避免重复加载模型带来的冗余资源消耗。