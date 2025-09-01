from huggingface_hub import snapshot_download
from src.config import load_config


def load_bge_large_zh_v15():

    config = load_config()
    blz_model_path = config.get('embedding', 'BLZ_model_path')
    print(blz_model_path)

    snapshot_download(repo_id="BAAI/bge-large-zh-v1.5", local_dir=blz_model_path, allow_patterns=["*.json", "*.bin", "*.txt"], endpoint="https://hf-mirror.com", force_download=False)

if __name__ == "__main__":
    load_bge_large_zh_v15()