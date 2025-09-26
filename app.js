async function sendMessage() {
    const input = document.getElementById('user-input');
    const text = input.value;
    input.value = '';

    const res = await fetch('/chat', {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({user_id:1, text: text})
    });
    const data = await res.json();

    const chatBox = document.getElementById('chat-box');
    chatBox.innerHTML += `<p><b>You:</b> ${text}</p>`;
    chatBox.innerHTML += `<p><b>MindMate:</b> ${data.reply}</p>`;
}
