# DDL、DML、DCLの違い

SQLは大きく分けて、**DDL（Data Definition Language）**、**DML（Data Manipulation Language）**、**DCL（Data Control Language）**の3つに分類されます。

---

## DDL（Data Definition Language）データ定義言語

DDLは、データベースの**構造**を定義・変更するための言語です。

### DDLの主なコマンド

- **CREATE**: テーブル、インデックス、ビューなどのオブジェクトを作成
- **ALTER**: 既存のテーブル構造を変更（カラム追加、削除など）
- **DROP**: テーブル、インデックス、ビューなどを削除
- **TRUNCATE**: テーブルの全データを削除（構造は残す）

---

## DML（Data Manipulation Language）データ操作言語

DMLは、データベース内の**データ**を操作するための言語です。

### DMLの主なコマンド

- **SELECT**: データを取得・検索
- **INSERT**: 新しいデータを追加
- **UPDATE**: 既存のデータを更新
- **DELETE**: データを削除

---

## DCL（Data Control Language）データ制御言語

DCLは、データベースへの**アクセス権限**を制御するための言語です。

### DCLの主なコマンド

- **GRANT**: ユーザーやロールに権限を付与
- **REVOKE**: ユーザーやロールから権限を剥奪

---

## DDL、DML、DCLの比較表

| 項目 | DDL | DML | DCL |
|------|-----|-----|-----|
| **目的** | データベース構造の定義・変更 | データの操作 | アクセス権限の制御 |
| **主なコマンド** | CREATE, ALTER, DROP, TRUNCATE | SELECT, INSERT, UPDATE, DELETE | GRANT, REVOKE |
| **トランザクション** | 自動コミット（ロールバック不可） | トランザクション内で実行可能 | 自動コミット |
| **実行頻度** | 低い（スキーマ変更時） | 高い（通常の操作） | 低い（権限設定時） |
| **影響範囲** | データベース構造全体 | データのみ | アクセス権限 |

---

## まとめ

- **DDL**: データベースの「設計図」を作成・変更する（CREATE, ALTER, DROP）
- **DML**: データベースの「中身」を操作する（SELECT, INSERT, UPDATE, DELETE）
- **DCL**: データベースへの「アクセス権限」を制御する（GRANT, REVOKE）
