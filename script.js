let isBaking = false;
let timeLeft = 25 * 60;
let interval;

function toggleBaking() {
    if (!isBaking) {
        isBaking = true;
        document.getElementById('start-btn').innerText = 'Stop';
        document.getElementById('start-btn').style.background = '#ef4444';
        document.getElementById('bun').className = 'bun rising';

        interval = setInterval(() => {
            timeLeft--;
            const mins = Math.floor(timeLeft / 60);
            const secs = timeLeft % 60;
            document.getElementById('timer-display').innerText = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
            
            if (timeLeft <= 0) {
                clearInterval(interval);
                isBaking = false;
                document.getElementById('start-btn').innerText = 'Start Baking';
                document.getElementById('start-btn').style.background = 'var(--accent)';
                document.getElementById('bun').className = 'bun baked';
                timeLeft = 25 * 60;
            }
        }, 1000);
    } else {
        isBaking = false;
        clearInterval(interval);
        document.getElementById('start-btn').innerText = 'Start Baking';
        document.getElementById('start-btn').style.background = 'var(--accent)';
        document.getElementById('bun').className = 'bun burnt';
    }
}

function handleChatEnter(e) {
    if (e.key === 'Enter') sendChatMessage();
}

async function sendChatMessage() {
    const input = document.getElementById('chat-input');
    const msg = input.value.trim();
    if (!msg) return;
    
    const history = document.getElementById('chat-history');
    
    history.innerHTML += `<div class="chat-msg user">${msg}</div>`;
    input.value = '';
    history.scrollTop = history.scrollHeight;
    
    const aiDiv = document.createElement('div');
    aiDiv.className = 'chat-msg ai';
    aiDiv.innerText = 'Thinking...';
    history.appendChild(aiDiv);
    history.scrollTop = history.scrollHeight;

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt: msg })
        });
        const data = await response.json();
        
        if(data.error) throw new Error(data.error);
        aiDiv.innerText = data.text;
    } catch (error) {
        aiDiv.innerText = "Error connecting to AI: " + error.message;
    }
    history.scrollTop = history.scrollHeight;
}