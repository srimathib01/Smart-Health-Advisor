
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