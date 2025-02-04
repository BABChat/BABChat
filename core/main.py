import os
from flask import Flask, request, render_template
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # 加载环境变量

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一个乐于助人的助手"},
                {"role": "user", "content": user_message},
            ],
        )
        return {"reply": response.choices[0].message.content, "status": "success"}
    except Exception as e:
        return {"reply": str(e), "status": "error"}


if __name__ == "__main__":
    app.run(debug=True)
