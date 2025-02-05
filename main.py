# 123
import os
from flask import Flask, request, render_template
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# 可用模型列表
AVAILABLE_MODELS = ["deepseek-ai/DeepSeek-R1", "deepseek-ai/DeepSeek-V3"]


@app.route("/")
def index():
    return render_template("index.html", models=AVAILABLE_MODELS)


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data["message"]
    api_key = data["api_key"]
    model = data.get("model", "gpt-3.5-turbo")

    if not api_key:
        return {"reply": "API密钥不能为空", "status": "error"}

    if model not in AVAILABLE_MODELS:
        return {"reply": "不支持选择的模型", "status": "error"}

    try:
        client = OpenAI(api_key=api_key, base_url="https://api.siliconflow.cn/v1")
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "你是一个乐于助人的助手"},
                {"role": "user", "content": user_message},
            ],
            stream=True,
        )
        return {"reply": response.choices[0].message.content, "status": "success"}
    except Exception as e:
        return {"reply": f"API请求失败: {str(e)}", "status": "error"}


if __name__ == "__main__":
    app.run(debug=True)
