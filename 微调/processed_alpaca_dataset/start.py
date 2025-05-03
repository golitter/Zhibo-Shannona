import json
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from use_deepseek_r1 import *
from use_local_llm import *
OUTPUT_DIR = "./data/output/"

def process_item(item_id: int) -> None:
    # 这里可以是任何需要处理的逻辑
    # 例如，调用 DeepSeek R1 API 或本地 LLM
    result = get_message_dsr1()
    # result = get_message_localllm()
    return {"id": item_id, "result": result}

rng = range(1, 567)
max_workers = 2

def main():
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_item = {executor.submit(process_item, item_id): item_id for item_id in rng}
        for future in tqdm(as_completed(future_to_item), total=len(rng), desc="评估中"):
            try:
                result = future.result()
                with open(OUTPUT_DIR + f"{result['id']}.txt", "w") as f:
                    json.dump(result['result'], f, ensure_ascii=False, indent=4)
            except Exception as e:
                print(f"Error processing item {future_to_item[future]}: {e}")

if __name__ == "__main__":
    main()
