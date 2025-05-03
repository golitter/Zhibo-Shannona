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

print("\n==================== 智博陕珂娜 =====================\n")
print("Hello. What can I do for you?")

while True:
    question = input("\n==================== User =====================\n> ")
    print("\n==================== 智博陕珂娜 =====================\n")
    
    cont = ""
    for ans in session.ask(question, stream=True):
        print(ans.content[len(cont):], end='', flush=True)
        cont = ans.content