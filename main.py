# main.py
from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)

# 预配置的提供商信息
PROVIDER_CONFIGS = {
    "阿里云": {
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1/",
        "default_model": "deepseek-r1",
    },
    "OpenAI": {
        "base_url": "https://api.openai.com/v1",
        "default_model": "gpt-3.5-turbo",
    },
}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    api_key = data["apiKey"]
    messages = data["messages"]
    provider_url = data.get("providerUrl", "")  # 获取自定义的提供商URL
    selected_provider = data.get("provider")  # 获取选中的预设提供商
    model_name = data.get("model", "")  # 获取用户输入的模型名称

    try:
        # 确定最终的base_url
        if selected_provider and selected_provider in PROVIDER_CONFIGS:
            base_url = PROVIDER_CONFIGS[selected_provider]["base_url"]
        elif provider_url:
            base_url = provider_url.rstrip("/") + "/"  # 规范化URL格式
        else:
            # 如果没有输入时默认使用阿里云
            base_url = PROVIDER_CONFIGS["阿里云"]["base_url"]
            selected_provider = "阿里云"

        # 确定最终的模型名称
        if not model_name and selected_provider in PROVIDER_CONFIGS:
            model_name = PROVIDER_CONFIGS[selected_provider]["default_model"]

        client = openai.OpenAI(api_key=api_key, base_url=base_url)

        response = client.chat.completions.create(
            model=model_name, messages=messages, temperature=0.7
        )

        return jsonify({"content": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
