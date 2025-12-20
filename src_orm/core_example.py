"""
SQLAlchemy Core を使ったサンプルプログラム

SQLAlchemy Core は、SQL に近い低レベルの API を提供します。
テーブル定義やクエリを Python のコードで記述できますが、
SQL の知識が必要です。

このサンプルでは、以下の操作を学べます：
- テーブルの定義（メタデータ）
- SELECT クエリの実行
- INSERT, UPDATE, DELETE の実行
- JOIN を使った複雑なクエリ
"""

from sqlalchemy import (
    create_engine, MetaData, Table, Column, Integer, String, 
    Text, DateTime, Numeric, ForeignKey, select, insert, update, delete
)
from sqlalchemy.sql import func
from datetime import datetime
import os
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()

# データベース接続URL（環境変数から取得、なければデフォルト値）
DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgresql://user:password@localhost:5432/dbname'
)

# エンジンを作成（データベースへの接続を管理）
engine = create_engine(DATABASE_URL, echo=True)  # echo=True で実行されるSQLを表示

# メタデータオブジェクトを作成（テーブル定義を管理）
metadata = MetaData()

# テーブル定義（SQLAlchemy Core では Table クラスのインスタンスで定義）
# Table はクラス、students はそのインスタンス（オブジェクト）です
students = Table(
    'students', metadata,
    Column('student_id', Integer, primary_key=True),
    Column('name', String(200), nullable=False),
    Column('email', String(200), nullable=False, unique=True),
    Column('enrollment_date', DateTime, nullable=False)
)

courses = Table(
    'courses', metadata,
    Column('course_id', Integer, primary_key=True),
    Column('title', String(200), nullable=False),
    Column('description', Text),
    Column('monthly_price', Numeric(10, 2), nullable=False),
    Column('created_at', DateTime, nullable=False)
)

enrollments = Table(
    'enrollments', metadata,
    Column('enrollment_id', Integer, primary_key=True),
    Column('student_id', Integer, ForeignKey('students.student_id'), nullable=False),
    Column('course_id', Integer, ForeignKey('courses.course_id'), nullable=False),
    Column('enrolled_at', DateTime, nullable=False),
    Column('status', String(20), nullable=False)
)

lessons = Table(
    'lessons', metadata,
    Column('lesson_id', Integer, primary_key=True),
    Column('enrollment_id', Integer, ForeignKey('enrollments.enrollment_id'), nullable=False),
    Column('scheduled_at', DateTime, nullable=False),
    Column('duration_minutes', Integer, nullable=False),
    Column('status', String(20), nullable=False),
    Column('notes', Text)
)

video_submissions = Table(
    'video_submissions', metadata,
    Column('submission_id', Integer, primary_key=True),
    Column('lesson_id', Integer, ForeignKey('lessons.lesson_id'), nullable=False),
    Column('title', String(200), nullable=False),
    Column('video_url', String(500)),
    Column('submitted_at', DateTime, nullable=False),
    Column('status', String(20), nullable=False)
)

reviews = Table(
    'reviews', metadata,
    Column('review_id', Integer, primary_key=True),
    Column('submission_id', Integer, ForeignKey('video_submissions.submission_id'), nullable=False),
    Column('rating', Integer),
    Column('feedback', Text),
    Column('reviewed_at', DateTime, nullable=False)
)


def example_1_select_all_students():
    """例1: すべての生徒を取得"""
    print("\n=== 例1: すべての生徒を取得 ===")
    
    # SELECT * FROM students に相当
    query = select(students)
    
    with engine.connect() as conn:
        result = conn.execute(query)
        for row in result:
            print(f"ID: {row.student_id}, 名前: {row.name}, メール: {row.email}")


def example_2_select_with_condition():
    """例2: 条件付きで生徒を取得"""
    print("\n=== 例2: 2024年1月に登録した生徒を取得 ===")
    
    # SELECT * FROM students WHERE enrollment_date >= '2024-01-01'
    query = select(students).where(
        students.c.enrollment_date >= datetime(2024, 1, 1)
    )
    
    with engine.connect() as conn:
        result = conn.execute(query)
        for row in result:
            print(f"ID: {row.student_id}, 名前: {row.name}, 登録日: {row.enrollment_date}")


def example_3_select_specific_columns():
    """例3: 特定のカラムのみ取得"""
    print("\n=== 例3: コースのタイトルと価格のみ取得 ===")
    
    # SELECT title, monthly_price FROM courses
    query = select(courses.c.title, courses.c.monthly_price)
    
    with engine.connect() as conn:
        result = conn.execute(query)
        for row in result:
            print(f"コース: {row.title}, 月額: {row.monthly_price}円")


def example_4_join_query():
    """例4: JOIN を使ったクエリ"""
    print("\n=== 例4: 生徒と受講登録を JOIN ===")
    
    # SELECT s.name, e.status FROM students s
    # JOIN enrollments e ON s.student_id = e.student_id
    query = select(
        students.c.name,
        enrollments.c.status
    ).select_from(
        students.join(enrollments, students.c.student_id == enrollments.c.student_id)
    )
    
    with engine.connect() as conn:
        result = conn.execute(query)
        for row in result:
            print(f"生徒名: {row.name}, ステータス: {row.status}")


def example_5_aggregate_query():
    """例5: 集計関数を使ったクエリ"""
    print("\n=== 例5: コースごとの平均価格を計算 ===")
    
    # SELECT AVG(monthly_price) FROM courses
    query = select(func.avg(courses.c.monthly_price))
    
    with engine.connect() as conn:
        result = conn.execute(query)
        avg_price = result.scalar()  # 単一の値を取得
        print(f"平均月額料金: {avg_price}円")


def example_6_group_by():
    """例6: GROUP BY を使った集計"""
    print("\n=== 例6: ステータスごとの受講登録数を集計 ===")
    
    # SELECT status, COUNT(*) FROM enrollments GROUP BY status
    query = select(
        enrollments.c.status,
        func.count().label('count')
    ).group_by(enrollments.c.status)
    
    with engine.connect() as conn:
        result = conn.execute(query)
        for row in result:
            print(f"ステータス: {row.status}, 件数: {row.count}")


def example_7_insert():
    """例7: INSERT でデータを追加"""
    print("\n=== 例7: 新しい生徒を追加 ===")
    
    # INSERT INTO students VALUES (...)
    new_student = insert(students).values(
        student_id=107,
        name='佐藤 花子',
        email='hanako.sato@example.com',
        enrollment_date=datetime.now()
    )
    
    with engine.connect() as conn:
        # 実際に実行する場合はコメントアウトを外してください
        # conn.execute(new_student)
        # conn.commit()
        print("新しい生徒の追加クエリを生成しました（実行はコメントアウト中）")


def example_8_update():
    """例8: UPDATE でデータを更新"""
    print("\n=== 例8: 生徒のメールアドレスを更新 ===")
    
    # UPDATE students SET email = 'new@example.com' WHERE student_id = 101
    update_query = update(students).where(
        students.c.student_id == 101
    ).values(email='new.email@example.com')
    
    with engine.connect() as conn:
        # 実際に実行する場合はコメントアウトを外してください
        # conn.execute(update_query)
        # conn.commit()
        print("更新クエリを生成しました（実行はコメントアウト中）")


def example_9_delete():
    """例9: DELETE でデータを削除"""
    print("\n=== 例9: 特定の生徒を削除 ===")
    
    # DELETE FROM students WHERE student_id = 107
    delete_query = delete(students).where(students.c.student_id == 107)
    
    with engine.connect() as conn:
        # 実際に実行する場合はコメントアウトを外してください
        # conn.execute(delete_query)
        # conn.commit()
        print("削除クエリを生成しました（実行はコメントアウト中）")


def example_10_complex_join():
    """例10: 複数のテーブルを JOIN"""
    print("\n=== 例10: 生徒、コース、受講登録を JOIN ===")
    
    # 生徒名、コース名、受講日を取得
    query = select(
        students.c.name.label('student_name'),
        courses.c.title.label('course_title'),
        enrollments.c.enrolled_at
    ).select_from(
        students.join(enrollments, students.c.student_id == enrollments.c.student_id)
        .join(courses, enrollments.c.course_id == courses.c.course_id)
    ).where(enrollments.c.status == 'active')
    
    with engine.connect() as conn:
        result = conn.execute(query)
        for row in result:
            print(f"生徒: {row.student_name}, コース: {row.course_title}, 登録日: {row.enrolled_at}")


if __name__ == '__main__':
    print("SQLAlchemy Core サンプルプログラム")
    print("=" * 50)
    
    # 各例を実行
    example_1_select_all_students()
    example_2_select_with_condition()
    example_3_select_specific_columns()
    example_4_join_query()
    example_5_aggregate_query()
    example_6_group_by()
    example_7_insert()
    example_8_update()
    example_9_delete()
    example_10_complex_join()
    
    print("\n" + "=" * 50)
    print("すべての例を実行しました！")

