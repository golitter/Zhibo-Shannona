# 文件名：lazy_vectorstore.py

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

class LazyVectorStore:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, faiss_path="./faiss_index", embedding_model_name="./Models/BAAI-bge-large-zh-v1.5"):
        # from huggingface_hub import snapshot_download

        # snapshot_download(repo_id="BAAI/bge-large-zh-v1.5", local_dir="./Models/BAAI-bge-large-zh-v1.5", allow_patterns=["*.json", "*.bin", "*.txt"], force_download=True)

        if self._initialized:
            return
        self.faiss_path = faiss_path
        self.embedding_model_name = embedding_model_name
        self.vectorstore = None
        self.embedding_model = None
        self._initialized = True

    def get_embedding_model(self):
        if self.embedding_model is None:
            self.embedding_model = HuggingFaceEmbeddings(
                model_name=self.embedding_model_name,
                encode_kwargs={'normalize_embeddings': True}
            )
        return self.embedding_model

    def get_vectorstore(self):
        if self.vectorstore is None:
            embedding_model = self.get_embedding_model()
            self.vectorstore = FAISS.load_local(
                self.faiss_path,
                embeddings=embedding_model,
                allow_dangerous_deserialization=True
            )
        return self.vectorstore
