# DDL（データ定義言語）実践トレーニング

このドキュメントでは、データベースの構造を定義・変更するための **DDL（Data Definition Language）** 文を学びます。テーブルの作成、変更、削除の方法を実際に手を動かしながら身につけましょう。

- スキーマ定義: `sql/01_ddl.sql`
- サンプルデータ投入: `sql/02_seed.sql`

**実行環境**: Supabase（PostgreSQL ベース）を想定しています。

---

## DDL とは

DDL（Data Definition Language）は、データベースの**構造**を定義・変更するための SQL 文です。データベースの「設計図」を作成・変更するための言語と考えるとわかりやすいでしょう。

### DDL の主なコマンド

- **CREATE**: テーブル、インデックス、ビューなどのオブジェクトを作成
- **ALTER**: 既存のテーブル構造を変更（カラム追加、削除など）
- **DROP**: テーブル、インデックス、ビューなどを削除
- **TRUNCATE**: テーブルの全データを削除（構造は残す）

---

## CREATE TABLE - テーブルの作成

CREATE TABLE 文は、新しいテーブルを作成するための SQL 文です。

### CREATE TABLE 文の基本構文

```sql
CREATE TABLE テーブル名 (
  カラム名1 データ型 [制約],
  カラム名2 データ型 [制約],
  カラム名3 データ型 [制約],
  ...
  [テーブル制約]
);
```

### 主なデータ型（PostgreSQL）

- **INT / INTEGER**: 整数
- **VARCHAR(n)**: 可変長文字列（最大 n 文字）
- **TEXT**: 長い文字列（制限なし）
- **DECIMAL(p, s)**: 固定小数点（p: 全体の桁数、s: 小数部の桁数）
- **TIMESTAMP**: 日時
- **DATE**: 日付
- **BOOLEAN**: 真偽値（true/false）

### 主な制約

- **PRIMARY KEY**: 主キー（一意で NULL 不可）
- **NOT NULL**: NULL 値を許可しない
- **UNIQUE**: 一意制約（重複を許可しない）
- **FOREIGN KEY**: 外部キー（他のテーブルを参照）
- **DEFAULT**: デフォルト値
- **CHECK**: 値の範囲チェック

---

## 演習 1: CREATE TABLE - 基本的なテーブル作成

### 1-1) シンプルなテーブルを作成

`teachers` テーブルを作成してください。以下のカラムを持ちます：

- `teacher_id`: INT、主キー
- `name`: VARCHAR(200)、NOT NULL
- `email`: VARCHAR(200)、NOT NULL、UNIQUE
- `created_at`: TIMESTAMP、NOT NULL

**解答例**:

```sql
CREATE TABLE teachers (
  teacher_id INT PRIMARY KEY,
  name VARCHAR(200) NOT NULL,
  email VARCHAR(200) NOT NULL UNIQUE,
  created_at TIMESTAMP NOT NULL
);
```

**確認クエリ**:

```sql
-- テーブルが作成されたか確認
SELECT * FROM teachers;

-- テーブル構造を確認（PostgreSQL）
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'teachers';
```

### 1-2) デフォルト値を持つテーブルを作成

`notifications` テーブルを作成してください。以下のカラムを持ちます：

- `notification_id`: INT、主キー
- `student_id`: INT、NOT NULL
- `message`: TEXT、NOT NULL
- `read`: BOOLEAN、デフォルト値は `false`
- `created_at`: TIMESTAMP、NOT NULL、デフォルト値は現在時刻

**解答例**:

```sql
CREATE TABLE notifications (
  notification_id INT PRIMARY KEY,
  student_id INT NOT NULL,
  message TEXT NOT NULL,
  read BOOLEAN DEFAULT false,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

**確認クエリ**:

```sql
SELECT * FROM notifications;
```

---

## 演習 2: CREATE TABLE - 外部キー制約

### 2-1) 外部キーを持つテーブルを作成

`homework_submissions` テーブルを作成してください。以下のカラムを持ちます：

- `submission_id`: INT、主キー
- `lesson_id`: INT、NOT NULL、外部キー（`lessons.lesson_id` を参照）
- `title`: VARCHAR(200)、NOT NULL
- `content`: TEXT
- `submitted_at`: TIMESTAMP、NOT NULL

**解答例**:

```sql
CREATE TABLE homework_submissions (
  submission_id INT PRIMARY KEY,
  lesson_id INT NOT NULL,
  title VARCHAR(200) NOT NULL,
  content TEXT,
  submitted_at TIMESTAMP NOT NULL,
  FOREIGN KEY (lesson_id) REFERENCES lessons(lesson_id)
);
```

**確認クエリ**:

```sql
SELECT * FROM homework_submissions;
```

### 2-2) 複数の外部キーを持つテーブルを作成

`attendance` テーブルを作成してください。以下のカラムを持ちます：

- `attendance_id`: INT、主キー
- `lesson_id`: INT、NOT NULL、外部キー（`lessons.lesson_id` を参照）
- `student_id`: INT、NOT NULL、外部キー（`students.student_id` を参照）
- `attended`: BOOLEAN、デフォルト値は `true`
- `attended_at`: TIMESTAMP、NOT NULL

**解答例**:

```sql
CREATE TABLE attendance (
  attendance_id INT PRIMARY KEY,
  lesson_id INT NOT NULL,
  student_id INT NOT NULL,
  attended BOOLEAN DEFAULT true,
  attended_at TIMESTAMP NOT NULL,
  FOREIGN KEY (lesson_id) REFERENCES lessons(lesson_id),
  FOREIGN KEY (student_id) REFERENCES students(student_id)
);
```

**確認クエリ**:

```sql
SELECT * FROM attendance;
```

---

## CREATE TABLE AS SELECT - 既存テーブルからテーブルを作成

CREATE TABLE AS SELECT 文は、既存のテーブルからデータを取得して新しいテーブルを作成するための SQL 文です。バックアップテーブルの作成や、データのコピーに便利です。

### CREATE TABLE AS SELECT 文の基本構文

```sql
-- 既存テーブルのデータをコピーして新しいテーブルを作成
CREATE TABLE 新しいテーブル名 AS
SELECT * FROM 既存のテーブル名;

-- 条件を指定してデータをコピー
CREATE TABLE 新しいテーブル名 AS
SELECT * FROM 既存のテーブル名
WHERE 条件;
```

**注意**: `CREATE TABLE AS SELECT` で作成されたテーブルは、元のテーブルの制約（主キー、外部キー、UNIQUE 制約など）は引き継がれません。必要に応じて、後から制約を追加する必要があります。

---

## 演習 3: CREATE TABLE AS SELECT - バックアップテーブルの作成

### 3-1) テーブルの完全なコピーを作成

`students` テーブルのバックアップテーブル `students_backup` を作成してください。

**解答例**:

```sql
-- students テーブルのバックアップを作成
CREATE TABLE students_backup AS
SELECT * FROM students;
```

**確認クエリ**:

```sql
-- バックアップテーブルの件数を確認
SELECT COUNT(*) FROM students_backup;

-- 元のテーブルと件数が一致することを確認
SELECT
  (SELECT COUNT(*) FROM students) AS original_count,
  (SELECT COUNT(*) FROM students_backup) AS backup_count;
```

### 3-2) 条件付きでテーブルを作成

`enrollments` テーブルから、`status` が `active` の受講登録のみを含む `active_enrollments` テーブルを作成してください。

**解答例**:

```sql
-- active な受講登録のみを含むテーブルを作成
CREATE TABLE active_enrollments AS
SELECT * FROM enrollments
WHERE status = 'active';
```

**確認クエリ**:

```sql
-- 作成されたテーブルの件数を確認
SELECT COUNT(*) FROM active_enrollments;

-- 元のテーブルの active な件数と一致することを確認
SELECT
  (SELECT COUNT(*) FROM enrollments WHERE status = 'active') AS original_active_count,
  (SELECT COUNT(*) FROM active_enrollments) AS new_table_count;
```

## ALTER TABLE - テーブル構造の変更

ALTER TABLE 文は、既存のテーブルの構造を変更するための SQL 文です。

### ALTER TABLE の主な操作

- **ADD COLUMN**: カラムを追加
- **DROP COLUMN**: カラムを削除
- **ALTER COLUMN**: カラムの型や制約を変更
- **ADD CONSTRAINT**: 制約を追加
- **DROP CONSTRAINT**: 制約を削除
- **RENAME TO**: テーブル名を変更
- **RENAME COLUMN**: カラム名を変更

---

## 演習 4: ALTER TABLE - カラムの追加

### 4-1) カラムを追加

`teachers` テーブルに、以下のカラムを追加してください：

- `phone`: VARCHAR(20)

**解答例**:

```sql
ALTER TABLE teachers
ADD COLUMN phone VARCHAR(20);
```

**確認クエリ**:

```sql
SELECT * FROM teachers;
```

### 4-2) デフォルト値を持つカラムを追加

`notifications` テーブルに、以下のカラムを追加してください：

- `notification_type`: VARCHAR(50)、デフォルト値は `'info'`

**解答例**:

```sql
ALTER TABLE notifications
ADD COLUMN notification_type VARCHAR(50) DEFAULT 'info';
```

**確認クエリ**:

```sql
SELECT * FROM notifications;
```

---

## 演習 5: ALTER TABLE - カラムの削除

### 5-1) カラムを削除

`teachers` テーブルから `phone` カラムを削除してください。

**削除前の確認**:

```sql
SELECT * FROM teachers;
```

**解答例**:

```sql
ALTER TABLE teachers
DROP COLUMN phone;
```

**削除後の確認**:

```sql
SELECT * FROM teachers;
-- phone カラムがなくなっていることを確認
```

---

## 演習 6: ALTER TABLE - カラムの変更

### 6-1) カラムの型を変更

`notifications` テーブルの `notification_type` カラムの型を `VARCHAR(100)` に変更してください。

**解答例**:

```sql
ALTER TABLE notifications
ALTER COLUMN notification_type TYPE VARCHAR(100);
```

**確認クエリ**:

```sql
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'notifications' AND column_name = 'notification_type';
```

### 6-2) カラムに NOT NULL 制約を追加

`notifications` テーブルの `notification_type` カラムに NOT NULL 制約を追加してください。

**解答例**:

```sql
ALTER TABLE notifications
ALTER COLUMN notification_type SET NOT NULL;
```

**確認クエリ**:

```sql
SELECT column_name, is_nullable
FROM information_schema.columns
WHERE table_name = 'notifications' AND column_name = 'notification_type';
-- is_nullable が 'NO' になっていることを確認
```

---

## 演習 7: ALTER TABLE - 制約の追加・削除

### 7-1) 外部キー制約を追加

`notifications` テーブルの `student_id` カラムに、`students.student_id` を参照する外部キー制約を追加してください。

**解答例**:

```sql
ALTER TABLE notifications
ADD CONSTRAINT fk_notifications_student
FOREIGN KEY (student_id) REFERENCES students(student_id);
```

**確認クエリ**:

```sql
-- 外部キー制約が追加されたか確認
SELECT
  tc.constraint_name,
  tc.table_name,
  kcu.column_name,
  ccu.table_name AS foreign_table_name,
  ccu.column_name AS foreign_column_name
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu
  ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage AS ccu
  ON ccu.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY'
  AND tc.table_name = 'notifications';
```

### 7-2) 制約を削除

`notifications` テーブルから、先ほど追加した外部キー制約を削除してください。

**解答例**:

```sql
ALTER TABLE notifications
DROP CONSTRAINT fk_notifications_student;
```

**確認クエリ**:

```sql
-- 外部キー制約が削除されたか確認（上記のクエリで結果が0件になることを確認）
```

---

## 演習 8: ALTER TABLE - テーブル名・カラム名の変更

### 8-1) カラム名を変更

`notifications` テーブルの `read` カラムを `is_read` に変更してください。

**解答例**:

```sql
ALTER TABLE notifications
RENAME COLUMN read TO is_read;
```

**確認クエリ**:

```sql
SELECT * FROM notifications;
-- カラム名が is_read になっていることを確認
```

### 8-2) テーブル名を変更

`notifications` テーブルを `student_notifications` に変更してください。

**解答例**:

```sql
ALTER TABLE notifications
RENAME TO student_notifications;
```

**確認クエリ**:

```sql
SELECT * FROM student_notifications;
-- テーブル名が変更されたことを確認
```

---

## DROP TABLE - テーブルの削除

DROP TABLE 文は、テーブルを削除するための SQL 文です。

### DROP TABLE 文の基本構文

```sql
-- テーブルを削除（エラーが発生する場合は無視）
DROP TABLE テーブル名;

-- テーブルが存在する場合のみ削除（エラーを回避）
DROP TABLE IF EXISTS テーブル名;
```

**重要**: DROP TABLE を実行すると、テーブルとその中のすべてのデータが削除されます。実行前に必ず確認してください。

---

## 演習 9: DROP TABLE - テーブルの削除

### 9-1) テーブルを削除

`student_notifications` テーブルを削除してください。

**削除前の確認**:

```sql
SELECT * FROM student_notifications;
```

**解答例**:

```sql
DROP TABLE student_notifications;
```

**削除後の確認**:

```sql
SELECT * FROM student_notifications;
-- エラーが発生することを確認（テーブルが存在しない）
```

---

## 演習 10: 実践的なシナリオ

### 10-1) テーブルの再作成

以下の手順で、`teachers` テーブルを再作成してください：

1. 既存の `teachers` テーブルを削除
2. 新しい `teachers` テーブルを作成（以下のカラムを持つ）
   - `teacher_id`: INT、主キー
   - `name`: VARCHAR(200)、NOT NULL
   - `email`: VARCHAR(200)、NOT NULL、UNIQUE
   - `specialty`: VARCHAR(100)
   - `created_at`: TIMESTAMP、NOT NULL、デフォルト値は現在時刻

**解答例**:

```sql
-- 1. 既存のテーブルを削除
DROP TABLE IF EXISTS teachers;

-- 2. 新しいテーブルを作成
CREATE TABLE teachers (
  teacher_id INT PRIMARY KEY,
  name VARCHAR(200) NOT NULL,
  email VARCHAR(200) NOT NULL UNIQUE,
  specialty VARCHAR(100),
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

**確認クエリ**:

```sql
SELECT * FROM teachers;
```

---

## まとめ

- **CREATE TABLE**: 新しいテーブルを作成する
- **ALTER TABLE**: 既存のテーブル構造を変更する
- **DROP TABLE**: テーブルを削除する

DDL 文は、データベースの構造を定義・変更するための基本的な手段です。実務では、これらの文を組み合わせて、データベースの設計を構築・変更します。安全に操作するため、常に実行前に確認する習慣を身につけましょう。
