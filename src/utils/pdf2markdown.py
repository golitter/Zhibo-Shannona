from docling.document_converter import DocumentConverter
import os
from tqdm import tqdm
from src.config import load_config

os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

config = load_config()
def get_all_files(path:str) -> list[str]:
    # print(path)
    # 列出路径下的所有文件和目录
    items = os.listdir(path)
    # 筛选出所有以.pdf结尾的文件
    pdf_files = [os.path.join(path, item) for item in items if os.path.isfile(os.path.join(path, item)) and item.lower().endswith('.pdf')]
    return pdf_files

def pdfs_to_markdown(pdf_file_paths:list[str], to_dir:str) -> None:
    converter = DocumentConverter()

    for pdf_flie_path in tqdm(pdf_file_paths, desc="处理进度"):
        result = converter.convert(pdf_flie_path)
        file_name = os.path.basename(pdf_flie_path)
        # print(file_name)
        markdown_content = result.document.export_to_markdown()
        markdown_file_path = os.path.join(to_dir, f"{os.path.splitext(file_name)[0]}.md")
        with open(markdown_file_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

if __name__ == '__main__':
    pdf_main_directory = config.get("data_process", "pdf_dir_path")
    print('正在查找PDF文件...')
    pdf_files = get_all_files(pdf_main_directory)
    # print(pdf_files)
    print(f'找到{len(pdf_files)}个PDF文件')
    markdown_target_directory = config.get("data_process", "markdown_dir_path")
    pdfs_to_markdown(pdf_files, markdown_target_directory)