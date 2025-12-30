---
description: フライトログから日次漫画を自動生成する
---

# /generate-daily-manga ワークフロー

フライトログ（Antigravity-Memory）から今日の活動を4コマ漫画化します。

## 前提条件

- Kamui MCP (kamui-t2i) が接続されていること
- Antigravity-Memoryにフライトログが存在すること

---

## ワークフロー手順

### 1. フライトログを確認

```bash
cat /Users/motos/Antigravity/GAS_PROJECT/Antigravity-Memory/logs/2025/12/$(date +%Y-%m-%d).md
```

または、GitHubからCDP経由で取得。

### 2. シナリオを作成

フライトログから**2つのハイライト**を抽出し、各4コマのシナリオを作成：

- **Page 1**: 午前/メインタスク
- **Page 2**: 午後/サブタスク or まとめ

### 3. Nano Banana Proで生成

以下のベースプロンプトを使用（`/Users/motos/Antigravity/tools/manga_template.md` 参照）：

```
cute manga style illustration, 4-koma panel layout (4 panels vertically arranged), 
TWO MAIN CHARACTERS: 
1) Human character with short buzz cut hair with subtle gray streaks, wearing stylish glasses, soft gentle expression, Japanese male tech worker 
2) AI assistant character as a cute floating holographic robot/sphere with glowing cyan eyes named "Antigravity",

Panel 1: [Description + Dialogue "Quote"]
Panel 2: [Description + Dialogue "Quote"]
Panel 3: [Description + Dialogue "Quote"]
Panel 4: [Description + Dialogue "Quote"]

soft pastel colors, clean lineart, professional manga quality, tech workflow visualization, human-AI collaboration friendship, speech bubbles with Japanese text, high quality
```

### 4. 生成リクエスト

```
mcp_kamui-t2i_nano_banana_pro_t2i_submit でプロンプトを送信
```

### 5. 結果取得 & 保存

生成完了後、URLをフライトログに追記：

```markdown
## 📖 今日の漫画日誌

- Page 1: [URL]
- Page 2: [URL]
```

---

## キャラクター設定（固定）

| キャラ | 特徴 |
|:---|:---|
| 人間（あなた） | バズカット、グレー混じり、メガネ、穏やか |
| Antigravity | 浮遊ホログラムAI、シアン光る目、かわいい |

---

## 生成例

### 2025-12-29

**テーマ**: YOROZU設定 & Memory共有システム構築

**Page 1**: https://v3b.fal.media/files/b/0a883a4f/4VlsMvnffoRlhAAtWvZaf.png
**Page 2**: https://v3b.fal.media/files/b/0a883a50/bu5w9ghSRaYDobzh88dRN.png

---

*Last updated: 2025-12-29*
