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

    # system_content
    sys_content = "以下の内容(署名,宛名,要件)に基づいてメールの本文を作成してください。'拝啓'と'敬具'は不要.署名と宛名が不明な場合は分かりやすく'「署名」'と「'宛名」'と書く。メールの最後に宛名は要らない。文章は日本語で書いて"

    # user_content
    try:
        user_content = "宛名:" + data['recipient'] + "\n" + "署名:" + data['signature'] + "\n" + "要件:" + data['text']
    except:
        abort(400)


    # send to openai api gpt3.5turbo and get response
    response = chatgpt(sys_content, user_content)

    return jsonify({"result": response})


def chatgpt(sys_content, user_content):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": sys_content},
                {"role": "user",
                 "content": user_content}
            ]
        )
    except:
        return "エラーが発生しました。"
    return completion.choices[0].message.content.strip()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 4000))
    app.run(host="0.0.0.0", port=port)