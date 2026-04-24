import os
from openai import OpenAI

# 多模型配置（可自行扩展）
MODEL_CONFIGS = {
    "deepseek": {
        "api_key": os.getenv("DEEPSEEK_API_KEY", "*"),
        "base_url": "https://api.deepseek.com",
        "model_name": "deepseek-chat"
    }
}

DEFAULT_MODEL = "deepseek"

def get_client(model_key=DEFAULT_MODEL):
    cfg = MODEL_CONFIGS[model_key]
    client = OpenAI(
        api_key=cfg["api_key"],
        base_url=cfg["base_url"]
    )
    return client, cfg["model_name"]