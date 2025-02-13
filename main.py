# main.py
from flask import Flask, render_template, request, jsonify
import openai
import logging

app = Flask(__name__)

# 预配置的提供商信息
PROVIDER_CONFIGS = {
    "阿里云": {
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1/",
        "default_model": "deepseek-r1",
    },
    "硅基流动": {
        "base_url": "https://api.siliconflow.cn/v1",
        "default_model": "deepseek-ai/DeepSeek-R1",
    },
}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    api_key = data.get("apiKey")
    messages = data.get("messages", [])
    provider_url = data.get("providerUrl", "")
    selected_provider = data.get("provider")
    model_name = data.get("model", "")

    if not api_key or not messages:
        return jsonify({"error": "API密钥或消息为空"}), 400

    try:
        # 确定base_url
        if selected_provider in PROVIDER_CONFIGS:
            base_url = PROVIDER_CONFIGS[selected_provider]["base_url"]
        elif provider_url:
            base_url = provider_url.rstrip("/") + "/"
        else:
            base_url = PROVIDER_CONFIGS["阿里云"]["base_url"]
            selected_provider = "阿里云"

        # 确定模型名称
        if not model_name:
            model_name = PROVIDER_CONFIGS.get(selected_provider, {}).get(
                "default_model", "deepseek-r1"
            )

        client = openai.OpenAI(api_key=api_key, base_url=base_url)

        response = client.chat.completions.create(
            model=model_name, messages=messages, temperature=0.7
        )

        return jsonify({"content": response.choices[0].message.content})
    except Exception as e:
        logging.error(f"Error processing chat request: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
