# 智博陕珂娜（Zhibo-Shannona） RAG智能助手

1. 设置`.env`中的密钥。本项目使用deepseek-r1和qwen系列

```.env
deep_seek_api_key=<ds_api_key>
DASHSCOPE_API_KEY=<qwen_api_key>
```

2. 检查相关配置

   ```shell
   python -m src.setup
   ```

   会安装embedding模型、文本向量化、检查chat模型状态。

3. 页面展示

   ```shell
   python webUI.py
   ```

4. api使用

   ```shell
   python app.py
   ```

5. docker容器部署

   ```shell
   # 构建容器
   docker build -t zhibo_shannona:1.0.1 .
   # 运行
   docker run -d -p 8001:8000 zhibo_shannona:1.0.1
   ```



![img](images/d274fccb1720b885a48a14a4c2fab9fd.png)



webUI:

![img](images/2e2192e0e8ee9c5f599e4a888e805de7.png)



**项目具体实现**：

drawio图...