# DML（データ操作言語）実践トレーニング

このドキュメントでは、データベースのデータを操作するための **INSERT**、**UPDATE**、**DELETE** 文を学びます。実際に手を動かしながら、データの追加・更新・削除の方法を身につけましょう。

- スキーマ定義: `sql/01_ddl.sql`
- サンプルデータ投入: `sql/02_seed.sql`

**実行環境**: Supabase（PostgreSQL ベース）を想定しています。

---

## セットアップ手順

### 1) テーブルの準備

SQL Editor で `sql/01_ddl.sql` を実行してテーブルを作成し、`sql/02_seed.sql` を実行してサンプルデータを投入してください。

### 2) 実行前の確認

各演習を実行する前に、以下のクエリで現在のデータを確認できます：

```sql
-- テーブルごとの件数確認
SELECT 'students' AS tbl, COUNT(*) FROM students
UNION ALL SELECT 'courses', COUNT(*) FROM courses
UNION ALL SELECT 'enrollments', COUNT(*) FROM enrollments
UNION ALL SELECT 'lessons', COUNT(*) FROM lessons
UNION ALL SELECT 'video_submissions', COUNT(*) FROM video_submissions
UNION ALL SELECT 'reviews', COUNT(*) FROM reviews;
```

---

## INSERT 文 - データの追加

INSERT 文は、テーブルに新しいデータを追加するための SQL 文です。

### INSERT 文の基本構文

```sql
-- すべてのカラムに値を指定する場合
INSERT INTO テーブル名 VALUES (値1, 値2, 値3, ...);

-- 特定のカラムにのみ値を指定する場合（推奨）
INSERT INTO テーブル名 (カラム1, カラム2, ...) VALUES (値1, 値2, ...);

-- 複数行を一度に追加する場合
INSERT INTO テーブル名 (カラム1, カラム2, ...)
VALUES
  (値1, 値2, ...),
  (値3, 値4, ...),
  (値5, 値6, ...);

-- SELECT句の結果を挿入する場合（既存のテーブルからデータを取得して挿入）
INSERT INTO テーブル名 (カラム1, カラム2, ...)
SELECT カラム1, カラム2, ...
FROM 元のテーブル名
WHERE 条件;
```

---

## 演習 1: INSERT 文 - データの追加

### 1-1) 複数の受講登録を一度に追加

`enrollments` テーブルに、以下の 2 つの受講登録を一度に追加してください：

1. `enrollment_id`: 312, `student_id`: 107, `course_id`: 201, `enrolled_at`: 2024-03-01 10:15:00, `status`: 'active'
2. `enrollment_id`: 313, `student_id`: 107, `course_id`: 206, `enrolled_at`: 2024-03-01 10:20:00, `status`: 'active'

**解答例**:

```sql
INSERT INTO enrollments (enrollment_id, student_id, course_id, enrolled_at, status)
VALUES
  (312, 107, 201, '2024-03-01 10:15:00', 'active'),
  (313, 107, 206, '2024-03-01 10:20:00', 'active');
```

**確認クエリ**:

```sql
SELECT * FROM enrollments WHERE student_id = 107;
```

### 1-2) 複数の授業スケジュールを追加

`lessons` テーブルに、以下の 2 つの授業スケジュールを一度に追加してください：

1. `lesson_id`: 424, `enrollment_id`: 312, `scheduled_at`: 2024-03-05 10:00:00, `duration_minutes`: 60, `status`: 'scheduled', `notes`: '自己紹介と挨拶'
2. `lesson_id`: 425, `enrollment_id`: 313, `scheduled_at`: 2024-03-06 11:00:00, `duration_minutes`: 60, `status`: 'scheduled', `notes`: '発音の基礎'

**解答例**:

```sql
INSERT INTO lessons (lesson_id, enrollment_id, scheduled_at, duration_minutes, status, notes)
VALUES
  (424, 312, '2024-03-05 10:00:00', 60, 'scheduled', '自己紹介と挨拶'),
  (425, 313, '2024-03-06 11:00:00', 60, 'scheduled', '発音の基礎');
```

**確認クエリ**:

```sql
SELECT * FROM lessons WHERE enrollment_id IN (312, 313);
```

---

## 演習 2: INSERT 文 - SELECT 句を使ったデータの追加

INSERT 文に SELECT 句を組み合わせることで、既存のテーブルからデータを取得して別のテーブルに挿入できます。これは、データのコピーや集計結果の保存などに便利です。

### 2-1) 退会済みの生徒を別テーブルに移す

退会済みの生徒の情報を `old_students` テーブルに移します。まず、`students` テーブルに `status` カラムを追加し、`old_students` テーブルを作成します。

**準備**（テーブルの準備）:

```sql
-- students テーブルに status カラムを追加
ALTER TABLE students
ADD COLUMN status VARCHAR(20) DEFAULT 'active';

-- 退会済みの生徒を保存するテーブルを作成
CREATE TABLE old_students (
  student_id INT PRIMARY KEY,
  name VARCHAR(200) NOT NULL,
  email VARCHAR(200) NOT NULL,
  enrollment_date TIMESTAMP NOT NULL,
  left_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- テスト用に、一部の生徒を退会済みに設定
UPDATE students
SET status = 'left'
WHERE student_id IN (101, 103);
```

**解答例**（退会済みの生徒を old_students テーブルに移す）:

```sql
-- 退会済みの生徒を old_students テーブルに挿入
INSERT INTO old_students (student_id, name, email, enrollment_date, left_at)
SELECT
  student_id,
  name,
  email,
  enrollment_date,
  CURRENT_TIMESTAMP AS left_at
FROM students
WHERE status = 'left';
```

**確認クエリ**:

```sql
-- old_students テーブルに移されたデータを確認
SELECT * FROM old_students;

-- students テーブルの退会済み生徒を確認
SELECT * FROM students WHERE status = 'left';
```

### 2-2) 集計結果を別テーブルに保存

生徒ごとの受講コース数を集計し、その結果を新しいテーブルに保存します。

まず、集計結果を保存するためのテーブルを作成します：

```sql
-- 集計結果を保存するテーブルを作成
CREATE TABLE IF NOT EXISTS student_course_summary (
  student_id INT PRIMARY KEY,
  student_name VARCHAR(200),
  num_courses INT,
  total_monthly_price DECIMAL(10,2),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

次に、集計結果を挿入します：

**解答例**:

```sql
-- 生徒ごとの受講コース数と合計月額料金を集計して挿入
INSERT INTO student_course_summary (student_id, student_name, num_courses, total_monthly_price)
SELECT
  s.student_id,
  s.name AS student_name,
  COUNT(e.enrollment_id) AS num_courses,
  COALESCE(SUM(c.monthly_price), 0) AS total_monthly_price
FROM students s
LEFT JOIN enrollments e ON e.student_id = s.student_id AND e.status != 'cancelled'
LEFT JOIN courses c ON c.course_id = e.course_id
GROUP BY s.student_id, s.name;
```

**確認クエリ**:

```sql
SELECT * FROM student_course_summary
ORDER BY total_monthly_price DESC;
```

## UPDATE 文 - データの更新

UPDATE 文は、既存のデータを更新するための SQL 文です。

### UPDATE 文の基本構文

```sql
UPDATE テーブル名
SET カラム1 = 値1, カラム2 = 値2, ...
WHERE 条件;
```

**重要**: WHERE 句を忘れると、テーブル内のすべての行が更新されてしまいます。必ず WHERE 句を指定してください。

---

## 演習 3: UPDATE 文 - データの更新

### 3-1) 受講登録のステータスと日時を更新

`enrollments` テーブルで、`enrollment_id` が 312 の受講登録のステータスを `completed` に、`enrolled_at` を 2024-03-15 10:15:00 に更新してください。

**解答例**:

```sql
UPDATE enrollments
SET status = 'completed',
    enrolled_at = '2024-03-15 10:15:00'
WHERE enrollment_id = 312;
```

**確認クエリ**:

```sql
SELECT enrollment_id, student_id, course_id, enrolled_at, status
FROM enrollments
WHERE enrollment_id = 312;
```

### 3-2) 授業のステータスとメモを更新

`lessons` テーブルで、`lesson_id` が 424 の授業のステータスを `completed` に、`notes` を '自己紹介と挨拶（完了）' に更新してください。

**解答例**:

```sql
UPDATE lessons
SET status = 'completed', notes = '自己紹介と挨拶（完了）'
WHERE lesson_id = 424;
```

**確認クエリ**:

```sql
SELECT lesson_id, enrollment_id, scheduled_at, status, notes
FROM lessons
WHERE lesson_id = 424;
```

---

## DELETE 文 - データの削除

DELETE 文は、テーブルからデータを削除するための SQL 文です。

### DELETE 文の基本構文

```sql
DELETE FROM テーブル名
WHERE 条件;
```

**重要**: WHERE 句を忘れると、テーブル内のすべてのデータが削除されてしまいます。必ず WHERE 句を指定してください。

---

## 演習 4: DELETE 文 - データの削除

### 4-1) 特定のデータを削除

`reviews` テーブルで、`review_id` が 613 のレビューを削除してください。

**削除前の確認**:

```sql
SELECT * FROM reviews WHERE review_id = 613;
```

**解答例**:

```sql
DELETE FROM reviews
WHERE review_id = 613;
```

**削除後の確認**:

```sql
SELECT * FROM reviews WHERE review_id = 613;
-- 結果が0件になっていることを確認
```

### 4-2) 条件に一致するデータを一括削除

`enrollments` テーブルで、`status` が `cancelled` の受講登録をすべて削除してください。

**削除前の確認**:

```sql
SELECT * FROM enrollments WHERE status = 'cancelled';
```

**解答例**:

```sql
DELETE FROM enrollments
WHERE status = 'cancelled';
```

**削除後の確認**:

```sql
SELECT * FROM enrollments WHERE status = 'cancelled';
-- 結果が0件になっていることを確認
```

---

## 演習 5: 外部キー制約を考慮した削除

### 5-1) 関連データを考慮した削除順序

`enrollments` テーブルから `enrollment_id` が 312 の受講登録を削除する場合、関連する `lessons` テーブルのデータも削除する必要があります。

**削除前の確認**:

```sql
-- 関連する授業を確認
SELECT * FROM lessons WHERE enrollment_id = 312;
```

**解答例**:

```sql
-- まず関連する授業を削除
DELETE FROM lessons
WHERE enrollment_id = 312;

-- その後、受講登録を削除
DELETE FROM enrollments
WHERE enrollment_id = 312;
```

**削除後の確認**:

```sql
SELECT * FROM enrollments WHERE enrollment_id = 312;
SELECT * FROM lessons WHERE enrollment_id = 312;
-- 両方とも結果が0件になっていることを確認
```

---

## 演習 6: 実践的なシナリオ

### 6-1) 生徒の退会処理

生徒（`student_id` = 107）が退会する場合、以下の処理を行ってください：

1. 関連するすべての授業を削除
2. 関連するすべての受講登録を削除
3. 最後に生徒データを削除

**解答例**:

```sql
-- 1. 関連する授業を削除（enrollments を経由）
DELETE FROM lessons
WHERE enrollment_id IN (
  SELECT enrollment_id FROM enrollments WHERE student_id = 107
);

-- 2. 関連する受講登録を削除
DELETE FROM enrollments
WHERE student_id = 107;

-- 3. 生徒データを削除
DELETE FROM students
WHERE student_id = 107;
```

**確認クエリ**:

```sql
SELECT * FROM students WHERE student_id = 107;
SELECT * FROM enrollments WHERE student_id = 107;
SELECT * FROM lessons WHERE enrollment_id IN (
  SELECT enrollment_id FROM enrollments WHERE student_id = 107
);
-- すべて結果が0件になっていることを確認
```

---

## まとめ

- **INSERT**: 新しいデータを追加する
- **UPDATE**: 既存のデータを更新する（WHERE 句を忘れずに）
- **DELETE**: データを削除する（WHERE 句を忘れずに）

DML 文は、データベースのデータを操作する基本的な手段です。実務では、これらの文を組み合わせて、複雑なデータ操作を行います。安全に操作するため、常に WHERE 句を指定し、実行前に確認する習慣を身につけましょう。
