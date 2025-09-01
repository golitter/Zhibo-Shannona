# lazy_llm.py

import os
from getpass import getpass
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

class LazyMainLLM:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(
        self,
        model_provider='deepseek',
        model='deepseek-chat',
        base_url='https://api.deepseek.com/v1/chat/completions',
        env_key='deep_seek_api_key',
        max_retries=3,
    ):
        if self._initialized:
            return

        self.model_provider = model_provider
        self.model = model
        self.base_url = base_url
        self.env_key = env_key
        self.max_retries = max_retries
        self.llm = None
        self._initialized = True

    def get_llm(self):
        if self.llm is None:
            print(f'初始化 MainLLM')
            load_dotenv()
            api_key = os.getenv(self.env_key)
            if not api_key:
                api_key = getpass(f"Enter your {self.model_provider} API key: ")
                os.environ[self.env_key] = api_key

            if self.model_provider == 'deepseek':
                self.llm = init_chat_model(
                    model=self.model,
                    base_url=self.base_url,
                    api_key=api_key,
                    max_retries=self.max_retries
                )
            else:
                raise NotImplementedError(f"Model provider '{self.model_provider}' not supported.")
            print(f'Main LLM 初始化完成: {self.llm}')
        return self.llm

class LazyRerankLLM:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(
        self,
        model_provider='openai',
        model='qwen-max-latest', # 使用免费额度 https://bailian.console.aliyun.com/?tab=model#/model-market/detail/qwen-max?modelGroup=qwen-max
        base_url='https://dashscope.aliyuncs.com/compatible-mode/v1',
        env_key='DASHSCOPE_API_KEY',
        max_retries=3,
    ):
        if self._initialized:
            return

        self.model_provider = model_provider
        self.model = model
        self.base_url = base_url
        self.env_key = env_key
        self.max_retries = max_retries
        self.llm = None
        self._initialized = True

    def get_llm(self):
        if self.llm is None:
            print(f'初始化 Rerank LLM : {self.model_provider} - {self.model}')
            load_dotenv()
            api_key = os.getenv(self.env_key)
            if not api_key:
                api_key = getpass(f"Enter your {self.model_provider} API key: ")
                os.environ[self.env_key] = api_key

            if self.model_provider == 'openai':
                self.llm = init_chat_model(
                    model_provider=self.model_provider,
                    model=self.model,
                    base_url=self.base_url,
                    api_key=api_key,
                    max_retries=self.max_retries
                )
            else:
                raise NotImplementedError(f"Model provider '{self.model_provider}' not supported.")
            print(f'Rerank LLM 初始化完成: {self.llm}')
        return self.llm
