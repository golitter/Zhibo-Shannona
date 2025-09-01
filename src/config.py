import configparser
import os
import yaml

def load_config():
    config = configparser.ConfigParser()
    config_file_path = './config.ini'
    if not os.path.exists(config_file_path):
        print(f"错误：配置文件 '{config_file_path}' 不存在！")
        exit()
    config.read(config_file_path, encoding='utf-8')
    return config


def load_prompt_templates() -> dict:
    config = load_config()
    prompt_template_path = config.get('prompts', 'prompt_template')
    if not os.path.exists(prompt_template_path):
        raise FileNotFoundError(f"配置文件未找到: {prompt_template_path}")

    with open(prompt_template_path, 'r', encoding='utf-8') as f:
        # 使用 safe_load 防止执行任意代码，更安全
        prompts = yaml.safe_load(f)
    
    return prompts

# print(load_prompt_templates())