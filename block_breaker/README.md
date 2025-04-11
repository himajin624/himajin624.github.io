# ブロック崩しゲーム

シンプルなブロック崩しゲームです。pygameを使用して作成されています。

## 必要条件

- Python 3.6以上
- pygame

## インストール方法

```bash
pip install pygame
```

## 実行方法

```bash
python -m block_breaker.main
```

## 操作方法

- 左矢印キーまたはAキー: パドルを左に移動
- 右矢印キーまたはDキー: パドルを右に移動

## ゲームのルール

1. パドルを使ってボールを跳ね返し、ブロックを壊していきます
2. すべてのブロックを壊すとゲームクリアです
3. ボールが下に落ちるとゲームオーバーです

## プロジェクト構造

```
block_breaker/
├── main.py              # ゲームのエントリーポイント
├── game.py              # メインゲームクラス
├── sprites/
│   ├── __init__.py
│   ├── paddle.py        # パドルクラス
│   ├── ball.py          # ボールクラス
│   └── block.py         # ブロッククラス
├── utils/
│   ├── __init__.py
│   └── constants.py     # 定数（色、サイズなど）
└── assets/
    ├── images/          # 画像ファイル
    ├── sounds/          # 音声ファイル
    └── fonts/           # フォントファイル
``` 