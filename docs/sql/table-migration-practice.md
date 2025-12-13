# テーブル構造変更の実践シナリオ

このドキュメントでは、既存のテーブル構造を変更する際の**安全で信頼性の高い移行方法**を学びます。

## この演習の目的と重要性

データベースのテーブル構造を変更する際、単に `ALTER TABLE` を実行するだけでは不十分な場合があります。特に、テーブル作成時しか設定できない設定（例：ストレージエンジン、パーティショニング設定、特定の制約など）を変更する場合や、テーブル名を変更したくない場合には、別のアプローチが必要です。

### なぜ安全な移行方法が重要なのか

1. **データの保護**: 移行中にデータが失われるリスクを最小限に抑える
2. **検証可能性**: 移行前後でデータの整合性を確認できる
3. **監査証跡**: 後から「このリリースが問題なかった」ことを証明できる

### この演習で学ぶこと

- バックアップテーブルの作成方法
- データの差分チェック方法（EXCEPT を使用）
- 安全なテーブル再作成とデータ移行の手順
- 各ステップでの検証方法

---

## シナリオ: students テーブルに NOT NULL 制約を追加する

### 前提条件

現在の `students` テーブルには `status` カラムが存在し、NULL 値を許可しています。これを NOT NULL 制約に変更したいとします。

**注意**: 実際には、NOT NULL 制約の追加は `ALTER TABLE ... ALTER COLUMN ... SET NOT NULL` で対応できます。しかし、この演習では「テーブル作成時しか設定できない設定を変更する必要がある場合」を想定しています。例えば、ストレージエンジンの変更、パーティショニング設定の変更、特定のデータベース固有のオプションなどが該当します。NOT NULL 制約の追加は、そのような設定変更の例として扱います。

既存のデータには NULL 値が含まれている可能性があるため、慎重に移行する必要があります。

### 移行前の準備

まず、現在のテーブル構造とデータを確認します：

```sql
-- 現在のテーブル構造を確認
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'students'
ORDER BY ordinal_position;

-- 現在のデータ件数を確認
SELECT COUNT(*) AS total_count,
       COUNT(status) AS status_not_null_count,
       COUNT(*) - COUNT(status) AS status_null_count
FROM students;
```

---

## ステップ 1: バックアップテーブルの作成

既存のテーブルを日付サフィックス付きでバックアップします。

**解答例**:

```sql
-- バックアップテーブルを作成（CREATE TABLE AS SELECT を使用）
-- 日付サフィックス: 20251213（例: 2024年3月15日）
CREATE TABLE students_backup_20251213 AS
SELECT * FROM students;
```

**確認クエリ**:

```sql
-- バックアップテーブルの件数を確認
SELECT COUNT(*) FROM students_backup_20251213;

-- 元のテーブルと件数が一致することを確認
SELECT
  (SELECT COUNT(*) FROM students) AS original_count,
  (SELECT COUNT(*) FROM students_backup_20251213) AS backup_count;
```

---

## ステップ 2: データの差分チェック（EXCEPT を使用）

バックアップテーブルと元のテーブルに差分がないことを確認します。

**EXCEPT とは**: 2 つのクエリの結果を比較し、最初のクエリにのみ存在する行を返します。両方向で EXCEPT を実行することで、完全な差分を確認できます。

**解答例**:

```sql
-- 元のテーブルにあってバックアップにないデータを確認
SELECT * FROM students
EXCEPT
SELECT * FROM students_backup_20251213;

-- バックアップにあって元のテーブルにないデータを確認
SELECT * FROM students_backup_20251213
EXCEPT
SELECT * FROM students;
```

**期待される結果**: 両方のクエリが 0 件を返すこと（差分がないことを意味します）

**差分がある場合の対処**: 差分が見つかった場合は、バックアップテーブルを削除して再作成するか、原因を調査してください。

---

## ステップ 3: 既存テーブルの削除

差分がなかったことを確認したら、既存のテーブルを削除します。

**重要**: このステップを実行する前に、必ずステップ 2 で差分がないことを確認してください。

**解答例**:

```sql
-- 既存のテーブルを削除
DROP TABLE students;
```

**確認クエリ**:

```sql
-- テーブルが削除されたことを確認
SELECT *
FROM information_schema.tables
WHERE table_schema = 'public' AND table_name = 'students';
-- 結果が0件になることを確認
```

---

## ステップ 4: 新しい設定でテーブルを再作成

新しい設定（NOT NULL 制約を含む）でテーブルを再作成します。

**解答例**:

```sql
-- 新しい設定でテーブルを再作成
CREATE TABLE students (
  student_id INT PRIMARY KEY,
  name VARCHAR(200) NOT NULL,
  email VARCHAR(200) NOT NULL UNIQUE,
  enrollment_date TIMESTAMP NOT NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'active'  -- NOT NULL 制約を追加
);
```

**確認クエリ**:

```sql
-- 新しいテーブル構造を確認
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'students'
ORDER BY ordinal_position;
-- status カラムの is_nullable が 'NO' になっていることを確認
```

---

## ステップ 5: バックアップテーブルからデータを挿入

バックアップテーブルから新しいテーブルにデータを移行します。

**注意**: バックアップテーブルに NULL 値が含まれている場合、NOT NULL 制約によりエラーが発生します。その場合は、NULL 値を適切なデフォルト値に変換する必要があります。

**解答例**:

```sql
-- バックアップテーブルからデータを挿入
-- status が NULL の場合は 'active' に変換
INSERT INTO students (student_id, name, email, enrollment_date, status)
SELECT
  student_id,
  name,
  email,
  enrollment_date,
  COALESCE(status, 'active') AS status  -- NULL の場合は 'active' に変換
FROM students_backup_20251213;
```

**確認クエリ**:

```sql
-- データが正しく挿入されたことを確認
SELECT COUNT(*) FROM students;
SELECT COUNT(*) FROM students_backup_20251213;
-- 両方の件数が一致することを確認
```

---

## ステップ 6: 再度差分チェック

バックアップテーブルと再作成したテーブルのデータに差分がないことを確認します。

**解答例**:

```sql
-- 再作成したテーブルにあってバックアップにないデータを確認
SELECT * FROM students
EXCEPT
SELECT * FROM students_backup_20251213;

-- バックアップにあって再作成したテーブルにないデータを確認
SELECT * FROM students_backup_20251213
EXCEPT
SELECT * FROM students;
```

**期待される結果**: 両方のクエリが 0 件を返すこと（ただし、status が NULL から 'active' に変換された場合は、その行は差分として表示されます。これは意図的な変更なので問題ありません）

---

## ステップ 7: バックアップテーブルの削除

すべての検証が完了し、問題がないことを確認したら、バックアップテーブルを削除します。

**解答例**:

```sql
-- バックアップテーブルを削除
DROP TABLE students_backup_20251213;
```

**確認クエリ**:

```sql
-- バックアップテーブルが削除されたことを確認
SELECT *
FROM information_schema.tables
WHERE table_schema = 'public' AND table_name = 'students_backup_20251213';
-- 結果が0件になることを確認
```

---

## 最終確認

移行が正常に完了したことを確認します。

**確認クエリ**:

```sql
-- テーブル構造の確認
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'students'
ORDER BY ordinal_position;

-- データの確認
SELECT COUNT(*) AS total_count,
       COUNT(status) AS status_not_null_count,
       COUNT(*) - COUNT(status) AS status_null_count
FROM students;
-- status_null_count が 0 であることを確認

-- サンプルデータの確認
SELECT * FROM students LIMIT 5;
```

---

## まとめ

この演習では、以下の安全な移行手順を学びました：

1. **バックアップの作成**: `CREATE TABLE AS SELECT` でバックアップテーブルを作成
2. **差分チェック**: `EXCEPT` を使用してデータの整合性を確認
3. **段階的な移行**: 各ステップで検証を行いながら進める
4. **検証の徹底**: 移行前後でデータの整合性を確認
5. **クリーンアップ**: 問題がないことを確認してからバックアップを削除

### 実務での応用

この方法は、以下のような場面で役立ちます：

- ストレージエンジンの変更（例: MyISAM → InnoDB）
- パーティショニングの追加・変更
- テーブル作成時のみ設定可能なオプションの変更
- 大規模な構造変更が必要な場合

### ベストプラクティス

- **バックアップの保持期間**: 本番環境では、バックアップテーブルを一定期間（例: 1 週間）保持することを推奨します
- **ログの記録**: 各ステップの実行時刻と結果を記録しておくと、後から問題を追跡しやすくなります
- **段階的な適用**: 本番環境に適用する前に、開発環境やステージング環境で十分にテストしてください

---
