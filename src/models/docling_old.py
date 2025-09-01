from huggingface_hub import snapshot_download
from src.config import load_config


def load_docling_layout_model():

    config = load_config()
    docling_old = config.get('docling', 'docling_model_path')
    print(docling_old)

    snapshot_download(repo_id="ds4sd/docling-layout-old", local_dir=docling_old, allow_patterns=["*.json", "*.bin", "*.txt"], endpoint="https://hf-mirror.com", force_download=False)

if __name__ == "__main__":
    load_docling_layout_model()