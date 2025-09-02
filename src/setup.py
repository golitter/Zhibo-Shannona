import configparser
import os
from src.utils.pdf2markdown import pdfs_to_markdown, get_all_files
from src.utils.tovedb import embedding_txt2vec
from src.config import load_config
from src.models.embedding_model import load_bge_large_zh_v15
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

def setup():

    print("[1] BAAI/bge-large-zh-v1.5 安装")
    load_bge_large_zh_v15()

    print("[2] PDF 转 Markdown")
    config = load_config()
    pdf_main_directory = config.get("data_process", "pdf_dir_path")
    print('正在查找PDF文件...')
    pdf_files = get_all_files(pdf_main_directory)
    print(f'找到{len(pdf_files)}个PDF文件')
    markdown_target_directory = config.get("data_process", "markdown_dir_path")
    pdfs_to_markdown(pdf_files, markdown_target_directory)

    print("[3] Markdown 转 Vector")
    embedding_txt2vec()

    print("[4] LLM Chat 初始化")
    from src.chat.chatbot import prompt_template
    from src.chat.ragchatbot import rag_qa_chain
    from src.chat.ragmemory import rag_chain_with_memory

if __name__ == "__main__":
    setup()