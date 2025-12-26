# FastAPI + SQLAlchemy シンプル実装

このプロジェクトは、SQLAlchemy と FastAPI を使った最もシンプルな API 実装です。
学習管理システムのデータを扱います。

## セットアップ

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2. データベース接続の設定

`.env`ファイルを作成して、データベース接続情報を設定してください：

```env
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/dbname
```

**注意**: `psycopg`（psycopg3）を使用するため、接続文字列は`postgresql+psycopg://`で始める必要があります。

### 3. データベースの準備

`docs/sql/`配下の SQL ファイルを使ってデータベースをセットアップしてください：

1. `01_ddl.sql`でテーブルを作成
2. `02_seed.sql`でサンプルデータを投入

### 4. アプリケーションの起動

```bash
uvicorn main:app --reload
```

アプリケーションは `http://localhost:8000` で起動します。

## API エンドポイント

### ヘルスチェック

- `GET /` - ルートエンドポイント
- `GET /health` - ヘルスチェック

### Students（生徒）

- `GET /students` - 全生徒を取得（クエリパラメータ: `skip`, `limit`）
- `GET /students/{student_id}` - 特定の生徒を取得
- `POST /students` - 新しい生徒を作成

### Courses（コース）

- `GET /courses` - 全コースを取得（クエリパラメータ: `skip`, `limit`）
- `GET /courses/{course_id}` - 特定のコースを取得
- `POST /courses` - 新しいコースを作成

## API ドキュメント

アプリケーション起動後、以下の URL で自動生成された API ドキュメントを確認できます：

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 使用例

### 生徒一覧を取得

```bash
curl http://localhost:8000/students
```

### 特定の生徒を取得

```bash
curl http://localhost:8000/students/101
```

### 新しい生徒を作成

```bash
curl -X POST http://localhost:8000/students \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": 107,
    "name": "佐藤 花子",
    "email": "hanako.sato@example.com",
    "enrollment_date": "2024-03-01T10:00:00"
  }'
```

## 使用技術について

このプロジェクトで使用している主要な技術について説明します。

### FastAPI

FastAPI は、Python で Web API を構築するためのモダンなフレームワークです。

**主な特徴：**

- **高速**: Node.js や Go と同等の高いパフォーマンスを実現
- **自動ドキュメント生成**: API の仕様書（Swagger UI や ReDoc）を自動で生成してくれる
- **型ヒント対応**: Python の型ヒントを使って、コードを書くだけで API の仕様が明確になる
- **シンプルな記述**: デコレータ（`@app.get()`など）を使うだけで、簡単に API エンドポイントを定義できる

このプロジェクトでは、`main.py`で FastAPI のアプリケーションインスタンスを作成し、各エンドポイントを定義しています。

### Pydantic

Pydantic は、データのバリデーション（検証）とシリアライゼーション（データの変換）を行うためのライブラリです。

**主な特徴：**

- **型に基づいたバリデーション**: Python の型ヒントを使って、データが正しい形式かどうかを自動でチェック
- **エラーメッセージが分かりやすい**: データが不正な場合、どこが問題なのかを明確に教えてくれる
- **JSON との変換が簡単**: Python のオブジェクトと JSON を簡単に変換できる

このプロジェクトでは、`schemas.py`で Pydantic のモデルを定義し、API のリクエストやレスポンスのデータ構造を定義しています。例えば、生徒データを作成する際に、必要な項目が揃っているか、データ型が正しいかを自動でチェックしてくれます。

### Uvicorn

Uvicorn は、FastAPI アプリケーションを動かすための ASGI サーバーです。（Asynchronous Server Gateway Interface）

**主な特徴：**

- **ASGI 対応**: 非同期処理に対応したサーバーで、高速にリクエストを処理できる
- **開発に便利**: `--reload`オプションを使うと、コードを変更すると自動で再起動してくれる
- **本番環境でも使用可能**: 開発環境だけでなく、本番環境でも使える実用的なサーバー

このプロジェクトでは、`uvicorn main:app --reload`というコマンドでアプリケーションを起動します。`main:app`は「`main.py`ファイルの中の`app`という変数」を指しており、FastAPI のアプリケーションインスタンスを指定しています。

## プロジェクト構成

```
src_fast_api/
├── main.py          # FastAPIアプリケーションのエントリーポイント
├── database.py      # データベース接続とセッション管理
├── models.py        # SQLAlchemyモデル定義
├── schemas.py       # Pydanticスキーマ定義（リクエスト/レスポンス）
├── requirements.txt # 依存関係
└── README.md       # このファイル
```

## 注意事項

- この実装は学習用のサンプルコードです。本番環境で使用する場合は、エラーハンドリング、認証、バリデーションなどを追加してください。
- データベース接続情報は環境変数で管理することを推奨します。
