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

def analyze_higgsfield():
    # 1. Get Tab
    try:
        req = urllib.request.Request("http://localhost:9222/json/list")
        with urllib.request.urlopen(req) as f:
            tabs = json.loads(f.read().decode('utf-8'))
    except Exception as e:
        print(f"HTTP Error: {e}")
        return

    # Look for likely Higgfield tab
    ws_url = next((t.get("webSocketDebuggerUrl") for t in tabs if "higgsfield.ai" in t.get("url", "")), None)
    if not ws_url:
        print("Error: Higgsfield tab not found.")
        # Fallback to active tab info if specific URL match failed but user said they are there
        return

    # 2. Connect
    print(f"Connecting to: {ws_url}...")
    path = ws_url.replace("ws://localhost:9222", "")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5.0) # 5 seconds timeout
    try:
        s.connect(('localhost', 9222))
        key = base64.b64encode(os.urandom(16)).decode('utf-8')
        s.sendall(f"GET {path} HTTP/1.1\r\nHost: localhost:9222\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n".encode())
        
        # Handshake Read
        buffer = b""
        while b"\r\n\r\n" not in buffer:
            chunk = s.recv(4096)
            if not chunk: raise Exception("Socket closed during handshake")
            buffer += chunk
        print("Handshake Complete.")

    except Exception as e:
        print(f"Connection Error: {e}")
        return

    # 3. Analyze DOM Structure (Summary)
    js_code = """
    (function() {
        const text = document.body.innerText.substring(0, 1000).replace(/\\n/g, ' :: ');
        const inputCount = document.querySelectorAll('input').length;
        const buttonCount = document.querySelectorAll('button').length;
        return `Prewview: ${text}\\nInputs: ${inputCount}, Buttons: ${buttonCount}`;
    })();
    """
    print("Sending DOM analysis command...")

    msg = {"id": 304, "method": "Runtime.evaluate", "params": {"expression": js_code, "returnByValue": True}}
    s.sendall(create_ws_frame(json.dumps(msg)))
    
    # Read Result
    buffer = b""
    while True:
        try:
            chunk = s.recv(8192)
            if not chunk: break
            buffer += chunk
            
            decoded, remainder = parse_ws_frame(buffer)
            if decoded:
                try:
                    data = json.loads(decoded)
                    if data.get("id") == 304:
                        print(data.get("result", {}).get("result", {}).get("value", "No Result"))
                        break
                except: pass
                # Reset buffer to remainder if we want to handle multiple messages, 
                # but we only care about one here.
                buffer = remainder
            else:
                # Need more data, loop again
                pass
        except socket.timeout:
            print("Timeout.")
            break

    s.close()

if __name__ == "__main__":
    analyze_higgsfield()
