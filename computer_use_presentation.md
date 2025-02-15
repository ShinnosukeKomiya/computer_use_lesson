---
marp: true
theme: gaia
class: invert
# スライド全体のデザイン調整用のCSSを適宜追加
style: |
  section {
    font-family: "Hiragino Sans","Noto Sans JP",sans-serif;
  }
  h1, h2, h3 {
    font-weight: 600;
  }
  .highlight {
    color: #007acc;
    font-weight: bold;
  }
  .emphasis {
    background-color: #fffae6;
    padding: 0.2em 0.4em;
    border-radius: 4px;
  }
  code {
    background-color: #eee;
    color: #333;
    padding: 2px 4px;
    border-radius: 4px;
  }
header: "**Computer Use勉強会**"
footer: "by **社内勉強会**"
paginate: true
backgroundColor: #f8f8f8
---

<!-- _class: lead -->
# Computer Use勉強会

## AIによるインタラクティブなシステム操作の実現

**〜生産性とUXを革新する次世代の自動操作プラットフォーム〜**

---

# アジェンダ

1. **Computer Useの概要と意義**
2. **デモンストレーション：AIによる画面操作の流れ**
3. **技術要素の詳細解説**
   - マルチモーダル入力処理
   - システムプロンプトとChain-of-Thought
   - ツール統合による操作コマンド
   - プロンプトキャッシングによる最適化
   - ストリーミングレスポンスの活用
4. **開発・運用上のポイント**  ← **NEW!**
   - フレームワーク選定 & 既存RPAとの比較
   - エラーリカバリとテスト戦略
   - セキュリティ・プライバシー対策
5. **課題とベストプラクティス**
6. **質疑応答・ディスカッション & ハンズオン予告**  ← **NEW!**

---

# Computer Useの概要

- **定義**
  AIが画面情報（画像・テキスト等）を解析し、**ユーザーに代わって操作（クリック、入力、スクロール等）を自動実行**する仕組み

- **背景と目的**
  - 定型業務の自動化やオペレーションミスの低減
  - **RPA**以上に柔軟で、**UI/UXを深く理解する操作ロジック**を構築
  - **業務効率と品質向上**を両立

- **活用例**
  - ブラウザ操作の自動化（フォーム入力、スクレイピング など）
  - Webアプリ/ネイティブアプリ上でのガイド付き操作
  - カスタマーサポート用のオペレーター支援

---

# デモンストレーションの流れ

1. **入力**
   - 画面キャプチャやセンサーデータを取得
   - （例：スクリーンショット, ウィンドウ情報）

2. **解析**
   - AIモデルが画像やテキスト情報を解析し、画面構造・状態を把握

3. **操作決定**
   - システムプロンプトとChain-of-Thoughtに基づき、**最適な操作(次のクリック箇所など)**を決定

4. **実行 & フィードバック**
   - ツール統合で操作コマンドを実行し、結果をリアルタイムで確認（ストリーミング）

---

# マルチモーダル入力処理

- **目的**
  複数のデータソース（画像、テキスト、UI要素の座標など）を融合して、**文脈に応じた意思決定**を行う

- **具体例**
  1. 画面キャプチャを取得 -> base64エンコード
  2. 補助テキスト（HTMLのDOM情報など）
  3. マウスポインタの位置やクリック履歴などのログ

```python
def create_image_message(image_path):
    with open(image_path, "rb") as f:
        data = base64.b64encode(f.read()).decode('utf-8')
    return {"type": "image", "data": data}
```

- **応用Tips**
  - DOMツリーやコンポーネント構造を合わせて送ることで、**より正確なUI認識**を可能に
  - 画像内テキストをOCRしてテキスト化するなどの前処理

---

# システムプロンプトとChain-of-Thought

- **システムプロンプトの役割**
  - AIへの「初期方針」を与える。**動作ルールや制約**も含め、ブレない軸を定義
  - 例：「画面内の重要要素を優先し、ユーザーが求めるタスク達成を導く操作手順を考案せよ」

- **Chain-of-Thought**
  - 思考過程を段階的に書き出すことで、**説明可能性**を高めたり、**デバッグ**を容易にする
  - 例：
    1. 画面全体の構造把握
    2. 特定UI要素の位置特定
    3. 操作シナリオ(クリック or 入力 or スクロール)の選択

- **実装のポイント**
  - **プロンプトが肥大化しがち** → 分割やテンプレート管理でメンテナンス性を確保
  - Chain-of-Thoughtをユーザーに返す/返さない等の情報制御(セキュリティ)

---

# ツール統合と操作コマンド

- **概念**
  - クリックやキーボード入力、スクロールなどを**汎用コマンド化**してAIから呼び出せるようにする

- **実装例**

```python
tools = [
  {
    "name": "click",
    "description": "指定座標をクリックする",
    "input_schema": {"x": "number", "y": "number"}
  },
  {
    "name": "input_text",
    "description": "テキスト入力",
    "input_schema": {"text": "string"}
  }
]
```

- **メリット**
  - モジュール分割により、**単体テスト**が容易
  - 「クリック可能かどうか」「要素が画面内にあるか」などの検証ロジックを**共通化**できる

- **発展**
  - 「ダブルクリック」「ドラッグ&ドロップ」「要素ハイライト」などの拡張コマンド導入
  - **他システムやAPI**への連携（例：ファイルアップロード先のクラウドストレージ操作）

---

# プロンプトキャッシングと最適化

- **背景**
  - LLMなどを使う場合、**推論コスト**が高くなる
  - 同じ操作判断を何度も再計算するのは非効率

- **実装上の注意点**
  1. キャッシュキー設計：
     - 入力画像のハッシュ値や操作コンテキストをキーにする
  2. TTL(有効期限)：
     - 5分〜30分など運用に応じて調整
  3. **キャッシュヒット率向上**と、誤ったキャッシュ再利用リスクのトレードオフ

- **効果**
  - 大量バッチ処理時の応答速度向上
  - リアルタイム性が必要なUIでの**レスポンス向上**

---

# ストリーミングレスポンスの活用

- **特徴**
  - AIの推論結果を段階的に受け取り、**ユーザーへ即時フィードバック**
  - 長時間待ち時間のストレスを軽減し、**進捗可視化**を可能に

```python
with client.messages.stream(
    max_tokens=1024,
    messages=[{"role": "user", "content": "操作開始"}],
    model=MODEL_NAME,
) as stream:
    for text_chunk in stream.text_stream:
        handle_partial_output(text_chunk)  # 画面に随時表示
```

- **開発Tips**
  - 部分的な結果が返る前提でUIを作る必要がある
  - 非同期処理や**WebSocket**との組み合わせでスムーズなUXを実装

---

# 各技術の統合フロー

1. **入力取得**
   - マルチモーダル（画像、DOM、コンテキストなど）

2. **解析と判断**
   - システムプロンプト & Chain-of-Thoughtで操作ロジックを決定

3. **操作コマンドの発行**
   - ツール統合によるクリック/入力/スクロール等

4. **最適化処理**
   - プロンプトキャッシングで重複推論を削減

5. **フィードバック**
   - ストリーミングレスポンスでユーザーへ結果を即時還元

> 実際にはシステム構成図などを入れて視覚的にまとめると効果的

---

# 開発・運用上のポイント

## 1. フレームワーク選定 & 既存RPAとの比較

- **RPAツール（UiPath, Automation Anywhere等）**
  - GUI操作に特化しワークフローが組みやすいが、**細かい分岐ロジック**や**自然言語処理**は苦手
- **Computer Use(LLM)アプローチ**
  - 高い柔軟性・汎用性を持ち、UIの変化にも**言語理解**をベースに適応が可能
  - ただしLLM依存コストや**学習モデルの更新管理**が必要

> 使い分けとして、**「複雑な画面変化に対応したい」「自然言語を活かした操作をしたい」**場合にLLMが有効

---

## 2. エラーリカバリとテスト戦略

- **AI推論エラーの種類**
  - **部分的ミス**: 「クリック場所を微妙に外す」など
  - **論理的ミス**: 不要なステップを挟む、誤った順序で操作する

- **対策**
  - **座標クリック**だけでなくUI要素IDやテキストラベルを用いて冗長化
  - 重要ステップ前後でスクリーンショット比較やコンディションチェックを挿入

- **テストの自動化**
  - シナリオごとに入力データを変化させ、**回帰テスト/リグレッションテスト**を実行
  - **CI/CDパイプライン**でAIモデルと操作ロジックの継続検証

---

## 3. セキュリティ・プライバシー対策

- **画面キャプチャの取り扱い**
  - 機密情報が含まれる可能性
  - **アクセス権限**や**保存先の暗号化**を明確に

- **LLMへの送信データ**
  - **社外クラウドAPI**を使う場合、やり取りするデータに要注意
  - **匿名化やマスキング**を実施し、個人情報や機密情報を直接送信しない

> **運用フェーズ**では、ログやキャッシュデータの削除ポリシーなど**ガバナンス**を整備

---

# 課題とベストプラクティス

- **現状の課題**
  1. レイテンシーと正確性のバランス
  2. エラー発生時の自動リカバリ / フォールバック
  3. セキュリティ面の懸念（情報流出、モデル品質）

- **ベストプラクティス**
  - **小さな単位**でのモジュールテスト & 統合テスト
  - **Chain-of-Thought**のログを追いやすくして、問題判定を迅速に
  - **コンプライアンス**に配慮した環境構築（オンプレモデル or セキュアなAPI）

---

# まとめと今後の展望

- **まとめ**
  - Computer Useは、**マルチモーダル入力、LLMプロンプト、ツール統合**など複数技術の融合
  - **業務効率**と**UI/UX革新**の両方に貢献する可能性

- **今後の展望**
  - **強化学習**や**注意メカニズム**を活用した、**自律的操作最適化**
  - 社内オンプレ環境でのLLMホスティング、**プライバシー保護強化**
  - 音声指示・AR/VRとの連携など、更なる**マルチモーダル**拡張

> **最先端の自動化手法**として進化を続ける分野です。一緒にアップデートを追いかけましょう！

---

<!-- _class: lead -->
# ご清聴ありがとうございました
