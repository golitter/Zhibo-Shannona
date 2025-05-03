import json

# 假设这是从文件中读取的JSON字符串
json_str = """

# 去除反斜杠和换行符
clean_json_str = json_str.replace("\\", "").replace("\n", "")

# 将字符串转换为JSON对象
json_data = json.loads(clean_json_str)

# 打印处理后的JSON数据
print(json_data)
"""