import os
from flask import Flask, render_template_string, request
import requests
import json
from dotenv import load_dotenv

load_dotenv()

# Secure API key from environment
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

app = Flask(__name__, static_url_path="/static")

def processInput(inputText):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8080",  # Optional: your deployment domain
        "X-Title": "Personal Health Assistant",   # Optional: app title
    }

    data = {
        "model": "deepseek/deepseek-v3-base:free",
        "messages": [
            {
                "role": "user",
                "content": f"As your personal health assistant, I can provide tips and suggest medicines based on your symptoms: {inputText}"
            }
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, data=json.dumps(data))

    try:
        return response.json()['choices'][0]['message']['content']
    except KeyError:
        return f"Error: {response.json()}"

@app.route('/', methods=['GET', 'POST'])
def hello():
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
  <title>Personal Health Assistant</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" type="text/css" href="/static/personal-Assistant.css">
</head>
<body>
  <div class="hero">
    <h1>Personal Health <span>Assistant Bot</span></h1>
    <textarea id="inputTextArea" placeholder="Write your Symptoms here..."></textarea>
    <div class="row"> 
      <button id="enterButton">Enter</button>
    </div>
    <textarea id="outputTextArea" class="result" placeholder="Finding way out.." readonly></textarea>
  </div>
<script>
document.addEventListener('DOMContentLoaded', function () {
  const input = document.getElementById('inputTextArea');
  const output = document.getElementById('outputTextArea');

  document.getElementById('enterButton').addEventListener('click', function () {
      const inputText = input.value.trim();
      if (inputText.length === 0) return;

      fetch('/generate', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: `input=${encodeURIComponent(inputText)}`
      })
      .then(response => response.text())
      .then(data => {
          output.value = data;
      })
      .catch(error => {
          output.value = "Error: Unable to process your request.";
          console.error('Error:', error);
      });
  });
});
</script>
</body>
</html>
''')

@app.route('/generate', methods=['POST'])
def generate():
    inputText = request.form.get('input', '')
    return processInput(inputText)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
