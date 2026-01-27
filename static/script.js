const API_URL = "/api";

async function startSystem() {
    const conf = document.getElementById('conf').value / 100;
    const source = document.getElementById('camera').value;
    const model = document.getElementById('model').value;
    const statusEl = document.getElementById('status-system');

    statusEl.innerText = "Iniciando...";

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
        } else {
            statusEl.innerText = "Erro: " + data.message;
        }
    } catch (e) {
        statusEl.innerText = "Erro de conexão";
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

// Simple polling to check status? (Optional, skipping for now to keep it simple as PIDs might change)
