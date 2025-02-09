from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)

# 阿里云配置
ALIYUN_CONFIG = {
    "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1/",
    "model": "deepseek-r1",
}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    api_key = data["apiKey"]
    messages = data["messages"]

    try:
        client = openai.OpenAI(api_key=api_key, base_url=ALIYUN_CONFIG["base_url"])

        response = client.chat.completions.create(
            model=ALIYUN_CONFIG["model"], messages=messages, temperature=0.7
        )

        return jsonify({"content": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
