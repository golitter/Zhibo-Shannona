from docling.document_converter import DocumentConverter
import os
from tqdm import tqdm

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
    main_directory = './data/pdf/'
    print('正在查找PDF文件...')
    pdf_files = get_all_files(main_directory)
    print(f'找到{len(pdf_files)}个PDF文件')
    target_directory = './data/markdown/'
    pdfs_to_markdown(pdf_files, target_directory)