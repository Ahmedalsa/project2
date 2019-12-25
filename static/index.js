document.addEventListener('DOMContentLoaded', () => {
    // Initialize new Chat
    const nickname = document.querySelector('#nickname').value;
    request.open('POST', '/chat');

    // Initialize local storage
    document.querySelector('button').onclick = () => {
      if (!localStorage.getItem('nickname'))
        localStorage.setItem('nickname', nickname));
      }
