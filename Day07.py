# import os
# from dotenv import load_dotenv
# load_dotenv("D:/agent_Git/.env")
# print(bool(os.environ.get("API_KEY")))   # 应为 True


import os
import requests
from dotenv import load_dotenv

load_dotenv("D:/agent_Git/.env")

api_key = os.getenv("DASHSCOPE_API_KEY")
if not api_key:
    print("错误: 未找到 DASHSCOPE_API_KEY，请检查 .env 文件")
    exit(1)

try:
    resp = requests.post(
        "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "qwen-plus",
            "input": {
                "messages": [
                    {"role": "user",
                     "content": "把'今天心情不错'归为 正面/中性/负面 之一，只输出标签"}
                ]
            },
            "parameters": {
                "result_format": "message"
            }
        },
        timeout=30
    )
    resp.raise_for_status()
except requests.exceptions.ConnectionError:
    print("错误: 网络连接失败")
except requests.exceptions.Timeout:
    print("错误: 请求超时")
except requests.exceptions.HTTPError as e:
    print(f"错误: HTTP 请求失败, 状态码={resp.status_code}")
    print(resp.text)
else:
    data = resp.json()
    content = data.get("output", {}).get("choices", [{}])[0].get("message", {}).get("content", "未获取到内容")
    print("模型返回标签:", content)

    usage = data.get("usage")
    if usage:
        print("Token使用情况:", usage)