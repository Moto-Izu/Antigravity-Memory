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

def generate_image():
    # 1. Get Tab
    try:
        req = urllib.request.Request("http://localhost:9222/json/list")
        with urllib.request.urlopen(req) as f:
            tabs = json.loads(f.read().decode('utf-8'))
    except Exception as e:
        print(f"HTTP Error: {e}")
        return

    ws_url = next((t.get("webSocketDebuggerUrl") for t in tabs if "midjourney.com" in t.get("url", "")), None)
    if not ws_url:
        print("Error: Midjourney tab not found.")
        return

    # 2. Connect
    path = ws_url.replace("ws://localhost:9222", "")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 9222))
    key = base64.b64encode(os.urandom(16)).decode('utf-8')
    s.sendall(f"GET {path} HTTP/1.1\r\nHost: localhost:9222\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n".encode())
    while b"\r\n\r\n" not in s.recv(4096): pass

    # 3. Prompt
    PROMPT = "Extremely beautiful Japanese woman, 27 years old, light smile while keeping small mouth, delicate small mouth, round beautiful eyes, blend of cute and beautiful, round face, long straight black hair down to waist, walking in modern Yokohama streets, casual fashion, photorealistic, cinematic lighting --ar 4:5 --v 7"
    
    # 4. Inject Action Script
    # Attempts to find the prompt bar and insert text, then simulate Enter.
    js_code = f"""
    (function() {{
        // Specialized selector for Midjourney Web Alpha
        // They often use ContentEditable divs or textareas in a specific container.
        // We will try multiple common selectors.
        
        const selectors = [
            '[data-testid="prompt-bar-input"]',
            'textarea[placeholder*="What will you imagine"]',
            'input[placeholder*="What will you imagine"]',
            'div[role="textbox"][aria-label*="Prompt"]',
            '#prompt-input'
        ];
        
        let input = null;
        for (let sel of selectors) {{
            input = document.querySelector(sel);
            if (input) break;
        }}
        
        if (!input) {{
            // Fallback: Use active element if it looks like an input
            if (document.activeElement && (document.activeElement.tagName === 'INPUT' || document.activeElement.tagName === 'TEXTAREA' || document.activeElement.contentEditable === 'true')) {{
                input = document.activeElement;
            }}
        }}

        if (input) {{
            input.focus();
            
            // For React/Frameworks, setting value directly might not work.
            // ExecCommand is safer for contentEditable, but input events are needed for Inputs.
            
            const text = "{PROMPT}";
            
            // Method 1: InsertText (Works for many)
            document.execCommand('insertText', false, text);
            
            // Method 2: Dispatch Input Events manually (Backup)
            if (input.value !== text && input.innerText !== text) {{
                 if (input.tagName === 'TEXTAREA' || input.tagName === 'INPUT') {{
                     let lastValue = input.value;
                     input.value = text;
                     let event = new Event('input', {{ bubbles: true }});
                     event.simulated = true;
                     let tracker = input._valueTracker;
                     if (tracker) {{ tracker.setValue(lastValue); }}
                     input.dispatchEvent(event);
                 }} else {{
                     input.innerText = text;
                 }}
            }}

            // Press Enter
            setTimeout(() => {{
                input.dispatchEvent(new KeyboardEvent('keydown', {{ key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }}));
                input.dispatchEvent(new KeyboardEvent('keypress', {{ key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }}));
                input.dispatchEvent(new KeyboardEvent('keyup', {{ key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }}));
            }}, 500);
            
            return "Command Sent (" + input.tagName + ")";
        }} else {{
            return "Input not found";
        }}
    }})();
    """

    msg = {"id": 202, "method": "Runtime.evaluate", "params": {"expression": js_code, "returnByValue": True}}
    s.sendall(create_ws_frame(json.dumps(msg)))
    
    # Read Result
    while True:
        chunk = s.recv(4096)
        if not chunk: break
        decoded, remainder = parse_ws_frame(chunk)
        if decoded:
            print(decoded)
            if '"id":202' in decoded.replace(" ", ""): break

    s.close()

if __name__ == "__main__":
    generate_image()
