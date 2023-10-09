# Japanese Email Creation AI

## Introduction

This project, "Japanese Email Creation AI," is a web application that allows users to create emails in Japanese simply and efficiently. It includes an email generation feature and an emoji addition function, both utilizing the OpenAI API. This project is currently available for free at [mailsakusei.com](https://www.mailsakusei.com).

## Technologies Used

- **Backend**: Python Flask
- **Frontend**: HTML5, JavaScript (jQuery), Bootstrap
- **API**: OpenAI API

## Setup

1. **Clone the Repository**

    ```
    git clone [https://github.com/ryoshumei/mailsakusei.git]
    ```

2. **Install Dependencies**

    ```
    pip install -r requirements.txt
    ```

3. **Set Environment Variable**

   To use the OpenAI API, please set your API key as an environment variable.

    ```
   openai.api_key = os.getenv('OPENAI_KEY')
    ```

4. **Run the Application**

    ```
    python app.py
    ```

## Features

1. **Character Counter**: Counts the number of characters entered into the text area and limits them to 500 characters.
2. **Automatic Email Generation**: Generates email text automatically using the OpenAI API based on the input text.
3. **Insert Emoji, Adjust for Politeness**: Adjusts the generated content using the OpenAI API.

## Usage

1. Visit the webpage and enter your message into the provided text area.
2. Click the "Create" button to display the automatically generated email text.

## Screenshots

![Weixin Image_20231009233600.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3533761/c9b1a00b-35d6-3913-0042-7e4a5f239771.jpeg)

## Publication

This project is available for free at [mailsakusei.com](https://www.mailsakusei.com). Please visit and use it.

## Conclusion

"Japanese Email Creation AI" is a simple tool that supports email creation in Japanese. In the future, we plan to expand its features to make it a convenient tool for users in various situations.
