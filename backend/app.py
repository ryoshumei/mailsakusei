from flask import Flask, jsonify, request, abort, send_from_directory
import os
import openai

app = Flask(__name__, static_folder='../frontend', static_url_path='')
# need OPEN-AI API KEY below
openai.api_key = os.getenv('OPENAI_KEY')
@app.route('/')
def index():
    # return ../frontend/index.html
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/generate', methods=['POST'])
def generate_email():
    # Get data from POST request
    data = request.json

    # Use your 日本語メール作成AI logic here
    email_content = "以下の内容に基づいてメールの本文を作成してください。拝啓と敬具は不要、署名は直接書く署名：は不要。宛名：{宛名の内容 or '' if none}要件：{要件の内容}{署名の内容 or '' if none}"

    # email_content concat with data
    full_prompt = email_content + "\n" + "宛名:" + data['recipient'] + "\n" + "署名:" + data['signature'] + "\n" + "要件:" + data['text']

    # send to openai api gpt3.5turbo and get response
    response = chatgpt(full_prompt)

    return jsonify({"result": response})


def chatgpt(text):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": text}
            ]
        )
    except:
        return "エラーが発生しました。"
    return completion.choices[0].message.content.strip()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 4000))
    app.run(host="0.0.0.0", port=port)