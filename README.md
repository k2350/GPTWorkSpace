# Outline Transformer

Markdown形式の資料骨子を、用途別のドキュメントテンプレートに変換するCLIツールです。

## 使い方

```bash
python3 outline_transformer.py <入力.md> --style <report|proposal|minutes> -o <出力.md>
```

### 実行例

```bash
python3 outline_transformer.py problem_book_outline.md --style proposal -o generated_output/problem_book_outline_proposal.md
```

## 変換スタイル

- `report`: 報告書ドラフト
- `proposal`: 提案書ドラフト
- `minutes`: 議事録テンプレート
