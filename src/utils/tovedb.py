import os
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from langchain_huggingface import HuggingFaceEmbeddings
from src.config import load_config
def get_all_files(path:str) -> list[str]:
    # print(path)
    # 列出路径下的所有文件和目录
    items = os.listdir(path)
    # 筛选出所有以.md结尾的文件
    pdf_files = [os.path.join(path, item) for item in items if os.path.isfile(os.path.join(path, item)) and item.lower().endswith('.md')]
    return pdf_files

config = load_config()
def load_and_split_markdowns(directory):
    all_docs = []
    file_paths = get_all_files(directory)
    print(f"找到 {len(file_paths)} 个 Markdown 文件。")
    for filepath in file_paths:
        loader = TextLoader(filepath, encoding="utf-8")
        docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        split_docs = text_splitter.split_documents(docs)
        print(f"文件 {filepath} 被分割成 {len(split_docs)} 个文档块。")
        file_name = os.path.basename(filepath)
        # 加入元数据
        for idx, doc in enumerate(split_docs):
            meta = dict(doc.metadata)
            meta["source"] = file_name
            meta["block_pos"] = idx
            enhanced_doc = Document(page_content=doc.page_content, metadata=meta)
            all_docs.append(enhanced_doc)

    return all_docs

def embedding_txt2vec():
    directory = config.get("data_process", "markdown_dir_path")
    documents = load_and_split_markdowns(directory)
    print(f"总共加载并分块得到 {len(documents)} 个文档块")

    embedding_model = LazyVectorStore().get_embedding_model()
    vectorstore = FAISS.from_documents(documents, embedding_model)

    # 保存索引，方便后续加载
    faiss_path = config.get("vectorstore", "faiss_path")
    vectorstore.save_local(faiss_path)

    print("所有文档块已成功插入 Faiss 向量数据库。")

if __name__ == "__main__":
    embedding_txt2vec()
