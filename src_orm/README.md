# SQLAlchemy 学習用サンプルプログラム

このディレクトリには、SQLAlchemy を学習するためのサンプルプログラムが含まれています。
SQLAlchemy は Python でデータベースを操作するための強力なライブラリです。

## 目次

1. [SQLAlchemy とは](#sqlalchemy-とは)
2. [SQLAlchemy Core と ORM](#sqlalchemy-core-と-orm)
3. [セットアップ](#セットアップ)
4. [使い方](#使い方)
5. [サンプルプログラムの説明](#サンプルプログラムの説明)
6. [よくある操作](#よくある操作)

## SQLAlchemy とは

SQLAlchemy は、Python でデータベースを操作するためのライブラリです。
以下のような特徴があります：

- **データベース抽象化**: PostgreSQL、MySQL、SQLite など、複数のデータベースに対応
- **SQL 生成**: Python のコードから SQL を自動生成
- **型安全性**: Python の型ヒントと組み合わせて使える
- **パフォーマンス**: 効率的なクエリ実行と接続プール管理

## SQLAlchemy Core と ORM

SQLAlchemy には、2 つの主要な使い方があります：

### SQLAlchemy Core

**SQLAlchemy Core** は、SQL に近い低レベルの API です。

**特徴:**

- テーブル定義を `Table` オブジェクトで記述
- クエリを `select()`, `insert()`, `update()`, `delete()` で記述
- より細かい制御が可能
- パフォーマンスを重視する場合に適している

**例:**

```python
from sqlalchemy import select, Table, Column, Integer, String

# テーブル定義
students = Table('students', metadata,
    Column('student_id', Integer, primary_key=True),
    Column('name', String(200))
)

# クエリ実行
query = select(students).where(students.c.name == '田中 一郎')
result = conn.execute(query)
```

### SQLAlchemy ORM

**SQLAlchemy ORM** (Object-Relational Mapping) は、データベースのテーブルを Python のクラスとして扱えます。

**特徴:**

- テーブルをクラスとして定義
- オブジェクト操作でデータベースを操作
- リレーションシップを簡単に扱える
- コードが読みやすく、保守しやすい

**例:**

```python
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# モデルクラス定義
class Student(Base):
    __tablename__ = 'students'
    student_id = Column(Integer, primary_key=True)
    name = Column(String(200))

# クエリ実行
session = SessionLocal()
student = session.query(Student).filter(Student.name == '田中 一郎').first()
```

### どちらを使うべきか？

- **Core**: SQL に慣れている、パフォーマンスを重視する、複雑なクエリが多い
- **ORM**: SQL を書きたくない、オブジェクト指向で書きたい、リレーションシップを簡単に扱いたい

多くの場合、**ORM から始めることをおすすめします**。必要に応じて Core も使えます。

## セットアップ

### 1. 必要なライブラリのインストール

```bash
pip install -r requirements.txt
```

または、個別にインストール：

```bash
pip install sqlalchemy psycopg2-binary python-dotenv
```

### 2. データベースの準備

このサンプルは PostgreSQL を想定していますが、SQLite でも動作します。

**PostgreSQL の場合:**

1. PostgreSQL をインストール
2. データベースを作成
3. `docs/sql/01_ddl.sql` と `docs/sql/02_seed.sql` を実行してテーブルとデータを作成

**SQLite の場合（簡単に試したい場合）:**

```python
# 接続URLを変更
DATABASE_URL = 'sqlite:///example.db'
```

### 3. 環境変数の設定

`.env` ファイルを作成して、データベース接続情報を設定してください：

```env
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

または、プログラム内で直接指定することもできます。

## 使い方

### Core のサンプルを実行

```bash
python core_example.py
```

### ORM のサンプルを実行

```bash
python orm_example.py
```

## サンプルプログラムの説明

### core_example.py

SQLAlchemy Core を使ったサンプルプログラムです。

**含まれる例:**

1. すべての生徒を取得
2. 条件付きで生徒を取得
3. 特定のカラムのみ取得
4. JOIN を使ったクエリ
5. 集計関数を使ったクエリ
6. GROUP BY を使った集計
7. INSERT でデータを追加
8. UPDATE でデータを更新
9. DELETE でデータを削除
10. 複数のテーブルを JOIN

### orm_example.py

SQLAlchemy ORM を使ったサンプルプログラムです。

**含まれる例:**

1. すべての生徒を取得
2. ID で生徒を取得
3. 条件で生徒をフィルタリング
4. リレーションシップを使う
5. JOIN を使ったクエリ
6. 集計関数を使う
7. GROUP BY を使った集計
8. 新しい生徒を作成
9. 生徒情報を更新
10. 生徒を削除
11. リレーションシップを先読み（Eager Loading）
12. 複雑なクエリ

## よくある操作

### Core でのよくある操作

#### SELECT（取得）

```python
from sqlalchemy import select

# すべて取得
query = select(students)
result = conn.execute(query)

# 条件付き
query = select(students).where(students.c.student_id == 101)
result = conn.execute(query)

# 特定のカラムのみ
query = select(students.c.name, students.c.email)
result = conn.execute(query)
```

#### INSERT（追加）

```python
from sqlalchemy import insert

query = insert(students).values(
    student_id=107,
    name='佐藤 花子',
    email='hanako@example.com',
    enrollment_date=datetime.now()
)
conn.execute(query)
conn.commit()
```

#### UPDATE（更新）

```python
from sqlalchemy import update

query = update(students).where(
    students.c.student_id == 101
).values(email='new@example.com')
conn.execute(query)
conn.commit()
```

#### DELETE（削除）

```python
from sqlalchemy import delete

query = delete(students).where(students.c.student_id == 107)
conn.execute(query)
conn.commit()
```

#### JOIN

```python
query = select(
    students.c.name,
    courses.c.title
).select_from(
    students.join(enrollments, students.c.student_id == enrollments.c.student_id)
    .join(courses, enrollments.c.course_id == courses.c.course_id)
)
```

### ORM でのよくある操作

#### SELECT（取得）

```python
# すべて取得
students = session.query(Student).all()

# IDで取得
student = session.query(Student).filter(Student.student_id == 101).first()

# 条件付き
students = session.query(Student).filter(
    Student.enrollment_date >= datetime(2024, 1, 1)
).all()
```

#### INSERT（追加）

```python
new_student = Student(
    student_id=107,
    name='佐藤 花子',
    email='hanako@example.com',
    enrollment_date=datetime.now()
)
session.add(new_student)
session.commit()
```

#### UPDATE（更新）

```python
student = session.query(Student).filter(Student.student_id == 101).first()
student.email = 'new@example.com'
session.commit()
```

#### DELETE（削除）

```python
student = session.query(Student).filter(Student.student_id == 107).first()
session.delete(student)
session.commit()
```

#### リレーションシップを使う

```python
student = session.query(Student).filter(Student.student_id == 101).first()
# 生徒の受講登録を取得
for enrollment in student.enrollments:
    print(enrollment.course.title)
```

#### JOIN

```python
results = session.query(Student.name, Course.title).join(
    Enrollment, Student.student_id == Enrollment.student_id
).join(
    Course, Enrollment.course_id == Course.course_id
).all()
```

## 重要なポイント

### セッション管理（ORM）

ORM を使う場合、セッションの管理が重要です：

```python
session = SessionLocal()
try:
    # データベース操作
    student = session.query(Student).first()
    session.commit()
except Exception as e:
    session.rollback()  # エラー時はロールバック
    raise
finally:
    session.close()  # 必ずセッションを閉じる
```

### トランザクション

複数の操作をまとめて実行する場合：

```python
session = SessionLocal()
try:
    # 複数の操作
    session.add(student1)
    session.add(student2)
    session.commit()  # すべて成功したらコミット
except Exception as e:
    session.rollback()  # エラーがあればロールバック
finally:
    session.close()
```

### N+1 問題（ORM）

リレーションシップを取得する際、クエリが多くなりすぎる問題：

**悪い例:**

```python
students = session.query(Student).all()
for student in students:
    # 各生徒ごとにクエリが実行される（N+1問題）
    print(student.enrollments)
```

**良い例（Eager Loading）:**

```python
from sqlalchemy.orm import joinedload

students = session.query(Student).options(
    joinedload(Student.enrollments)
).all()
# 一度のクエリで関連データも取得
```

## 参考資料

- [SQLAlchemy 公式ドキュメント](https://docs.sqlalchemy.org/)
- [SQLAlchemy Core チュートリアル](https://docs.sqlalchemy.org/en/20/core/tutorial.html)
- [SQLAlchemy ORM チュートリアル](https://docs.sqlalchemy.org/en/20/orm/tutorial.html)

## トラブルシューティング

### 接続エラー

- データベースが起動しているか確認
- 接続情報（ホスト、ポート、ユーザー名、パスワード）が正しいか確認
- ファイアウォールの設定を確認

### テーブルが見つからない

- `docs/sql/01_ddl.sql` を実行してテーブルを作成したか確認
- データベース名が正しいか確認

### インポートエラー

- `pip install -r requirements.txt` でライブラリをインストールしたか確認
- 仮想環境を使っている場合、正しい環境で実行しているか確認


