# ✈️ Antigravity Flight Log: 2025-12-30

## 🎯 Daily Mission
- [x] Record "Agentic Browser & Rally Migration Guide" for multi-device sync

## 📝 Activity Log
| Time | Action | Outcome |
| :--- | :--- | :--- |
| 09:19 | **System Start** | Verified YOROZU Environment |
| 09:20 | **Memory Update** | Added Migration Guide to logs for sharing with other Macs |

## 📚 Shared Knowledge: Agentic Browser & Rally Migration Guide
*(Preserved for access on other machines)*

# Agentic Browser & Rally: 完全移行ガイド

このガイドは、新しいMacでも**「いつものChrome」**をそのまま使いながら、AI (Antigravity/Rally) に操作権限を与えるための設定手順です。
これにより、「AIが新しいウィンドウを勝手に開いて何もできない」状態を解消し、**「貴方のブラウザをAIが一緒に操作する」**状態を復元します。

---

## 理屈: 何が起きているのか？

通常、AIや自動化ツールは「真っさらなChrome」を起動しようとします。これが「ログインされていない別のブラウザ」が開く原因です。
**解決策:** 「いつものChrome」を、AIが接続できる**「受付窓口（デバッグポート9222）」を開けた状態で起動**します。

---

## 手順 1: ツール一式の配置

`llm-rally` フォルダを新しいMacに配置します（`~/Antigravity/llm-rally` 推奨）。

## 手順 2: Chromeの "Agentic起動" (最重要)

新しいMacで、以下のスクリプトを使ってChromeを起動します。
これは「いつものChrome」を起動しますが、AI用の裏口を開けておく魔法のコマンドです。

1.  **Chromeを完全に終了する (Cmd+Q)**
    *   ウィンドウを閉じるだけでなく、ドックのアイコンを右クリックして「終了」してください。

2.  **起動スクリプトを実行**
    ```bash
    cd ~/Antigravity/llm-rally
    chmod +x launch_main_chrome.sh
    ./launch_main_chrome.sh
    ```

    *   これで普段のChromeが立ち上がります。
    *   見た目は変わりませんが、AIが接続可能な状態になっています。

## 手順 3: Rally (Agentic Mode) の実行

これで、Rallyスクリプトが「いつものChrome」を使えるようになります。
以下のコマンドで実行してください。

```bash
# --cdp オプションで、先ほど起動したChromeに接続します
node rally.mjs --sites chatgpt,grok,mistral,gemini --cdp http://127.0.0.1:9222
```

このコマンドを打つと、**今開いているChrome**の中で、AIがタブを切り替えながら議論を始めます。ログインし直す必要はありません。

---

## 運用上の注意

*   **PC再起動後など**:
    Chromeを普通にアイコンから起動すると、AIは接続できません。AI操作が必要な作業をする時は、一度Chromeを終了し、`./launch_main_chrome.sh` から起動する癖をつけるとスムーズです。
*   **警告が出る場合**:
    Chromeの上部に「自動テストソフトウェアによって制御されています」というバーが出ることがありますが、正常です。

## 📜 Shared Script: launch_main_chrome.sh
*(Save this as `~/Antigravity/llm-rally/launch_main_chrome.sh` on new machines)*

```bash
#!/bin/bash

# Configuration
CHROME_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
# Standard Mac Chrome Profile Path
DEFAULT_PROFILE_DIR="$HOME/Library/Application Support/Google/Chrome"
DEBUG_PORT=9222

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Antigravity Agentic Browser Launcher (Main Profile) ===${NC}"
echo "This script enables AI control over your MAIN Chrome browser."

# Check if Chrome is running
if pgrep -f "Google Chrome" > /dev/null; then
    # Check if it's already debuggable
    if lsof -i :$DEBUG_PORT > /dev/null; then
        echo -e "${GREEN}Success: Chrome is already running and ready for Agentic Control!${NC}"
        exit 0
    else
        echo -e "${RED}⚠️  Action Required: Chrome is running but NOT controllable.${NC}"
        echo "To give the AI eyes and hands, we must restart Chrome with special flags."
        echo -e "${YELLOW}Please Quit Google Chrome completely (Cmd+Q) and run this script again.${NC}"
        exit 1
    fi
fi

echo "Launching Main Chrome Profile with Agentic Access..."

# Launch command
# We do NOT specify --user-data-dir ensures it uses the default system profile
"$CHROME_PATH" \
  --remote-debugging-port=$DEBUG_PORT \
  --restore-last-session \
  &

echo -e "${GREEN}Chrome launched!${NC}"
echo "You can now use your browser as usual."
echo "The AI (Antigravity/Rally) can now connect to your open tabs."
```
