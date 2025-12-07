# SQL 実践トレーニングドキュメント（1on1 学習カリキュラム管理システム）

このドキュメントは、実際に手を動かしながら SQL を学ぶためのハンズオン教材です。用意したサンプルデータを使い、基礎から実務で役立つ集計・結合・ウィンドウ関数まで段階的に練習できます。

- スキーマ定義: `sql/01_ddl.sql`
- サンプルデータ投入: `sql/02_seed.sql`

**実行環境**: Supabase（PostgreSQL ベース）を想定しています。

---

## セットアップ手順（Supabase）

### 1) Supabase プロジェクトの準備

1. [Supabase](https://supabase.com/)にログインし、プロジェクトを作成
2. プロジェクトの「SQL Editor」を開く

### 2) テーブル作成（DDL 実行）

SQL Editor で `sql/01_ddl.sql` の内容をコピー＆ペーストして実行します。

```sql
-- sql/01_ddl.sql の内容をそのまま実行
```

### 3) サンプルデータの投入

SQL Editor で `sql/02_seed.sql` の内容をコピー＆ペーストして実行します。

```sql
-- sql/02_seed.sql の内容をそのまま実行
```

### 4) テーブル一覧/件数確認（任意）

SQL Editor で以下のクエリを実行して、データが正しく投入されたか確認します。

```sql
SELECT 'students' AS tbl, COUNT(*) FROM students
UNION ALL SELECT 'courses', COUNT(*) FROM courses
UNION ALL SELECT 'enrollments', COUNT(*) FROM enrollments
UNION ALL SELECT 'lessons', COUNT(*) FROM lessons
UNION ALL SELECT 'video_submissions', COUNT(*) FROM video_submissions
UNION ALL SELECT 'reviews', COUNT(*) FROM reviews;
```

---

## スキーマ概要

- `students(student_id, name, email, enrollment_date)` - 生徒テーブル
- `courses(course_id, title, description, monthly_price, created_at)` - コーステーブル（月額料金含む）
- `enrollments(enrollment_id, student_id, course_id, enrolled_at, status)` - 受講登録（生徒がコースに登録）
- `lessons(lesson_id, enrollment_id, scheduled_at, duration_minutes, status, notes)` - 授業スケジュール（1 つの受講登録に対して複数回のレッスン）
- `video_submissions(submission_id, lesson_id, title, video_url, submitted_at, status)` - ビデオ提出
- `reviews(review_id, submission_id, rating, feedback, reviewed_at)` - レビュー（教師によるビデオ提出へのレビュー）

**注意**: 教師は 1 人のため、教師テーブルはありません。コースは月額コースです。`video_submissions`は`lesson_id`のみを持ち、`lesson_id`から`enrollments`と`students`を取得できます。

主な関係:

- `enrollments.student_id -> students.student_id`
- `enrollments.course_id -> courses.course_id`
- `lessons.enrollment_id -> enrollments.enrollment_id`（1 つの受講登録に対して複数回のレッスン）
- `video_submissions.lesson_id -> lessons.lesson_id`（lesson_id から enrollment_id と student_id を取得可能）
- `reviews.submission_id -> video_submissions(submission_id)`

---

## 演習 1: SELECT 基本

- 1-1) `students` から全列を 5 件表示
- 1-2) `name` と `email` のみ、`enrollment_date` 昇順で 5 件

解答例:

```sql
-- 1-1
SELECT *
FROM students
LIMIT 5;

-- 1-2
SELECT name, email
FROM students
ORDER BY enrollment_date ASC
LIMIT 5;
```

---

## 演習 2: WHERE での抽出

- 2-1) 月額料金が 16,000 円以上 20,000 円未満のコース一覧（`course_id, title, monthly_price`）
- 2-2) ステータスが `active` の受講登録（`enrollment_id, student_id, course_id`）

解答例:

```sql
-- 2-1
SELECT course_id, title, monthly_price
FROM courses
WHERE monthly_price >= 16000 AND monthly_price < 20000
ORDER BY monthly_price;

-- 2-2
SELECT enrollment_id, student_id, course_id
FROM enrollments
WHERE status = 'active';
```

---

## 演習 3: ORDER BY / LIMIT

- 3-1) 最新に追加されたコーストップ 3（`created_at` 降順）
- 3-2) 月額料金が高い順トップ 3 のコース名と月額料金

解答例:

```sql
-- 3-1
SELECT course_id, title, created_at
FROM courses
ORDER BY created_at DESC
LIMIT 3;

-- 3-2
SELECT title, monthly_price
FROM courses
ORDER BY monthly_price DESC
LIMIT 3;
```

---

## 演習 4: 集計（GROUP BY / HAVING）

- 4-1) 受講登録ごとの授業数
- 4-2) コースごとの受講者数（受講者数が 2 人以上のみ）

解答例:

```sql
-- 4-1
SELECT e.enrollment_id, COUNT(l.lesson_id) AS num_lessons
FROM enrollments e
LEFT JOIN lessons l ON l.enrollment_id = e.enrollment_id
GROUP BY e.enrollment_id
ORDER BY num_lessons DESC;

-- 4-2
SELECT c.title AS course_title,
       COUNT(DISTINCT e.student_id) AS num_students
FROM enrollments e
JOIN courses c ON c.course_id = e.course_id
WHERE e.status = 'active'
GROUP BY c.course_id, c.title
HAVING COUNT(DISTINCT e.student_id) >= 2
ORDER BY num_students DESC;
```

---

## 演習 5: JOIN で明細を見やすく

- 5-1) 授業一覧（`lesson_id, scheduled_at, status, student_name, course_title`）
- 5-2) ビデオ提出一覧（`submission_id, student_name, course_title, title, submitted_at`）

解答例:

```sql
-- 5-1
SELECT l.lesson_id, l.scheduled_at, l.status,
       s.name AS student_name, c.title AS course_title
FROM lessons l
JOIN enrollments e ON e.enrollment_id = l.enrollment_id
JOIN students s ON s.student_id = e.student_id
JOIN courses c ON c.course_id = e.course_id
ORDER BY l.scheduled_at;

-- 5-2
SELECT vs.submission_id, s.name AS student_name,
       c.title AS course_title, vs.title, vs.submitted_at
FROM video_submissions vs
JOIN lessons l ON l.lesson_id = vs.lesson_id
JOIN enrollments e ON e.enrollment_id = l.enrollment_id
JOIN students s ON s.student_id = e.student_id
JOIN courses c ON c.course_id = e.course_id
ORDER BY vs.submitted_at;
```

---

## 演習 6: SUM 関数 - 月額料金の合計算出（重要）

- 6-1) 生徒ごとの受講コース合計月額料金（`student_id, student_name, total_monthly_price`）を計算
- 6-2) コースごとの総月額売上（`course_id, course_title, total_revenue`）

解答例:

```sql
-- 6-1: SUM関数を使って生徒ごとの合計月額料金を計算
SELECT e.student_id,
       s.name AS student_name,
       SUM(c.monthly_price) AS total_monthly_price
FROM enrollments e
JOIN students s ON s.student_id = e.student_id
JOIN courses c ON c.course_id = e.course_id
WHERE e.status != 'cancelled'
GROUP BY e.student_id, s.name
ORDER BY total_monthly_price DESC;

-- 6-2: SUM関数を使ってコースごとの総月額売上を計算
SELECT e.course_id,
       c.title AS course_title,
       SUM(c.monthly_price) AS total_revenue
FROM enrollments e
JOIN courses c ON c.course_id = e.course_id
WHERE e.status != 'cancelled'
GROUP BY e.course_id, c.title
ORDER BY total_revenue DESC;
```

---

## 演習 7: SUM 関数 - コースごとの売上分析

- 7-1) コースごとの授業数と、そのコースの合計月額料金
- 7-2) 月別の総月額売上（SUM 関数を使用）

解答例:

```sql
-- 7-1: コースごとの授業数と合計月額料金
SELECT c.course_id,
       c.title AS course_title,
       COUNT(DISTINCT l.lesson_id) AS num_lessons,
       SUM(c.monthly_price) AS total_course_revenue
FROM courses c
LEFT JOIN enrollments e ON e.course_id = c.course_id
LEFT JOIN lessons l ON l.enrollment_id = e.enrollment_id
WHERE e.status != 'cancelled' OR e.status IS NULL
GROUP BY c.course_id, c.title
ORDER BY total_course_revenue DESC;

-- 7-2: 月別の総月額売上（SUM関数を使用）
-- Supabase（PostgreSQL）では DATE_TRUNC 関数が使用可能です
SELECT DATE_TRUNC('month', e.enrolled_at) AS month,
       SUM(c.monthly_price) AS monthly_revenue
FROM enrollments e
JOIN courses c ON c.course_id = e.course_id
WHERE e.status != 'cancelled'
GROUP BY DATE_TRUNC('month', e.enrolled_at)
ORDER BY month;
```

---

## 演習 8: SUM 関数 - レビュー評価の集計

- 8-1) 全体のレビュー平均評価とレビュー数（SUM 関数でレビュー数を数える方法も含む）
- 8-2) 生徒ごとの提出ビデオ数と、そのビデオに対するレビュー平均評価

解答例:

```sql
-- 8-1: 全体のレビュー平均評価とレビュー数
SELECT COUNT(r.review_id) AS num_reviews,
       AVG(r.rating) AS avg_rating,
       SUM(r.rating) AS total_rating_sum  -- SUM関数の例
FROM reviews r;

-- 8-2: 生徒ごとの提出ビデオ数とレビュー平均評価
SELECT s.student_id,
       s.name AS student_name,
       COUNT(vs.submission_id) AS num_submissions,
       AVG(r.rating) AS avg_review_rating,
       SUM(r.rating) AS total_rating_sum  -- SUM関数の例
FROM students s
LEFT JOIN enrollments e ON e.student_id = s.student_id
LEFT JOIN lessons l ON l.enrollment_id = e.enrollment_id
LEFT JOIN video_submissions vs ON vs.lesson_id = l.lesson_id
LEFT JOIN reviews r ON r.submission_id = vs.submission_id
GROUP BY s.student_id, s.name
ORDER BY num_submissions DESC;
```

---

## 演習 9: SUM 関数 - ウィンドウ関数との組み合わせ

- 9-1) 生徒ごとの受講日時順に、累積受講料金を計算（SUM OVER を使用）
- 9-2) コースごとの受講者数と、そのコースの累積売上

解答例:

```sql
-- 9-1: 累積受講月額料金（SUM OVER を使用）
SELECT e.enrollment_id,
       e.student_id,
       s.name AS student_name,
       c.title AS course_title,
       c.monthly_price AS course_monthly_price,
       e.enrolled_at,
       SUM(c.monthly_price) OVER (
         PARTITION BY e.student_id
         ORDER BY e.enrolled_at, e.enrollment_id
         ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS cumulative_total_monthly_price
FROM enrollments e
JOIN students s ON s.student_id = e.student_id
JOIN courses c ON c.course_id = e.course_id
WHERE e.status != 'cancelled'
ORDER BY e.student_id, e.enrolled_at;

-- 9-2: コースごとの受講者数と累積売上
SELECT c.course_id,
       c.title AS course_title,
       COUNT(DISTINCT e.student_id) AS num_students,
       SUM(c.monthly_price) AS total_revenue,
       SUM(SUM(c.monthly_price)) OVER (
         ORDER BY c.course_id
         ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS cumulative_revenue
FROM courses c
LEFT JOIN enrollments e ON e.course_id = c.course_id AND e.status != 'cancelled'
GROUP BY c.course_id, c.title
ORDER BY c.course_id;
```

---

## 演習 10: CASE / 条件分岐

- 10-1) 受講登録ステータスを日本語ラベルに変換して表示
- 10-2) コース料金が 70,000 円以上なら「高額」、それ以外は「通常」ラベル

解答例:

```sql
-- 10-1
SELECT enrollment_id, status,
       CASE status
         WHEN 'active' THEN '受講中'
         WHEN 'completed' THEN '完了'
         WHEN 'cancelled' THEN 'キャンセル'
         ELSE 'その他'
       END AS status_jp
FROM enrollments
ORDER BY enrollment_id;

-- 10-2
SELECT course_id,
       title,
       monthly_price,
       CASE WHEN monthly_price >= 18000 THEN '高額' ELSE '通常' END AS price_label
FROM courses
ORDER BY monthly_price DESC;
```

---

## 演習 11: 未受講コースの抽出

- 11-1) 一度も受講されていないコース一覧

解答例:

```sql
SELECT c.course_id, c.title
FROM courses c
LEFT JOIN enrollments e ON e.course_id = c.course_id
WHERE e.course_id IS NULL
ORDER BY c.course_id;
```

---

## 演習 12: SUM 関数 - 複雑な集計

- 12-1) コースごとの総月額売上と、そのコースの授業の合計時間（分）
- 12-2) 月別の総月額売上と、その月の受講者数

解答例:

```sql
-- 12-1: コースごとの総月額売上と授業時間の合計
SELECT c.course_id,
       c.title AS course_title,
       SUM(c.monthly_price) AS total_revenue,
       SUM(l.duration_minutes) AS total_lesson_minutes
FROM courses c
LEFT JOIN enrollments e ON e.course_id = c.course_id
LEFT JOIN lessons l ON l.enrollment_id = e.enrollment_id
WHERE e.status != 'cancelled' OR e.status IS NULL
GROUP BY c.course_id, c.title
ORDER BY total_revenue DESC;

-- 12-2: 月別の総月額売上と受講者数
-- Supabase（PostgreSQL）では DATE_TRUNC 関数が使用可能です
SELECT DATE_TRUNC('month', e.enrolled_at) AS month,
       SUM(c.monthly_price) AS monthly_revenue,
       COUNT(DISTINCT e.student_id) AS num_students
FROM enrollments e
JOIN courses c ON c.course_id = e.course_id
WHERE e.status != 'cancelled'
GROUP BY DATE_TRUNC('month', e.enrolled_at)
ORDER BY month;
```

---

## 演習 13: SUM 関数 - サブクエリとの組み合わせ

- 13-1) 各生徒の受講コース数と、その合計料金を表示
- 13-2) レビュー評価の合計が最も高い教師を特定

解答例:

```sql
-- 13-1: 生徒ごとの受講コース数と合計月額料金
SELECT s.student_id,
       s.name AS student_name,
       COUNT(e.enrollment_id) AS num_courses,
       COALESCE(SUM(c.monthly_price), 0) AS total_monthly_price
FROM students s
LEFT JOIN enrollments e ON e.student_id = s.student_id AND e.status != 'cancelled'
LEFT JOIN courses c ON c.course_id = e.course_id
GROUP BY s.student_id, s.name
ORDER BY total_monthly_price DESC;

-- 13-2: レビュー評価の合計と平均
SELECT COUNT(r.review_id) AS num_reviews,
       SUM(r.rating) AS total_rating_sum,
       AVG(r.rating) AS avg_rating
FROM reviews r;
```

---

## 追加アイデア（発展）

- 月別・コース別の売上ヒートマップ
- 生徒の初回受講からの経過日数を用いたコホート分析
- レビュー評価の平均と標準偏差の比較
- 未レビューのビデオ提出の推移
- SUM 関数を使った複数条件での集計（例：アクティブな受講のみ、完了した受講のみなど）

---

## 参考: 実行順序のヒント

1. Supabase の SQL Editor で `sql/01_ddl.sql` を実行してテーブル作成
2. Supabase の SQL Editor で `sql/02_seed.sql` を実行してデータ投入
3. 本ドキュメントの演習を上から順に実行

**Supabase での注意点**:

- PostgreSQL ベースのため、PostgreSQL の構文・関数が使用可能です
- `DATE_TRUNC('month', ...)` などの日付関数が使用できます
- SQL Editor でクエリを実行すると、結果がテーブル形式で表示されます

---

## SUM 関数の学習ポイント

この教材では、SUM 関数を以下の場面で使用します：

1. **基本的な集計**: グループごとの合計を計算（演習 6, 7, 8, 12）
2. **ウィンドウ関数との組み合わせ**: 累積合計を計算（演習 9）
3. **複数テーブルの結合**: JOIN した結果の合計を計算（演習 7, 12）
4. **条件付き集計**: CASE 文と組み合わせた条件付き合計
5. **サブクエリとの組み合わせ**: 複雑な集計処理（演習 13）

SUM 関数は、数値データの合計を計算する最も基本的な集計関数の一つです。GROUP BY 句と組み合わせることで、グループごとの合計を計算できます。
