<div align="center">

# 🧠 Antigravity-Memory

### ～ 反重力の記憶 ～

<p align="center">
  <img src="https://img.shields.io/badge/Agent-Google%20Antigravity-blue?style=for-the-badge&logo=google" alt="Agent">
  <img src="https://img.shields.io/badge/Sync-3%20Macs-purple?style=for-the-badge&logo=apple" alt="Sync">
  <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge" alt="Status">
</p>

**Antigravityエージェントの日々の活動を記録し、複数Mac間で共有するメモリーバンク**

</div>

---

## 🌌 概要

このリポジトリは、**3台のMac**（職場・自宅など）で稼働するAntigravityエージェントの作業ログを一元管理するための**共有メモリ**です。

各Macで実行されたタスク、成果物、学習内容がここに蓄積され、どの端末からでもコンテキストを引き継いで作業を継続できます。

---

## 📂 構造

```
Antigravity-Memory/
├── logs/                    # 日次ログ
│   └── 2025/
│       └── 12/
│           └── 2025-12-29.md
├── sync-status.md           # 各Macの同期状態
└── README.md
```

---

## 🔄 同期方法

Antigravityで以下のコマンドを実行：

```
/daily-memory-sync
```

または手動で：
```bash
git pull origin main
# ログを追記
git add . && git commit -m "📝 [Mac名] YYYY-MM-DD セッションログ"
git push origin main
```

---

## 🖥️ 登録Mac一覧

| Mac ID | 場所 | 最終同期 |
|:-------|:-----|:---------|
| `motos-mac` | 自宅 | 2025-12-29 |
| `work-mac` | 職場 | - |
| `mac-3` | - | - |

---

<div align="center">

*Powered by YOROZU & Google Antigravity*

</div>
