from sqlalchemy import Column, Integer, String, Text, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Student(Base):
    """生徒テーブル"""
    __tablename__ = "students"

    student_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False, unique=True)
    enrollment_date = Column(DateTime, nullable=False)

    # リレーションシップ
    enrollments = relationship("Enrollment", back_populates="student")


class Course(Base):
    """コーステーブル"""
    __tablename__ = "courses"

    course_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    monthly_price = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime, nullable=False)

    # リレーションシップ
    enrollments = relationship("Enrollment", back_populates="course")


class Enrollment(Base):
    """受講登録テーブル"""
    __tablename__ = "enrollments"

    enrollment_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.student_id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.course_id"), nullable=False)
    enrolled_at = Column(DateTime, nullable=False)
    status = Column(String(20), nullable=False)  # 'active', 'completed', 'cancelled'

    # リレーションシップ
    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
    lessons = relationship("Lesson", back_populates="enrollment")


class Lesson(Base):
    """授業スケジュールテーブル"""
    __tablename__ = "lessons"

    lesson_id = Column(Integer, primary_key=True, index=True)
    enrollment_id = Column(Integer, ForeignKey("enrollments.enrollment_id"), nullable=False)
    scheduled_at = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False)  # 'scheduled', 'completed', 'cancelled'
    notes = Column(Text)

    # リレーションシップ
    enrollment = relationship("Enrollment", back_populates="lessons")
    video_submissions = relationship("VideoSubmission", back_populates="lesson")


class VideoSubmission(Base):
    """ビデオ提出テーブル"""
    __tablename__ = "video_submissions"

    submission_id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.lesson_id"), nullable=False)
    title = Column(String(200), nullable=False)
    video_url = Column(String(500))
    submitted_at = Column(DateTime, nullable=False)
    status = Column(String(20), nullable=False)  # 'submitted', 'reviewed', 'revised'

    # リレーションシップ
    lesson = relationship("Lesson", back_populates="video_submissions")
    reviews = relationship("Review", back_populates="submission")


class Review(Base):
    """レビューテーブル"""
    __tablename__ = "reviews"

    review_id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey("video_submissions.submission_id"), nullable=False)
    rating = Column(Integer)  # 1-5の評価
    feedback = Column(Text)
    reviewed_at = Column(DateTime, nullable=False)

    # リレーションシップ
    submission = relationship("VideoSubmission", back_populates="reviews")

