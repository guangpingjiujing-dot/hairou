from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from decimal import Decimal


# Student スキーマ
class StudentBase(BaseModel):
    name: str
    email: EmailStr
    enrollment_date: datetime


class StudentCreate(StudentBase):
    student_id: int


class StudentResponse(StudentBase):
    student_id: int

    class Config:
        from_attributes = True


# Course スキーマ
class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    monthly_price: Decimal
    created_at: datetime


class CourseCreate(CourseBase):
    course_id: int


class CourseResponse(CourseBase):
    course_id: int

    class Config:
        from_attributes = True

