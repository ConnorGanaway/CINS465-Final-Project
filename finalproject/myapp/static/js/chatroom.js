function scrollToBottom() {
    let objDiv = document.getElementById("chat-log");
    objDiv.scrollTop = objDiv.scrollHeight;
}

scrollToBottom();

const roomName = JSON.parse(document.getElementById('room-name').textContent);
const userName = JSON.parse(document.getElementById('username').textContent);

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + roomName
    + '/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    if (data.message) {
        document.querySelector('#chat-log').value += ('' + data.username + ': ' +data.message + '\n');
    } else {
        alert('The message was empty!')
    }

    scrollToBottom();
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message': message,
        'username': userName,
        'room': roomName
    }));
    messageInputDom.value = '';
};

