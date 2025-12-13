-- SQL Practice Schema (DDL) for 1on1 Learning Curriculum Management System
-- For Supabase (PostgreSQL)

-- Clean up existing objects (ignore errors if your RDBMS doesn't support IF EXISTS)
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS video_submissions;
DROP TABLE IF EXISTS lessons;
DROP TABLE IF EXISTS enrollments;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS students;

-- Students: 生徒テーブル
CREATE TABLE students (
  student_id INT PRIMARY KEY,
  name VARCHAR(200) NOT NULL,
  email VARCHAR(200) NOT NULL UNIQUE,
  enrollment_date TIMESTAMP NOT NULL
);

-- Courses: コーステーブル（月額料金含む）
CREATE TABLE courses (
  course_id INT PRIMARY KEY,
  title VARCHAR(200) NOT NULL,
  description TEXT,
  monthly_price DECIMAL(10,2) NOT NULL, -- 月額料金
  created_at TIMESTAMP NOT NULL
);

-- Enrollments: 受講登録（生徒とコースの関係）
CREATE TABLE enrollments (
  enrollment_id INT PRIMARY KEY,
  student_id INT NOT NULL,
  course_id INT NOT NULL,
  enrolled_at TIMESTAMP NOT NULL,
  status VARCHAR(20) NOT NULL, -- 'active', 'completed', 'cancelled'
  FOREIGN KEY (student_id) REFERENCES students(student_id),
  FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

-- Lessons: 授業スケジュール（1つの受講登録に対して複数回のレッスン）
CREATE TABLE lessons (
  lesson_id INT PRIMARY KEY,
  enrollment_id INT NOT NULL,
  scheduled_at TIMESTAMP NOT NULL,
  duration_minutes INT NOT NULL,
  status VARCHAR(20) NOT NULL, -- 'scheduled', 'completed', 'cancelled'
  notes TEXT,
  FOREIGN KEY (enrollment_id) REFERENCES enrollments(enrollment_id)
);

-- Video Submissions: ビデオ提出
CREATE TABLE video_submissions (
  submission_id INT PRIMARY KEY,
  lesson_id INT NOT NULL,
  title VARCHAR(200) NOT NULL,
  video_url VARCHAR(500),
  submitted_at TIMESTAMP NOT NULL,
  status VARCHAR(20) NOT NULL, -- 'submitted', 'reviewed', 'revised'
  FOREIGN KEY (lesson_id) REFERENCES lessons(lesson_id)
);

-- Reviews: レビュー（教師によるビデオ提出へのレビュー）
CREATE TABLE reviews (
  review_id INT PRIMARY KEY,
  submission_id INT NOT NULL,
  rating INT, -- 1-5の評価
  feedback TEXT,
  reviewed_at TIMESTAMP NOT NULL,
  FOREIGN KEY (submission_id) REFERENCES video_submissions(submission_id)
);


