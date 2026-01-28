const API_URL = "/api";

async function startSystem() {
    const startBtn = document.getElementById('btn-start-system');
    const stopBtn = document.getElementById('btn-stop-system');
    const statusEl = document.getElementById('status-system');

    // UI Feedback: Loading
    startBtn.disabled = true;
    startBtn.innerText = "Carregando...";
    statusEl.innerText = "Iniciando...";

    const conf = document.getElementById('conf').value / 100;
    const source = document.getElementById('camera').value;
    const model = document.getElementById('model').value;

    try {
        const response = await fetch(`${API_URL}/start-system`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ source, model, conf })
        });
        const data = await response.json();

        if (data.status === 'success') {
            statusEl.innerText = "Executando (PID: " + data.pid + ")";
            statusEl.classList.add('active');

            // Switch buttons
            startBtn.style.display = 'none';
            stopBtn.style.display = 'block';
        } else {
            statusEl.innerText = "Erro: " + data.message;
            // Reset button
            startBtn.disabled = false;
            startBtn.innerText = "INICIAR SISTEMA";
        }
    } catch (e) {
        statusEl.innerText = "Erro de conexão";
        startBtn.disabled = false;
        startBtn.innerText = "INICIAR SISTEMA";
    }
}

async function stopSystem() {
    const startBtn = document.getElementById('btn-start-system');
    const stopBtn = document.getElementById('btn-stop-system');
    const statusEl = document.getElementById('status-system');

    statusEl.innerText = "Parando...";
    stopBtn.disabled = true;

    try {
        const response = await fetch(`${API_URL}/stop-system`, { method: 'POST' });
        const data = await response.json();

        if (data.status === 'success' || data.message === "System not running") {
            statusEl.innerText = "Parado";
            statusEl.classList.remove('active');

            // Switch buttons back
            stopBtn.style.display = 'none';
            stopBtn.disabled = false;

            startBtn.style.display = 'block';
            startBtn.disabled = false;
            startBtn.innerText = "INICIAR SISTEMA";
        } else {
            statusEl.innerText = "Erro ao parar: " + data.message;
            stopBtn.disabled = false;
        }
    } catch (e) {
        statusEl.innerText = "Erro de conexão";
        stopBtn.disabled = false;
    }
}

async function startCapture() {
    const statusEl = document.getElementById('status-capture');
    statusEl.innerText = "Abrindo...";

    try {
        const response = await fetch(`${API_URL}/capture`, { method: 'POST' });
        const data = await response.json();

        if (data.status === 'success') {
            statusEl.innerText = "Executando (PID: " + data.pid + ")";
            statusEl.classList.add('active');
        } else {
            statusEl.innerText = "Erro: " + data.message;
        }
    } catch (e) {
        statusEl.innerText = "Erro de conexão";
    }
}

async function startLabel() {
    const statusEl = document.getElementById('status-train');
    statusEl.innerText = "Rotulando...";

    try {
        const response = await fetch(`${API_URL}/label`, { method: 'POST' });
        const data = await response.json();
        statusEl.innerText = data.message;
    } catch (e) {
        statusEl.innerText = "Erro de conexão";
    }
}

async function startManualLabel() {
    const statusEl = document.getElementById('status-train');
    statusEl.innerText = "Abrindo Labelme...";

    try {
        const response = await fetch(`${API_URL}/manual-label`, { method: 'POST' });
        const data = await response.json();
        statusEl.innerText = data.message;
    } catch (e) {
        statusEl.innerText = "Erro de conexão";
    }
}

async function startTrain() {
    const statusEl = document.getElementById('status-train');
    statusEl.innerText = "Iniciando Treino...";

    try {
        const response = await fetch(`${API_URL}/train`, { method: 'POST' });
        const data = await response.json();
        statusEl.innerText = data.message;
    } catch (e) {
        statusEl.innerText = "Erro de conexão";
    }
}

// Polling to check system status and update UI
setInterval(async () => {
    try {
        const response = await fetch(`${API_URL}/status`);
        const status = await response.json();

        // Check system status
        if (status.system === 'stopped') {
            const startBtn = document.getElementById('btn-start-system');
            const stopBtn = document.getElementById('btn-stop-system');
            const statusEl = document.getElementById('status-system');

            if (stopBtn.style.display !== 'none') {
                // Process ended externally, reset UI
                statusEl.innerText = "Offline";
                statusEl.classList.remove('active');

                stopBtn.style.display = 'none';
                startBtn.style.display = 'block';
                startBtn.disabled = false;
                startBtn.innerText = "INICIAR SISTEMA";
            }
        }
    } catch (e) {
        // Silently fail if server is down
    }
}, 2000); // Check every 2 seconds
