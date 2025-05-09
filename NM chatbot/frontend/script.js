document.addEventListener('DOMContentLoaded', function () {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const defaultOptionsDiv = document.getElementById('default-options');
  
    function addMessage(content, isUser) {
      const messageDiv = document.createElement('div');
      messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
  
      const avatarDiv = document.createElement('div');
      avatarDiv.className = 'avatar';
      avatarDiv.innerHTML = isUser ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';
  
      const contentDiv = document.createElement('div');
      contentDiv.className = 'message-content';
      contentDiv.innerHTML = `<p>${content}</p>`;
  
      messageDiv.appendChild(avatarDiv);
      messageDiv.appendChild(contentDiv);
  
      chatMessages.appendChild(messageDiv);
      chatMessages.scrollTop = chatMessages.scrollHeight;
    }
  
    function showDefaultOptions() {
      const options = [
        "Account issues",
        "Order status",
        "Product information",
        "Payment questions",
        "Talk to a human"
      ];
  
      options.forEach(option => {
        const btn = document.createElement('button');
        btn.className = 'option-button';
        btn.textContent = option;
        btn.addEventListener('click', () => {
          userInput.value = option;
          sendMessage();
        });
        defaultOptionsDiv.appendChild(btn);
      });
    }
  
    async function sendMessage() {
      const message = userInput.value.trim();
      if (message === '') return;
  
      addMessage(message, true);
      userInput.value = '';
  
      try {
        const response = await fetch('http://127.0.0.1:5000/api/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ message: message })
        });
  
        const data = await response.json();
        addMessage(data.response, false);
      } catch (error) {
        addMessage("Sorry, I'm having trouble connecting to the server.", false);
        console.error('Error:', error);
      }
    }
  
    sendButton.addEventListener('click', sendMessage);
  
    userInput.addEventListener('keypress', function (e) {
      if (e.key === 'Enter') {
        sendMessage();
      }
    });
  
    // Initialize default options
    showDefaultOptions();
  });
  