from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import subprocess
import os
import sys

app = FastAPI(title="Vision System Dashboard")

# Mount static files (will be created next)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return FileResponse('static/index.html')

# --- API Endpoints ---

class StartConfig(BaseModel):
    source: str = "0"
    model: str = "best_seg.pt"
    conf: float = 0.65

# Keep track of processes (simple implementation)
processes = {}

@app.post("/api/start-system")
def start_system(config: StartConfig):
    """Launches the main vision system (main.py)"""
    cmd = [sys.executable, "main.py", "--source", config.source, "--model", config.model, "--conf", str(config.conf)]
    # Use Popen to run in background
    # Note: On Windows with shell=True/False depending on how we want the window to appear
    # We want a NEW window for the vision system usually, but subprocess might hide it by default.
    # On Windows, 'start' command opens a new window, but subprocess.Popen(['python', ...])
    # usually spawns a console window if python is used.
    
    # Let's try direct execution. If it blocks or hides window, we might need creationflags.
    if "system" in processes and processes["system"].poll() is None:
        return {"status": "error", "message": "System already running"}

    try:
        # start_new_session=True helps detach it somewhat
        proc = subprocess.Popen(cmd, cwd=os.getcwd()) 
        processes["system"] = proc
        return {"status": "success", "message": "System started", "pid": proc.pid}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/api/capture")
def start_capture():
    """Launches the capture tool (capture_data.py)"""
    if "capture" in processes and processes["capture"].poll() is None:
        return {"status": "error", "message": "Capture tool already running"}

    try:
        proc = subprocess.Popen([sys.executable, "capture_data.py"], cwd=os.getcwd())
        processes["capture"] = proc
        return {"status": "success", "message": "Capture tool started", "pid": proc.pid}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/api/manual-label")
def start_manual_label():
    """Launches Labelme for manual annotation"""
    try:
        # Launch labelme pointing to the dataset directory
        # labelme [image_dir]
        dataset_dir = os.path.join(os.getcwd(), "dataset")
        cmd = ["labelme", dataset_dir]
        
        proc = subprocess.Popen(cmd, cwd=os.getcwd())
        return {"status": "success", "message": "Labelme started"}
    except Exception as e:
        return {"status": "error", "message": "Could not start Labelme. Error: " + str(e)}

@app.post("/api/label")
def start_labeling():
    """Runs auto-labeling (auto_label.py) - This is blocking usually, but we'll run async background"""
    try:
        # This one prints to stdout, we might want to capture it? 
        # For now, let it run in its own console or background
        proc = subprocess.Popen([sys.executable, "auto_label.py"], cwd=os.getcwd())
        return {"status": "success", "message": "Auto-labeling started..."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/api/train")
def start_training():
    """Runs training (train_wrapper.py)"""
    if "train" in processes and processes["train"].poll() is None:
        return {"status": "error", "message": "Training already in progress"}

    try:
        # We start a new console for it so user can see progress bar
        # Windows specific: CREATE_NEW_CONSOLE = 0x00000010
        creation_flags = 0x00000010
        proc = subprocess.Popen([sys.executable, "train_wrapper.py"], cwd=os.getcwd(), creationflags=creation_flags)
        processes["train"] = proc
        return {"status": "success", "message": "Training started in new window"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/status")
def get_status():
    status = {}
    for name, proc in processes.items():
        if proc.poll() is None:
            status[name] = "running"
        else:
            status[name] = "stopped"
    return status

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
