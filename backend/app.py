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
    # Get data from POST request
    data = request.json

    # system_content japanese
    sys_content = "Please rewrite the following sentence to make it more polite. Please write the text in Japanese and make it much more polite."
    # user_content
    try:
        user_content = data['text']
    except:
        abort(400)

    # send to openai api gpt3.5turbo and get response
    response = chatgpt(sys_content, user_content)

    return jsonify({"result": response})
@app.route('/api/add_emoji', methods=['POST'])
def add_emoji():
    # Get data from POST request
    data = request.json

    # system_content
    sys_content = "Add emojis to the following contents.  Please use Japanese."

    # user_content
    try:
        user_content = "\n:" + data['text']
    except:
        abort(400)

    # delete all emojis from user_content
    #clean_user_content = remove_emojis(user_content)

    # send to openai api gpt3.5turbo and get response
    response = chatgpt(sys_content, user_content)

    return jsonify({"result": response})

@app.route('/api/reply', methods=['POST'])
def reply_email():
    # Get data from POST request
    data = request.json

    # system_content japanese
    sys_content = "以下の受信内容と返信要件に基づいてメール返信文を作成してください。文章は日本語で書いて"

    # user_content
    try:
        user_content = "受信内容:" + data['received_email'] + "\n" + "返信要件:" + data['text']
    except:
        abort(400)

    # send to openai api gpt3.5turbo and get response
    response = chatgpt(sys_content, user_content)

    return jsonify({"result": response})


@app.route('/api/generate', methods=['POST'])
def generate_email():
    # Get data from POST request
    data = request.json

    # system_content japanese
    #sys_content = "以下の内容(署名,宛名,要件)に基づいてメールの本文を作成してください。'拝啓'と'敬具'は不要.署名と宛名が不明な場合は分かりやすく'「署名」'と「'宛名」'と書く。メールの最後に宛名は要らない。文章は日本語で書いて"
    sys_content = "Please create the body of the Japanese business email based on the following details (署名,宛名,要件). There's no need for '拝啓' and '敬具'. If the signature and recipient are not clear, write clearly as '「署名」' and '「宛名」'. There's no need for the recipient's name at the end of the email. Please write the text in Japanese and make it much more polite. "
    # user_content
    try:
        user_content = "宛名:" + data['recipient'] + "\n" + "署名:" + data['signature'] + "\n" + "要件:" + data['text']
    except:
        abort(400)


    # send to openai api gpt3.5turbo and get response
    response = chatgpt(sys_content, user_content)

    return jsonify({"result": response})

# something wrong with this function
def remove_emojis(text):
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F700-\U0001F77F"  # alchemical symbols
        u"\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
        u"\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        u"\U0001FA00-\U0001FA6F"  # Chess Symbols
        u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        u"\U00002702-\U000027B0"  # Dingbats
        u"\U000024C2-\U0001F251"  
        "]+",
        flags=re.UNICODE,
    )
    return emoji_pattern.sub(r'', text)

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

if __name__ == "__main__":
    port = int(os.getenv("PORT", 4000))
    app.run(host="0.0.0.0", port=port)