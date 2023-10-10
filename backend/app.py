from flask import Flask, jsonify, request, abort, send_from_directory
import os
import openai
import emoji
import re

app = Flask(__name__, static_folder='../frontend', static_url_path='')
# need OPEN-AI API KEY below
openai.api_key = os.getenv('OPENAI_KEY')
# Routes
@app.route('/')
def index():
    # return ../frontend/index.html
    return send_from_directory(app.static_folder, 'index.html')
@app.route('/reply_page')
def reply_page():
    # return ../frontend/index.html
    return send_from_directory(app.static_folder, 'reply_page.html')
@app.route('/add_emoji_page')
def add_emoji_page():
    # return ../frontend/index.html
    return send_from_directory(app.static_folder, 'add_emoji_page.html')
# API
@app.route('/api/more_polite', methods=['POST'])
def more_polite():
    try:
        # Get data from POST request
        data = request.json
        lang_string = get_lang_string(data['lang'])
        # system_content japanese
        sys_content = f"Please rewrite the following sentence to make it more polite. Please write the text in {lang_string} and make it much more polite."
        # user_content
        user_content = data['text']
    except:
        abort(400)

    # send to openai api gpt3.5turbo and get response
    response = chatgpt(sys_content, user_content)

    return jsonify({"result": response})
@app.route('/api/add_emoji', methods=['POST'])
def add_emoji():
    # user_content
    try:
        # Get data from POST request
        data = request.json
        lang_string = get_lang_string(data['lang'])
        # system_content
        sys_content = f"Add emojis to the following contents.  Please use {lang_string}."
        user_content = "\n:" + data['text']
    except:
        abort(400)

    # send to openai api gpt3.5turbo and get response
    response = chatgpt(sys_content, user_content)

    return jsonify({"result": response})

@app.route('/api/reply', methods=['POST'])
def reply_email():

    try:
        # Get data from POST request
        data = request.json
        lang_string = get_lang_string(data['lang'])
        # system_content japanese
        sys_content = f"以下の受信内容と返信要件に基づいてメール返信文を作成してください。文章は {lang_string} で書いて"
        # user_content
        user_content = "受信内容:" + data['received_email'] + "\n" + "返信要件:" + data['text']
    except:
        abort(400)

    # send to openai api gpt3.5turbo and get response
    response = chatgpt(sys_content, user_content)

    return jsonify({"result": response})


@app.route('/api/generate', methods=['POST'])
def generate_email():
    # Get data from POST request
    try:
        data = request.json
        lang_string = get_lang_string(data['lang'])
        print(lang_string)
        # system_content japanese
        sys_content = f"Please create the body of the {lang_string} business email based on the following details (署名,宛名,要件). There's no need for '拝啓' and '敬具'. If the signature and recipient are not clear, write clearly as '「署名」' and '「宛名」'. There's no need for the recipient's name at the end of the email. Please write the text in {lang_string} and make it much more polite. "
        # user_content
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

def flex_chatgpt(sys_content, user_content):
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

def get_lang_string(val):
    # van to int
    val = int(val)

    if val == 1:
        return "日本語"
    elif val == 2:
        return "English"
    elif val == 3:
        return "简体中文"
    elif val == 4:
        return "繁體中文"


if __name__ == "__main__":
    port = int(os.getenv("PORT", 4000))
    app.run(host="0.0.0.0", port=port)