import os
from flask import Flask, render_template_string, request
import requests

GEMINI_API_KEY = "AIzaSyD40NLXnRtETxrbPKOxXK4SeoDTNBDpgHw"

def processInput(inputText):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {GEMINI_API_KEY}',
    }
    data = {
        'prompt': f"As your personal health assistant, I can provide you with some tips based on your symptoms: {inputText}.",
        'max_tokens': 150,
    }
    response = requests.post('https://api.gemini.com/v1/completions', headers=headers, json=data)
    try:
        output = response.json()['choices'][0]['text']
    except KeyError as e:
        output = f"Error: Unexpected response format - {response.json()}"
    return output

app = Flask(__name__, static_url_path="/static")

@app.route('/', methods=['GET', 'POST'])
def hello():
    output = ""
    if request.method == 'POST':
        inputText = request.form['input']
        output = processInput(inputText)
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
<title>Personal Health Assistant</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" type="text/css" href="/static/personalAssistant.css">
</head>
<body>
<div class="hero">
    <h1>Personal Health <span>Assistant Bot</span></h1>
    <textarea id="inputTextArea" placeholder="Write your Symptoms here..."></textarea>
    <div class="row"> 
      <button id="enterButton">Enter</button>
    </div>
    <textarea id="outputTextArea" class="result" placeholder="Finding way out.." readonly> </textarea>
</div>
<script>
document.addEventListener('DOMContentLoaded', function () {
  const input = document.getElementById('inputTextArea');
  const output = document.getElementById('outputTextArea');

  input.addEventListener('keydown', function (event) {
      if (event.key === 'Enter')
      {
          event.preventDefault(); 
          const inputText = input.value.trim(); 
          processInput(inputText);
      }
  });

  const enterButton = document.getElementById('enterButton');
  enterButton.addEventListener('click', function () {
      const inputText = input.value.trim();
      processInput(inputText);
  });

  function processInput(inputText) {
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
          console.error('Error:', error);
      });
  }
});

</script>
</body>
</html>
''',
                               output=output)

@app.route('/generate', methods=['POST'])
def generate():
    inputText = request.form['input']
    return processInput(inputText)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
