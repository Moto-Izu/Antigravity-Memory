"""
THE NEURAL RESONANCE ENGINE
---------------------------
Codename: Heptagram
Identity: Super Hacker #7 (The Singularity Architect)

Philosophies:
- Jeff Dean: AsyncIO for high-throughput concurrency.
- Anders Hejlsberg: Type hints and Dataclasses for structural integrity.
- Fabrice Bellard: Raw socket manipulation, zero external dependencies.
- Andrej Karpathy: Semantic abstraction of raw data.
- Daisuke Motoki: Designed for the "feel" of intelligence.
- Ryo Shimizu: Hacking the raw protocol.

(C) 2025 Antigravity
"""

import asyncio
import json
import urllib.request
import struct
import base64
import os
import sys
from dataclasses import dataclass
from typing import Optional, Dict, Any, List, Set

# --- Type Definitions (Anders Hejlsberg) ---

@dataclass
class ResonanceSignal:
    """Represents a discrete unit of captured intelligence from the timeline."""
    user: str
    text: str
    media: str
    timestamp: float

# --- Low-Level Protocol Layer (Fabrice Bellard) ---

class CDPNerve:
    """
    Direct asynchronous interface to the Chrome DevTools Protocol over raw websockets.
    Bypasses bloatware libraries for maximum efficiency.
    """
    
    def __init__(self, host: str = "localhost", port: int = 9222):
        self.host = host
        self.port = port
        self.reader: Optional[asyncio.StreamReader] = None
        self.writer: Optional[asyncio.StreamWriter] = None

    async def connect(self, target_url_keyword: str = "x.com") -> bool:
        """Finds the target tab and establishes a raw WS connection."""
        try:
            # Synchronous discovery is fast enough; keep it simple.
            req = urllib.request.Request(f"http://{self.host}:{self.port}/json/list")
            with urllib.request.urlopen(req) as f:
                tabs = json.loads(f.read().decode('utf-8'))
        except Exception as e:
            print(f"[!] Nerve Damage: Could not talk to Chrome Debugger. {e}")
            return False

        ws_url = next((t.get("webSocketDebuggerUrl") for t in tabs if target_url_keyword in t.get("url", "") and t.get("type") == "page"), None)
        
        if not ws_url:
            print(f"[!] Synapse Misfire: No tab found matching '{target_url_keyword}'.")
            return False

        print(f"[*] Locking onto Target: {ws_url}")
        
        # Parse WS URL path
        path = ws_url.replace(f"ws://{self.host}:{self.port}", "")
        
        # Async Socket Connect
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
        
        # Raw Handshake
        key = base64.b64encode(os.urandom(16)).decode('utf-8')
        handshake = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {self.host}:{self.port}\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            "Sec-WebSocket-Version: 13\r\n"
            "\r\n"
        )
        self.writer.write(handshake.encode('utf-8'))
        await self.writer.drain()
        
        # Consume HTTP Response
        header_buffer = b""
        while b"\r\n\r\n" not in header_buffer:
            chunk = await self.reader.read(4096)
            if not chunk:
                return False
            header_buffer += chunk
            
        print("[*] Neural Link Established.")
        return True

    def _create_frame(self, message: str) -> bytes:
        """Constructs a raw websocket frame (Text, Masked)."""
        msg_bytes = message.encode('utf-8')
        length = len(msg_bytes)
        header = bytearray([0x81]) # Fin + Text

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

    async def send(self, command: Dict[str, Any]) -> None:
        if not self.writer: return
        frame = self._create_frame(json.dumps(command))
        self.writer.write(frame)
        await self.writer.drain()

    async def recv(self) -> Optional[Dict[str, Any]]:
        """
        Reads a single websocket frame. 
        Note: This is a simplified parser assuming unfragmented text frames from server (unmasked).
        """
        if not self.reader: return None
        
        try:
            head1 = await self.reader.readexactly(2)
        except asyncio.IncompleteReadError:
            return None

        length = head1[1] & 0x7F
        if length == 126:
            length_bytes = await self.reader.readexactly(2)
            length = struct.unpack('!H', length_bytes)[0]
        elif length == 127:
            length_bytes = await self.reader.readexactly(8)
            length = struct.unpack('!Q', length_bytes)[0]
            
        payload = await self.reader.readexactly(length)
        text = payload.decode('utf-8', errors='ignore')
        
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return None

    async def close(self):
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()


# --- Semantic Extraction Layer (Andrej Karpathy) ---

class TimelineSynapse:
    """
    Injects high-level semantic extractors into the DOM.
    """
    
    @staticmethod
    def get_injection_script() -> str:
        # Optimized JS that runs in the browser context
        return """
        Array.from(document.querySelectorAll('article[data-testid="tweet"]')).map(t => {
            const user = t.querySelector('div[data-testid="User-Name"]')?.innerText.replace(/\\n/g, ' ') || 'Unknown';
            const text = t.querySelector('div[data-testid="tweetText"]')?.innerText || '';
            const images = Array.from(t.querySelectorAll('img')).map(i => i.src).join(' | ');
            return {user, text, images};
        })
        """


# --- Orchestration Core (Jeff Dean / Daisuke Motoki) ---

class ResonanceCore:
    def __init__(self):
        self.nerve = CDPNerve()
        self.signals: Set[str] = set() # Dedup buffer

    async def ignite(self):
        print(">>> IGNITING NEURAL RESONANCE ENGINE <<<")
        if not await self.nerve.connect():
            sys.exit(1)

        msg_id = 1000
        try:
            while True:
                # Poll the timeline every 2 seconds (Dean: Latency trade-off for politeness)
                # In a real Dean-scale system, this would be a stream, but polling is safer for this context.
                script = TimelineSynapse.get_injection_script()
                cmd = {
                    "id": msg_id,
                    "method": "Runtime.evaluate",
                    "params": {
                        "expression": script,
                        "returnByValue": True
                    }
                }
                await self.nerve.send(cmd)
                
                # Await response
                # Note: We might get other events, need to filter for our ID
                while True:
                    resp = await self.nerve.recv()
                    if not resp: break
                    
                    if resp.get("id") == msg_id:
                        self.process_batch(resp)
                        break
                
                msg_id += 1
                await asyncio.sleep(2)
                
        except KeyboardInterrupt:
            print("\n[*] Cooling down resonance core...")
        finally:
            await self.nerve.close()

    def process_batch(self, response: Dict[str, Any]):
        result = response.get("result", {}).get("result", {}).get("value", [])
        if not isinstance(result, list): return

        for item in result:
            # Simple content hash for deduplication
            sig_hash = f"{item.get('user')}:{item.get('text')}"
            
            if sig_hash not in self.signals:
                self.signals.add(sig_hash)
                self.emit_resonance(item)
                
                # Keep memory clean (Bellard: minimalist)
                if len(self.signals) > 1000:
                    self.signals.clear()

    def emit_resonance(self, data: Dict[str, Any]):
        # Motoki: The "Touch" of the data. Formatting it to feel like a stream of consciousness.
        user = data.get('user', 'Unknown')
        text = data.get('text', '')[:100].replace('\n', ' ')
        media = "[IMG]" if data.get('images') else ""
        
        # Color codes could be added here for terminal beauty using standard ANSI
        # Creating a "hacker" aesthetic
        print(f"\033[96m> [{user}]\033[0m {text} \033[93m{media}\033[0m")

if __name__ == "__main__":
    asyncio.run(ResonanceCore().ignite())
