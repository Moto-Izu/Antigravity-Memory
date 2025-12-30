import os
import time
import sys
import random

# --- AGO: ANTIGRAVITY ORBIT ---
# AI Model Quota Monitoring System

C_RESET = "\033[0m"
C_BRAND = "\033[48;5;51m\033[38;5;16m" # Neon Cyan background, black text
C_VALUE = "\033[38;5;51m"
C_LABEL = "\033[38;5;244m"
C_WARN  = "\033[38;5;208m"

def get_quotas():
    # Mock data - in a real scenario, this would poll APIs or local usage logs
    return {
        "GEMINI": f"{random.randint(70, 95)}%",
        "GPT-4o": "READY",
        "CLAUDE": f"{random.randint(10, 30)}/50",
        "LATENCY": f"{random.randint(20, 100)}ms"
    }

def draw_bar():
    quotas = get_quotas()
    
    brand = f"{C_BRAND} AGO / ORBIT {C_RESET}"
    items = []
    for k, v in quotas.items():
        color = C_VALUE
        if "/" in v:
            used, total = v.split("/")
            if int(used) > int(total) * 0.8:
                color = C_WARN
        
        items.append(f"{C_LABEL}{k}:{C_RESET} {color}{v}{C_RESET}")
    
    bar = f" {brand} {'  '.join(items)}"
    sys.stdout.write("\r" + bar + " " * 10)
    sys.stdout.flush()

def main():
    try:
        # Hide cursor
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()
        
        while True:
            draw_bar()
            time.sleep(2)
    except KeyboardInterrupt:
        # Show cursor
        sys.stdout.write("\033[?25h\n")
        sys.stdout.flush()
        print("Orbit Disengaged.")

if __name__ == "__main__":
    main()
