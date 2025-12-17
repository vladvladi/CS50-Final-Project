// Initialize socket connection
var socket = io();

// Get room data from data attributes (set by template)
const container = document.querySelector('.chat-container');
var roomCode = container.dataset.roomCode;
var username = container.dataset.username;

// Load message history on page load
window.addEventListener('DOMContentLoaded', () => {
    let messageHistory = JSON.parse(document.getElementById('message-history').textContent);
    let messagesDiv = document.getElementById('messages');
    
    messageHistory.forEach(msg => {
        let messageElement = document.createElement('div');
        messageElement.className = 'message';
        messageElement.innerHTML = `<strong>${msg.name}:</strong> ${msg.text}`;
        messagesDiv.appendChild(messageElement);
    });
    
    // Scroll to bottom after loading history
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
});

socket.on('connect', () => {
    // Join the room
    socket.emit('join', {username: username, room: roomCode});
});

socket.on('message', (msg) => {
    let messagesDiv = document.getElementById('messages');
    let messageElement = document.createElement('div');
    messageElement.className = 'message';
    messageElement.innerHTML = `<strong>${msg.name}:</strong> ${msg.text}`;
    messagesDiv.appendChild(messageElement);
    
    // Auto-scroll to bottom
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
});

// Update members count for all users in room
socket.on('update_members', (data) => {
    document.getElementById('members-count').innerText = data.count;
});

socket.on('redirect', (data) => {
    window.location.href = data.url;
});

function sendMessage() {
    let input = document.getElementById('message-input');
    let message = input.value.trim();
    if (message) {
        socket.emit('message', {name: username, text: message, room: roomCode});
        input.value = '';
    }
}

// Add Enter key support
document.getElementById('message-input').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

function leaveRoom() {
    socket.emit('leave', {username: username, room: roomCode});
}

function copyRoomCode() {
    const codeText = document.getElementById('room-code').innerText;
    navigator.clipboard.writeText(codeText).then(() => {
        // Visual feedback
        const btn = event.currentTarget;
        const originalHTML = btn.innerHTML;
        btn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"></polyline></svg>';
        btn.style.color = 'var(--accent)';
        
        setTimeout(() => {
            btn.innerHTML = originalHTML;
            btn.style.color = '';
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy:', err);
    });
}
