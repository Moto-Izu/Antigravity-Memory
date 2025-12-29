import json
import urllib.request
import socket
import struct
import base64
import os
import time
import sys
import random
import datetime

# --- CONFIGURATION ---
CHROME_DEBUG_PORT = 9222
TARGET_DOMAIN = "x.com"
SCROLL_INTERVAL_MIN = 2.0
SCROLL_INTERVAL_MAX = 4.5
RESONANCE_LOG = "resonance_log.jsonl"

# --- ANSI VISUALS ---
C_RESET = "\033[0m"
C_DIM = "\033[2m"
C_CYAN = "\033[36m"
C_GREEN = "\033[32m"
C_RED = "\033[31m"
C_YELLOW = "\033[33m"
C_BOLD = "\033[1m"
CLEAR_SCREEN = "\033[2J\033[H"

def log_system(msg, level="INFO"):
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    color = C_GREEN if level == "INFO" else (C_RED if level == "ERROR" else C_CYAN)
    print(f"{C_DIM}[{ts}]{C_RESET} {color}{level:<5}{C_RESET} {msg}")

# --- PROTOCOL: SYNAPSE (Raw Socket / WebSocket) ---

def create_ws_frame(message):
    """
    Constructs a masked text frame (Opcode 0x1) for sending to the browser.
    """
    msg_bytes = message.encode('utf-8')
    length = len(msg_bytes)
    
    header = bytearray([0x81]) # Fin + Text
    
    if length < 126:
        header.append(0x80 | length) # Mask bit | length
    elif length < 65536:
        header.append(0x80 | 126)
        header.extend(struct.pack('!H', length))
    else:
        header.append(0x80 | 127)
        header.extend(struct.pack('!Q', length))
        
    mask_key = os.urandom(4)
    header.extend(mask_key)
    
    payload = bytearray(msg_bytes)
    for i in range(len(payload)):
        payload[i] ^= mask_key[i % 4]
        
    return header + payload

def parse_ws_frame(data):
    """
    Parses unmasked frames from the browser (Server -> Client).
    """
    if len(data) < 2: return None, data
    
    # fin = data[0] & 0x80
    # opcode = data[0] & 0x0F
    
    payload_len = data[1] & 0x7F
    
    offset = 2
    if payload_len == 126:
        if len(data) < 4: return None, data
        payload_len = struct.unpack('!H', data[2:4])[0]
        offset = 4
    elif payload_len == 127:
        if len(data) < 10: return None, data
        payload_len = struct.unpack('!Q', data[2:10])[0]
        offset = 10
        
    if len(data) < offset + payload_len:
        return None, data # Incomplete
        
    payload = data[offset:offset+payload_len]
    return payload.decode('utf-8', errors='ignore'), data[offset+payload_len:]

# --- CORE: ARCHIMEDES (Connection) ---

def find_target_tab():
    log_system("Scanning Neural Interface (Localhost:9222)...")
    try:
        req = urllib.request.Request(f"http://localhost:{CHROME_DEBUG_PORT}/json/list")
        with urllib.request.urlopen(req) as f:
            tabs = json.loads(f.read().decode('utf-8'))
    except Exception as e:
        log_system(f"Connection Failed: {e}", "ERROR")
        return None, None

    # Priority: Explicit Target Domain, then most recent active tab
    target = None
    for tab in tabs:
        url = tab.get("url", "")
        if TARGET_DOMAIN in url:
            target = tab
            break
    
    if target:
        log_system(f"Locked Target: {C_BOLD}{target.get('title', 'Unknown')}{C_RESET} ({target.get('url')})")
        return target.get("webSocketDebuggerUrl"), target.get("id")
    
    log_system(f"Target '{TARGET_DOMAIN}' not found within active thoughts.", "WARN")
    return None, None

def connect_socket(ws_url):
    path = ws_url.replace(f"ws://localhost:{CHROME_DEBUG_PORT}", "")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', CHROME_DEBUG_PORT))
    
    key = base64.b64encode(os.urandom(16)).decode('utf-8')
    handshake = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: localhost:{CHROME_DEBUG_PORT}\r\n"
        "Upgrade: websocket\r\n"
        "Connection: Upgrade\r\n"
        f"Sec-WebSocket-Key: {key}\r\n"
        "Sec-WebSocket-Version: 13\r\n"
        "\r\n"
    )
    s.sendall(handshake.encode('utf-8'))
    
    # Drain handshake response
    resp = b""
    while b"\r\n\r\n" not in resp:
        resp += s.recv(4096)
    
    log_system("Synapse Established.")
    return s

# --- LOGIC: THE DESCENT (Injection) ---

DESCENT_SCRIPT = """
(function() {
    if (window._neural_uplink_active) return;
    window._neural_uplink_active = true;

    console.log("%c[SOCIAL RESONANCE ENGINE] ACTIVE", "color: #00ff00; font-size: 20px; background: #000");

    const SEEN_TWEETS = new Set();
    
    // Observer to capture atoms as they render
    const observer = new MutationObserver(() => {
        const tweets = Array.from(document.querySelectorAll('article[data-testid="tweet"]'));
        const newAtoms = [];

        tweets.forEach(t => {
            // Unique ID via link or some stable prop. Fallback to naive content hash if needed.
            const timeEl = t.querySelector('time');
            const tweetLink = timeEl ? timeEl.closest('a')?.href : null;
            const id = tweetLink || Math.random().toString(36).substr(2, 9);

            if (SEEN_TWEETS.has(id)) return;
            SEEN_TWEETS.add(id);

            const userEl = t.querySelector('div[data-testid="User-Name"]');
            const userText = userEl ? userEl.innerText.replace(/\\n/g, ' ') : "Unknown";
            
            const textEl = t.querySelector('div[data-testid="tweetText"]');
            const text = textEl ? textEl.innerText : "";
            
            const imgs = Array.from(t.querySelectorAll('img')).map(i => i.src).filter(s => s.includes('media'));

            if (text.length > 0 || imgs.length > 0) {
                newAtoms.push({
                    type: "ATOM",
                    id: id,
                    author: userText,
                    content: text,
                    media: imgs,
                    timestamp: new Date().toISOString()
                });
            }
        });

        if (newAtoms.length > 0) {
            // Transmit back to Python via console (if configured) or just assume the poller catches it.
            // Wait, for pure CDP via socket, we can evaluate a function that returns the buffer.
            // Better strategy: Push to a window-level queue that Python polls.
            window._atom_queue = (window._atom_queue || []).concat(newAtoms);
        }
    });

    observer.observe(document.body, { childList: true, subtree: true });

    // "The Descent": Organic Scrolling
    setInterval(() => {
        const scrollAmount = 300 + Math.random() * 400;
        window.scrollBy({ top: scrollAmount, behavior: 'smooth' });
    }, 4000 + Math.random() * 3000); // 4-7 seconds interval
})();
"""

DATA_HARVEST_SCRIPT = """
(function() {
    const q = window._atom_queue || [];
    window._atom_queue = [];
    return q;
})();
"""

def send_cdp_command(sock, msg_id, method, params=None):
    msg = {"id": msg_id, "method": method}
    if params:
        msg["params"] = params
    sock.sendall(create_ws_frame(json.dumps(msg)))

def run_engine():
    print(CLEAR_SCREEN)
    print(f"{C_BOLD}{C_CYAN}::: SOCIAL RESONANCE ENGINE ::: {C_RESET}")
    
    ws_url, _ = find_target_tab()
    if not ws_url:
        return

    try:
        sock = connect_socket(ws_url)
    except ConnectionRefusedError:
        log_system("Connection Refused. Is Chrome running with --remote-debugging-port=9222?", "ERROR")
        return

    # 1. Enable Runtime
    send_cdp_command(sock, 1, "Runtime.enable")

    # 2. Inject The Descent (MutationObserver + Scroll)
    log_system("Injecting 'The Descent' viral logic...")
    send_cdp_command(sock, 2, "Runtime.evaluate", {
        "expression": DESCENT_SCRIPT,
        "userGesture": True
    })

    log_system(f"Resonance Loop Initiated. Logging to {RESONANCE_LOG}")
    log_system("Press Ctrl+C to abort.")
    print("-" * 50)

    msg_id = 100
    try:
        with open(RESONANCE_LOG, "a", encoding="utf-8") as f_log:
            while True:
                # Poll the queue
                msg_id += 1
                send_cdp_command(sock, msg_id, "Runtime.evaluate", {
                    "expression": DATA_HARVEST_SCRIPT,
                    "returnByValue": True
                })

                # Read responses
                # Note: This is a simplified sync loop. Real CDP is async. 
                # We need to read *everything* on the wire until we find our response or empty.
                # For `select` based checking or non-blocking, we'd need more code.
                # Here we blocking read.
                
                # Logic: We might get "Runtime.consoleAPICalled" events or other noise.
                # We look for the result of our specific msg_id.
                
                # To avoid blocking forever if no data, set timeout
                sock.settimeout(1.0)
                try:
                    # Accumulate buffer for this 'tick'
                    buffer = b""
                    while True:
                        try:
                            chunk = sock.recv(65536)
                            if not chunk: break
                            buffer += chunk
                        except socket.timeout:
                            break
                    
                    # Process buffer
                    while buffer:
                        text, remainder = parse_ws_frame(buffer)
                        if text:
                            try:
                                data = json.loads(text)
                                # Check if this is our harvest result
                                if data.get("id") == msg_id:
                                    result = data.get("result", {}).get("result", {}).get("value")
                                    if result:
                                        for atom in result:
                                            # Visual Feedback
                                            author = atom.get('author', '???')
                                            content = atom.get('content', '')[:60].replace('\n', ' ')
                                            print(f"{C_CYAN}@{author}{C_RESET}: {content}...")
                                            
                                            # Archive
                                            f_log.write(json.dumps(atom) + "\n")
                                            f_log.flush()
                            except:
                                pass # Malformed JSON or frame
                        if buffer == remainder: break # Stuck/Incomplete
                        buffer = remainder

                except Exception as e:
                    pass # Timeout or other issue, just loop

                time.sleep(1.5) # Throttle poll

    except KeyboardInterrupt:
        print(f"\n{C_RED}Severing Neural Uplink...{C_RESET}")
    finally:
        sock.close()
        print(f"{C_GREEN}Session Archived.{C_RESET}")

if __name__ == "__main__":
    run_engine()
