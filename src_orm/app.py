from sqlalchemy import (
    create_engine, MetaData, Table, Column, Integer, String, 
    Text, DateTime, Numeric, ForeignKey, select, insert, update, delete
)
import os 
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()

DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgresql://user:password@localhost:5432/dbname'
)

# エンジンを作成（データベースへの接続を管理）
engine = create_engine(DATABASE_URL, echo=True)  # echo=True で実行されるSQLを表示

# セッションクラスを作成
SessionLocal = sessionmaker(bind=engine)

# ベースクラスを作成（すべてのモデルクラスはこれを継承）
Base = declarative_base()


class Student(Base):
    """生徒モデル"""
    __tablename__ = 'students'
    
    student_id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False, unique=True)
    enrollment_date = Column(DateTime, nullable=False)
    
    # リレーションシップ: 1人の生徒は複数の受講登録を持つ
    # enrollments = relationship('Enrollment', back_populates='student')
    
    # def __repr__(self):
    #     return f"<Student(id={self.student_id}, name='{self.name}')>"

session = SessionLocal()
student = session.query(Student).filter(Student.student_id == 101).first()

if student:
    print(student)
    print(student.name)

# メタデータオブジェクトを作成（テーブル定義を管理）
# metadata = MetaData()

# students = Table(
#     'students', metadata,
#     Column('student_id', Integer, primary_key=True),
#     Column('name', String(200), nullable=False),
#     Column('email', String(200), nullable=False, unique=True),
#     Column('enrollment_date', DateTime, nullable=False)
# )

# conn = engine.connect()
# result = conn.execute(select(students))

# print(result)
# print([row for row in result])