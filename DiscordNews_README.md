# 📺 Discord Daily News Generator

Discordサーバーの1日の活動ログを収集・整形し、Google NotebookLMを使って「ニュース動画（Video Overview）」を作成するためのツールセットです。

## 📦 同梱ファイル

| ファイル名 | 役割 |
| :--- | :--- |
| `fetch_discord_messages.py` | Discord APIを叩いてメッセージを収集・JSON保存するスクリプト |
| `format_messages.py` | 収集したJSONをNotebookLMが読みやすいMarkdown形式に整形するスクリプト |
| `requirements.txt` | 必要なPythonライブラリ一覧 |
| `.env.example` | 設定ファイルの雛形（トークン・チャンネルID） |

## 🚀 使い方

### 1. 準備 (初回のみ)

Pythonライブラリをインストールします。

```bash
pip3 install -r requirements.txt
```

`.env` ファイルを作成し、DiscordのトークンとサーバーIDを設定します。
（`.env.example` をコピーしてリネームしてください）

```env
DISCORD_TOKEN=あなたのユーザートークン
DISCORD_GUILD_ID=対象サーバーのID
# 特定のチャンネルだけ抜きたい場合は以下を設定（空なら全チャンネル）
DISCORD_CHANNEL_IDS=
```

### 2. データ収集 (毎日)

その日のログを吸い出します（デフォルトは `2025-12-29` になっています。日付を変える場合はスクリプト内の `TARGET_DATE` を編集してください ※後日引数化予定）。

```bash
python3 fetch_discord_messages.py
```

成功すると `discord_export_YYYY-MM-DD.json` が生成されます。

### 3. データ整形

NotebookLM用にデータを加工します。

```bash
python3 format_messages.py
```

成功すると `discord_news_source_YYYY-MM-DD.txt` が生成されます。

### 4. 動画生成

1.  Google NotebookLM を開きます。
2.  生成された `.txt` ファイルをアップロードします。
3.  **「Video Overview (動画の概要)」** ボタンをクリックします。
4.  AIがスライド付きのニュース動画を生成してくれます！

## ⚠️ 注意事項

- **トークンの取り扱い**: `.env` ファイルには個人のDiscordトークンが含まれます。**絶対にGitHubなどの公開リポジトリに `.env` をアップロードしないでください！** （`.gitignore` に追加済みであることを確認してください）
- **利用規約**: ユーザーアカウントでのスクリプト利用（Self-Botting）はDiscordの規約上グレーゾーンです。個人利用の範囲に留め、頻繁なリクエストは控えてください。
