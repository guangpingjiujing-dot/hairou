"""
SQLAlchemy ORM を使ったサンプルプログラム

SQLAlchemy ORM (Object-Relational Mapping) は、
データベースのテーブルを Python のクラスとして扱えます。
SQL を直接書かずに、Python のオブジェクト操作でデータベースを操作できます。

このサンプルでは、以下の操作を学べます：
- モデルクラスの定義
- セッションの使い方
- クエリの実行
- リレーションシップの定義と使い方
- データの追加、更新、削除
"""

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Numeric, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
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

# エンジンを作成
engine = create_engine(DATABASE_URL, echo=True)  # echo=True で実行されるSQLを表示

# セッションクラスを作成
SessionLocal = sessionmaker(bind=engine)

# ベースクラスを作成（すべてのモデルクラスはこれを継承）
Base = declarative_base()


# ==================== モデルクラスの定義 ====================
# 
# 【Core との違い】
# - Core: Table クラスからインスタンスを作成（students = Table(...)）
# - ORM: クラスを定義（class Student(Base):）
# 
# ORM では、テーブルを Python のクラスとして定義します。
# このクラスから、実際のデータ（インスタンス）を作成できます。
# 例: student = Student(name='田中', ...)  # Student クラスのインスタンス

class Student(Base):
    """生徒モデル"""
    __tablename__ = 'students'
    
    student_id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False, unique=True)
    enrollment_date = Column(DateTime, nullable=False)
    
    # リレーションシップ: 1人の生徒は複数の受講登録を持つ
    enrollments = relationship('Enrollment', back_populates='student')
    
    def __repr__(self):
        return f"<Student(id={self.student_id}, name='{self.name}')>"
    
    def has_active_enrollment(self):
        """
        シンプルなメソッド例: アクティブな受講登録があるかチェック
        
        【ORMのメリット】
        テーブルをクラスとして定義することで、データに関連するロジックを
        クラス内にメソッドとして定義できます。
        これにより、コードの再利用性と可読性が向上します。
        """
        return any(enrollment.status == 'active' for enrollment in self.enrollments)


class Course(Base):
    """コースモデル"""
    __tablename__ = 'courses'
    
    course_id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    monthly_price = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime, nullable=False)
    
    # リレーションシップ: 1つのコースは複数の受講登録を持つ
    enrollments = relationship('Enrollment', back_populates='course')
    
    def __repr__(self):
        return f"<Course(id={self.course_id}, title='{self.title}')>"


class Enrollment(Base):
    """受講登録モデル"""
    __tablename__ = 'enrollments'
    
    enrollment_id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.student_id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.course_id'), nullable=False)
    enrolled_at = Column(DateTime, nullable=False)
    status = Column(String(20), nullable=False)
    
    # リレーションシップ: 多対1の関係
    student = relationship('Student', back_populates='enrollments')
    course = relationship('Course', back_populates='enrollments')
    
    # リレーションシップ: 1つの受講登録は複数のレッスンを持つ
    lessons = relationship('Lesson', back_populates='enrollment')
    
    def __repr__(self):
        return f"<Enrollment(id={self.enrollment_id}, student_id={self.student_id}, course_id={self.course_id})>"
    
    def get_completed_lessons_count(self):
        """
        実用的なメソッド例: 完了したレッスン数を取得
        
        【ORMのメリット】
        複雑なロジック（リレーションシップを辿って集計するなど）を
        メソッドとして定義することで、ビジネスロジックをモデルに集約できます。
        呼び出し側は単純に enrollment.get_completed_lessons_count() と
        呼ぶだけで済み、実装の詳細を気にする必要がありません。
        """
        return sum(1 for lesson in self.lessons if lesson.status == 'completed')


class Lesson(Base):
    """レッスンモデル"""
    __tablename__ = 'lessons'
    
    lesson_id = Column(Integer, primary_key=True)
    enrollment_id = Column(Integer, ForeignKey('enrollments.enrollment_id'), nullable=False)
    scheduled_at = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False)
    notes = Column(Text)
    
    # リレーションシップ
    enrollment = relationship('Enrollment', back_populates='lessons')
    video_submissions = relationship('VideoSubmission', back_populates='lesson')
    
    def __repr__(self):
        return f"<Lesson(id={self.lesson_id}, enrollment_id={self.enrollment_id})>"


class VideoSubmission(Base):
    """ビデオ提出モデル"""
    __tablename__ = 'video_submissions'
    
    submission_id = Column(Integer, primary_key=True)
    lesson_id = Column(Integer, ForeignKey('lessons.lesson_id'), nullable=False)
    title = Column(String(200), nullable=False)
    video_url = Column(String(500))
    submitted_at = Column(DateTime, nullable=False)
    status = Column(String(20), nullable=False)
    
    # リレーションシップ
    lesson = relationship('Lesson', back_populates='video_submissions')
    reviews = relationship('Review', back_populates='submission')
    
    def __repr__(self):
        return f"<VideoSubmission(id={self.submission_id}, lesson_id={self.lesson_id})>"


class Review(Base):
    """レビューモデル"""
    __tablename__ = 'reviews'
    
    review_id = Column(Integer, primary_key=True)
    submission_id = Column(Integer, ForeignKey('video_submissions.submission_id'), nullable=False)
    rating = Column(Integer)
    feedback = Column(Text)
    reviewed_at = Column(DateTime, nullable=False)
    
    # リレーションシップ
    submission = relationship('VideoSubmission', back_populates='reviews')
    
    def __repr__(self):
        return f"<Review(id={self.review_id}, submission_id={self.submission_id}, rating={self.rating})>"


# ==================== サンプル関数 ====================

def example_1_get_all_students():
    """例1: すべての生徒を取得"""
    print("\n=== 例1: すべての生徒を取得 ===")
    
    session = SessionLocal()
    try:
        # SELECT * FROM students に相当
        students = session.query(Student).all()
        
        for student in students:
            print(f"ID: {student.student_id}, 名前: {student.name}, メール: {student.email}")
    finally:
        session.close()


def example_2_get_student_by_id():
    """例2: IDで生徒を取得"""
    print("\n=== 例2: ID=101の生徒を取得 ===")
    
    session = SessionLocal()
    try:
        # SELECT * FROM students WHERE student_id = 101
        student = session.query(Student).filter(Student.student_id == 101).first()
        
        if student:
            print(f"ID: {student.student_id}, 名前: {student.name}, メール: {student.email}")
        else:
            print("生徒が見つかりませんでした")
    finally:
        session.close()


def example_3_filter_students():
    """例3: 条件で生徒をフィルタリング"""
    print("\n=== 例3: 2024年1月に登録した生徒を取得 ===")
    
    session = SessionLocal()
    try:
        # SELECT * FROM students WHERE enrollment_date >= '2024-01-01'
        students = session.query(Student).filter(
            Student.enrollment_date >= datetime(2024, 1, 1)
        ).all()
        
        for student in students:
            print(f"ID: {student.student_id}, 名前: {student.name}, 登録日: {student.enrollment_date}")
    finally:
        session.close()


def example_4_use_relationship():
    """例4: リレーションシップを使う"""
    print("\n=== 例4: 生徒の受講登録を取得 ===")
    
    session = SessionLocal()
    
    try:
        student = session.query(Student).filter(Student.student_id == 101).first()
        
        if student:
            print(f"生徒: {student.name}")
            print("受講登録:")
            for enrollment in student.enrollments:
                course = enrollment.course  # リレーションシップでコースを取得
                print(f"  - {course.title} (ステータス: {enrollment.status})")
    finally:
        session.close()


def example_5_join_query():
    """例5: JOIN を使ったクエリ"""
    print("\n=== 例5: 生徒とコースを JOIN ===")
    
    session = SessionLocal()
    try:
        # SELECT s.name, c.title FROM students s
        # JOIN enrollments e ON s.student_id = e.student_id
        # JOIN courses c ON e.course_id = c.course_id
        results = session.query(Student.name, Course.title).join(
            Enrollment, Student.student_id == Enrollment.student_id
        ).join(
            Course, Enrollment.course_id == Course.course_id
        ).filter(Enrollment.status == 'active').all()
        
        for name, title in results:
            print(f"生徒: {name}, コース: {title}")
    finally:
        session.close()


def example_6_aggregate():
    """例6: 集計関数を使う"""
    print("\n=== 例6: コースの平均価格を計算 ===")
    
    session = SessionLocal()
    try:
        from sqlalchemy import func
        
        # SELECT AVG(monthly_price) FROM courses
        avg_price = session.query(func.avg(Course.monthly_price)).scalar()
        print(f"平均月額料金: {avg_price}円")
    finally:
        session.close()


def example_7_group_by():
    """例7: GROUP BY を使った集計"""
    print("\n=== 例7: ステータスごとの受講登録数を集計 ===")
    
    session = SessionLocal()
    try:
        from sqlalchemy import func
        
        # SELECT status, COUNT(*) FROM enrollments GROUP BY status
        results = session.query(
            Enrollment.status,
            func.count(Enrollment.enrollment_id).label('count')
        ).group_by(Enrollment.status).all()
        
        for status, count in results:
            print(f"ステータス: {status}, 件数: {count}")
    finally:
        session.close()


def example_8_create_new_student():
    """例8: 新しい生徒を作成"""
    print("\n=== 例8: 新しい生徒を作成 ===")
    
    session = SessionLocal()
    try:
        new_student = Student(
            student_id=107,
            name='佐藤 花子',
            email='hanako.sato@example.com',
            enrollment_date=datetime.now()
        )
        
        session.add(new_student)
        # 実際に保存する場合はコメントアウトを外してください
        # session.commit()
        print("新しい生徒を作成しました（保存はコメントアウト中）")
    except Exception as e:
        session.rollback()
        print(f"エラー: {e}")
    finally:
        session.close()


def example_9_update_student():
    """例9: 生徒情報を更新"""
    print("\n=== 例9: 生徒のメールアドレスを更新 ===")
    
    session = SessionLocal()
    try:
        student = session.query(Student).filter(Student.student_id == 101).first()
        
        if student:
            student.email = 'new.email@example.com'  # type: ignore[assignment]
            # 実際に保存する場合はコメントアウトを外してください
            # session.commit()
            print(f"生徒 {student.name} のメールアドレスを更新しました（保存はコメントアウト中）")
    except Exception as e:
        session.rollback()
        print(f"エラー: {e}")
    finally:
        session.close()


def example_10_delete_student():
    """例10: 生徒を削除"""
    print("\n=== 例10: 生徒を削除 ===")
    
    session = SessionLocal()
    try:
        student = session.query(Student).filter(Student.student_id == 107).first()
        
        if student:
            session.delete(student)
            # 実際に削除する場合はコメントアウトを外してください
            # session.commit()
            print(f"生徒 {student.name} を削除しました（実行はコメントアウト中）")
    except Exception as e:
        session.rollback()
        print(f"エラー: {e}")
    finally:
        session.close()


def example_11_eager_loading():
    """例11: リレーションシップを先読み（Eager Loading）"""
    print("\n=== 例11: 生徒と受講登録を一度に取得 ===")
    
    session = SessionLocal()
    try:
        from sqlalchemy.orm import joinedload
        
        # リレーションシップも一緒に取得（N+1問題を回避）
        students = session.query(Student).options(
            joinedload(Student.enrollments)
        ).all()
        
        for student in students[:3]:  # 最初の3人だけ表示
            print(f"生徒: {student.name}")
            print(f"  受講登録数: {len(student.enrollments)}")
    finally:
        session.close()


def example_12_complex_query():
    """例12: 複雑なクエリ"""
    print("\n=== 例12: 高評価のレビューを持つビデオ提出を取得 ===")
    
    session = SessionLocal()
    try:
        # 評価が4以上のレビューを持つビデオ提出を取得
        submissions = session.query(VideoSubmission).join(
            Review, VideoSubmission.submission_id == Review.submission_id
        ).filter(Review.rating >= 4).distinct().all()
        
        for submission in submissions:
            print(f"ビデオ: {submission.title}, レッスンID: {submission.lesson_id}")
            for review in submission.reviews:
                if review.rating >= 4:
                    print(f"  評価: {review.rating}, フィードバック: {review.feedback[:50]}...")
    finally:
        session.close()


def example_13_class_method_simple():
    """例13: クラスメソッドの使用例（シンプル）"""
    print("\n=== 例13: クラスメソッドの使用例（シンプル）===")
    print("【ORMのメリット】テーブルをクラスとして定義することで、")
    print("データに関連するロジックをメソッドとして定義できます。")
    print()
    
    session = SessionLocal()
    try:
        student = session.query(Student).filter(Student.student_id == 101).first()
        
        if student:
            print(f"生徒: {student.name}")
            # メソッドを呼び出すだけで、アクティブな受講登録があるかチェックできる
            if student.has_active_enrollment():
                print("  → アクティブな受講登録があります")
            else:
                print("  → アクティブな受講登録がありません")
    finally:
        session.close()


def example_14_class_method_practical():
    """例14: クラスメソッドの使用例（実用的）"""
    print("\n=== 例14: クラスメソッドの使用例（実用的）===")
    print("【ORMのメリット】複雑なロジックをメソッドとして定義することで、")
    print("ビジネスロジックをモデルに集約し、コードの再利用性が向上します。")
    print()
    
    session = SessionLocal()
    try:
        enrollments = session.query(Enrollment).limit(5).all()
        
        for enrollment in enrollments:
            student = enrollment.student
            course = enrollment.course
            # メソッドを呼び出すだけで、完了したレッスン数を取得できる
            completed_count = enrollment.get_completed_lessons_count()
            total_count = len(enrollment.lessons)
            
            print(f"生徒: {student.name}, コース: {course.title}")
            print(f"  完了レッスン数: {completed_count}/{total_count}")
    finally:
        session.close()


if __name__ == '__main__':
    print("SQLAlchemy ORM サンプルプログラム")
    print("=" * 50)
    
    # 各例を実行
    example_1_get_all_students()
    example_2_get_student_by_id()
    example_3_filter_students()
    example_4_use_relationship()
    example_5_join_query()
    example_6_aggregate()
    example_7_group_by()
    example_8_create_new_student()
    example_9_update_student()
    example_10_delete_student()
    example_11_eager_loading()
    example_12_complex_query()
    example_13_class_method_simple()
    example_14_class_method_practical()
    
    print("\n" + "=" * 50)
    print("すべての例を実行しました！")

