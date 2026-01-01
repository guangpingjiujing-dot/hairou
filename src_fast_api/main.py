from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Student, Course
from schemas import StudentCreate, StudentResponse, CourseCreate, CourseResponse

app = FastAPI(title="学習管理システムAPI", description="シンプルなFastAPI + SQLAlchemy実装")

# CORS設定（ブラウザからのアクセスを許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では特定のオリジンのみ許可することを推奨
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ========== Students エンドポイント ==========

@app.get("/students", response_model=List[StudentResponse])
def get_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """全生徒を取得"""
    students = db.query(Student).offset(skip).limit(limit).all()
    return students


@app.get("/students/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    """特定の生徒を取得"""
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@app.post("/students", response_model=StudentResponse)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    """新しい生徒を作成"""
    # 既に存在するかチェック
    existing_student = db.query(Student).filter(Student.student_id == student.student_id).first()
    if existing_student:
        raise HTTPException(status_code=400, detail="Student ID already exists")
    
    db_student = Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


# ========== Courses エンドポイント ==========

@app.get("/courses", response_model=List[CourseResponse])
def get_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """全コースを取得"""
    courses = db.query(Course).offset(skip).limit(limit).all()
    return courses


@app.get("/courses/{course_id}", response_model=CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):
    """特定のコースを取得"""
    course = db.query(Course).filter(Course.course_id == course_id).first()
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@app.post("/courses", response_model=CourseResponse)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    """新しいコースを作成"""
    # 既に存在するかチェック
    existing_course = db.query(Course).filter(Course.course_id == course.course_id).first()
    if existing_course:
        raise HTTPException(status_code=400, detail="Course ID already exists")
    
    db_course = Course(**course.model_dump())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


# ========== ヘルスチェック ==========

@app.get("/")
def root():
    """ルートエンドポイント"""
    return {"message": "学習管理システムAPIへようこそ！"}


@app.get("/health")
def health_check():
    """ヘルスチェック"""
    return {"status": "ok"}

