import json
import urllib.request
import socket
import struct
import base64
import os
import time

def create_ws_frame(message):
    msg_bytes = message.encode('utf-8')
    length = len(msg_bytes)
    header = bytearray([0x81])
    if length < 126:
        header.append(0x80 | length)
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
    if len(data) < 2: return None, data
    payload_len = data[1] & 0x7F
    offset = 2
    if payload_len == 126: offset = 4
    elif payload_len == 127: offset = 10
    if len(data) < offset + payload_len: return None, data
    return data[offset:offset+payload_len].decode('utf-8', errors='ignore'), data[offset+payload_len:]

def generate_video():
    # 1. Get Tab
    try:
        req = urllib.request.Request("http://localhost:9222/json/list")
        with urllib.request.urlopen(req) as f:
            tabs = json.loads(f.read().decode('utf-8'))
    except Exception as e:
        print(f"HTTP Error: {e}")
        return

    ws_url = next((t.get("webSocketDebuggerUrl") for t in tabs if "higgsfield.ai" in t.get("url", "")), None)
    if not ws_url:
        print("Error: Higgsfield tab not found.")
        return

    # 2. Connect
    path = ws_url.replace("ws://localhost:9222", "")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 9222))
    key = base64.b64encode(os.urandom(16)).decode('utf-8')
    s.sendall(f"GET {path} HTTP/1.1\r\nHost: localhost:9222\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n".encode())
    while b"\r\n\r\n" not in s.recv(4096): pass

    # 3. Prompt
    PROMPT = "Cinematic opening scene, beautiful Japanese woman walking in Yokohama city, heading to a date, happy anticipation, light smile, swaying long black hair, dynamic tracking shot, vivid city background, photorealistic, 4k"

    # 4. Inject Action Script
    js_code = f"""
    (function() {{
        // Logic to find Prompt Textarea and Generate Button
        // Try contenteditable text boxes often used in React apps
        let input = document.querySelector('textarea') || document.querySelector('input[type="text"]') || document.querySelector('[contenteditable="true"]');
        
        if (input) {{
            input.focus();
            
            // Method 1: execCommand (Best for contentEditable)
            document.execCommand('selectAll', false, null);
            document.execCommand('insertText', false, "{PROMPT}");
            
            // Method 2: Direct value set (for Inputs)
            if (input.value !== "{PROMPT}" && input.innerText !== "{PROMPT}") {{
                 const nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, "value")?.set;
                 if (nativeSetter && (input.tagName === 'TEXTAREA' || input.tagName === 'INPUT')) {{
                     nativeSetter.call(input, "{PROMPT}");
                 }} else {{
                     input.innerText = "{PROMPT}";
                 }}
                 input.dispatchEvent(new Event('input', {{ bubbles: true }}));
            }}
            
            // Wait slightly for UI update
            setTimeout(() => {{
                // Find Generate Button
                // Filter out dangerous buttons
                const buttons = Array.from(document.querySelectorAll('button'));
                const generateBtn = buttons.find(b => {{
                    const text = b.innerText.toLowerCase();
                    const isGenerate = text.includes('generate') || text.includes('create');
                    const isSafe = !text.includes('upgrade') && !text.includes('pro') && !text.includes('plan') && !text.includes('pricing');
                    return isGenerate && isSafe;
                }});
                
                if (generateBtn) {{
                    generateBtn.click();
                    console.log("Generate Clicked (Safe)");
                    return "Prompt Injected & Clicked";
                }} else {{
                    console.log("Safe Generate Button Not Found. Attempting Enter key.");
                    input.dispatchEvent(new KeyboardEvent('keydown', {{ key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }}));
                     return "Prompt Injected (Enter Key)";
                }}
            }}, 500);
        }} else {{
            return "Textarea not found";
        }}
    }})();
    """

    msg = {"id": 401, "method": "Runtime.evaluate", "params": {"expression": js_code, "returnByValue": True}}
    s.sendall(create_ws_frame(json.dumps(msg)))
    
    # Read Result
    while True:
        try:
            chunk = s.recv(8192)
            if not chunk: break
            decoded, remainder = parse_ws_frame(chunk)
            if decoded:
                try:
                    data = json.loads(decoded)
                    if data.get("id") == 401:
                        print("RESULT:", data.get("result", {}).get("result", {}).get("value", "No Result"))
                        break
                except: pass
        except: break

    s.close()

if __name__ == "__main__":
    generate_video()
