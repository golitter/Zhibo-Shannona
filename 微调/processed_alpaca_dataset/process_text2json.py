import json
import os

text_directory_path = './data/output'
json_directory_path = './data/jsons_style'

def count_files(directory):
    return len([file for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))])

def text2json(file_id: int) -> None:
    """
    将文本文件转换为JSON格式
    :param file_path: 文本文件路径
    :return: None
    """
    input_file_path = f"./data/output/{file_id}.txt"
    output_file_path = f"./data/jsons_style/{file_id}.json"
    # 读取文本文件内容
    with open(input_file_path, "r", encoding="utf-8") as f:
        text = f.read()
    # print(text)
    # exit(0)
    # 去除反斜杠和换行符
    clean_json_str = text.replace("\\n", "").replace("\\", "")
    # print(clean_json_str)
    # exit(0)
    # 删除首尾的双引号
    delete_presuf_double_quotes = clean_json_str[1:-1]

    # 将字符串转换为JSON对象
    data = json.loads(delete_presuf_double_quotes)

    # 将数据转换为JSON字符串
    json_string = json.dumps(data, indent=4, ensure_ascii=False)
    
    # 保存为JSON文件
    with open(output_file_path, "w", encoding='utf-8') as f:
        f.write(json_string)
        print(f"JSON数据已保存到 {f.name}")

def process_all_text2json() -> None:
    """
    处理所有文本文件并转换为JSON格式
    :return: None
    """
    total_files = count_files(text_directory_path)
    right_process_count = total_files
    except_file_list = []
    for i in range(1, total_files + 1):
        try:
            text2json(i)
        except Exception as e:
            print(f"处理文件 {i} 时发生错误: {e}")
            right_process_count -= 1
            except_file_list.append(i)
            continue
    print(f"所有文件处理完成！, json转换正确率为: {right_process_count}/{total_files}，\n异常文件列表: \n{except_file_list}")

def get_json_file(file_id: int) -> None:
    """
    获取JSON文件
    :param file_id: 文件ID
    :return: None
    """

    file_path = f"./data/jsons_style/{file_id}.json"
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    return json.loads(text)

def process_jsons2json() -> None:
    """
    处理所有JSON文件并转换为JSON格式
    :return: None
    """

    # total_files = count_files(json_directory_path)
    # final_json = []
    # for i in range(1, total_files + 1):
    #     json_fle = get_json_file(i)
    #     final_json += json_fle
        # print(final_json)
    # 将数据转换为JSON字符串

    final_json = []
    for file_name in os.listdir(json_directory_path):
        # print(file_name)
        # exit(0)
        file_path = os.path.join(json_directory_path, file_name)
        # print(file_path)
        # exit(0)
        if os.path.isfile(file_path) and file_path.endswith('.json'):
            file_id = int(file_name.split('.')[0])
            json_file = get_json_file(file_id)
            final_json += json_file
    
    json_string = json.dumps(final_json, indent=4, ensure_ascii=False)
    # 保存为JSON文件
    with open("./data/alpaca_dir/final.json", "w", encoding='utf-8') as f:
        f.write(json_string)
        print(f"JSON数据已保存到 {f.name}")

if __name__ == "__main__":
    

    # print(get_json_file(1))
    # json1 = get_json_file(1)
    # json2 = get_json_file(2)
    # json3 = json1 + json2
    # # print(json.dumps(json3, indent=4, ensure_ascii=False))
    # print(json3)
    # text2json(1)

    # 处理所有文本文件
    # process_all_text2json()

    # 将所有JSON文件合并为一个JSON文件
    process_jsons2json()


# # 提供的文本内容
# with open("data/output/1.txt", "r",encoding="utf-8") as f:
#     text = f.read()

# # 去除反斜杠和换行符
# clean_json_str = text.replace("\\n", "").replace("\\", "")

# # 删除首尾的双引号
# delete_presuf_double_quotes = clean_json_str[1:-1]
# # print(delete_presuf_double_quotes)

# # 将字符串转换为JSON对象
# data = json.loads(delete_presuf_double_quotes)

# # 将数据转换为JSON字符串
# json_string = json.dumps(data, indent=4, ensure_ascii=False)
# with open("data/jsons_style/1.json", "w", encoding='utf-8') as f:
#     f.write(json_string)
#     print(f"JSON数据已保存到 {f.name}")