from sqlalchemy import (
    create_engine, MetaData, Table, Column, Integer, String, 
    Text, DateTime, Numeric, ForeignKey, select, insert, update, delete
)
import os 
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()

DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgresql://user:password@localhost:5432/dbname'
)

# エンジンを作成（データベースへの接続を管理）
engine = create_engine(DATABASE_URL, echo=True)  # echo=True で実行されるSQLを表示

# メタデータオブジェクトを作成（テーブル定義を管理）
metadata = MetaData()

students = Table(
    'students', metadata,
    Column('student_id', Integer, primary_key=True),
    Column('name', String(200), nullable=False),
    Column('email', String(200), nullable=False, unique=True),
    Column('enrollment_date', DateTime, nullable=False)
)

conn = engine.connect()
result = conn.execute(select(students))

print(result)
print([row for row in result])