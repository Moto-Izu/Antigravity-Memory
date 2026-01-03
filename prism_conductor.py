import subprocess
import sys
import threading
import signal
import time
import os

# --- CONFIG ---
ENGINE_SCRIPT = "social_resonance_engine.py"
SERVER_SCRIPT = "resonance_server.py"

# --- ANSI ---
C_RESET = "\033[0m"
C_ENGINE = "\033[36m" # Cyan
C_SERVER = "\033[35m" # Magenta
C_SYS = "\033[33m"    # Yellow

processes = []

def log(tag, color, msg):
    print(f"{color}[{tag}] {msg}{C_RESET}")

def stream_reader(proc, tag, color):
    for line in iter(proc.stdout.readline, ''):
        if line:
            print(f"{color}[{tag}]{C_RESET} {line.strip()}")
    proc.stdout.close()

def start_process(cmd, tag, color):
    try:
        # bufsize=1 means line buffered
        proc = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            text=True, 
            bufsize=1,
            cwd=os.getcwd()
        )
        t = threading.Thread(target=stream_reader, args=(proc, tag, color))
        t.daemon = True
        t.start()
        return proc
    except Exception as e:
        log("SYSTEM", C_SYS, f"Failed to start {tag}: {e}")
        return None

def cleanup(signum, frame):
    log("CONDUCTOR", C_SYS, "Initiating Graceful Shutdown...")
    for p in processes:
        if p.poll() is None:
            try:
                p.terminate()
                p.wait(timeout=2)
            except:
                p.kill()
    log("CONDUCTOR", C_SYS, "Orchestra Silenced.")
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    log("CONDUCTOR", C_SYS, "Initializing Social Resonance System...")
    print(f"{C_SYS}╔════════════════════════════════════════╗{C_RESET}")
    print(f"{C_SYS}║   COLLECTIVE MIND: ORCHESTRATION LAYER ║{C_RESET}")
    print(f"{C_SYS}╚════════════════════════════════════════╝{C_RESET}")

    
    # 1. Start Server (Synaptic Relay)
    srv = start_process(["python3", "-u", SERVER_SCRIPT], "SERVER", C_SERVER)
    if srv: processes.append(srv)
    time.sleep(1)

    # 2. Start Engine (The Descent)
    eng = start_process(["python3", "-u", ENGINE_SCRIPT], "ENGINE", C_ENGINE)
    if eng: processes.append(eng)

    log("CONDUCTOR", C_SYS, "System Fully Operational. Press Ctrl+C to stop.")
    
    # Keep main thread alive
    while True:
        time.sleep(1)
        # Check if children died
        if all(p.poll() is not None for p in processes):
            log("CONDUCTOR", C_SYS, "All subsystems stopped.")
            break

if __name__ == "__main__":
    main()
