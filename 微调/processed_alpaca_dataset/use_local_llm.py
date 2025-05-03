from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from prompt_schema import task_prompt

# 模型路径
model_path = "/root/autodl-tmp/Hugging-Face/hub/models--deepseek-ai--DeepSeek-R1-Distill-Qwen-1.5B/snapshots/ad9f0ae0864d7fbcd1cd905e3c6c5b069cc8b562"

# 加载 tokenizer （分词器）
tokenizer = AutoTokenizer.from_pretrained(model_path)

# 加载模型并移动到可⽤设备（GPU/CPU）
device = "cuda" if torch.cuda.is_available() else "cpu"

model = AutoModelForCausalLM.from_pretrained(model_path).to(device)

def get_message_localllm(prompt: str = task_prompt):
    # 使⽤ tokenizer 编码输⼊的 prompt
    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    # 使⽤模型⽣成⽂本
    outputs = model.generate(inputs["input_ids"], max_length=15000)

    # 解码⽣成的输出
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
 
    return generated_text

if __name__ == "__main__":
    # 使⽤模型⽣成⽂本
    result = generate_text()
    print(result)