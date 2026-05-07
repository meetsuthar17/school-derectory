from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


# ---------------- DEPARTMENT ----------------

class Department(Base):

    __tablename__ = "departments"

    did = Column(Integer, primary_key=True, index=True)

    dname = Column(String(100), nullable=False)

    teachers = relationship("Teacher", back_populates="department")

    students = relationship("Student", back_populates="department")

    subjects = relationship("Subject", back_populates="department")

    def department_dict(self):

        return {
            "did": self.did,
            "dname": self.dname
        }


# ---------------- TEACHER ----------------

class Teacher(Base):

    __tablename__ = "teachers"

    tid = Column(Integer, primary_key=True, index=True)

    tname = Column(String(100), nullable=False)

    did = Column(Integer, ForeignKey("departments.did"))

    department = relationship("Department", back_populates="teachers")

    students = relationship("Student", back_populates="teacher")

    subjects = relationship("Subject", back_populates="teacher")

    def teacher_dict(self):

        return {
            "tid": self.tid,
            "tname": self.tname,
            "department_id": self.did
        }


# ---------------- STUDENT ----------------

class Student(Base):

    __tablename__ = "students"

    sid = Column(Integer, primary_key=True, index=True)

    sname = Column(String(100), nullable=False)

    rollno = Column(Integer, nullable=False)

    did = Column(Integer, ForeignKey("departments.did"))

    tid = Column(Integer, ForeignKey("teachers.tid"))

    department = relationship("Department", back_populates="students")

    teacher = relationship("Teacher", back_populates="students")

    def student_dict(self):

        return {
            "sid": self.sid,
            "sname": self.sname,
            "rollno": self.rollno,
            "department_id": self.did,
            "teacher_id": self.tid
        }


# ---------------- SUBJECT ----------------

class Subject(Base):

    __tablename__ = "subjects"

    code = Column(Integer, primary_key=True, index=True)

    sub1 = Column(String(100))

    sub2 = Column(String(100))

    sub3 = Column(String(100))

    did = Column(Integer, ForeignKey("departments.did"))

    tid = Column(Integer, ForeignKey("teachers.tid"))

    department = relationship("Department", back_populates="subjects")

    teacher = relationship("Teacher", back_populates="subjects")

    def subject_dict(self):

        return {
            "code":self.code,
            "sub1": self.sub1,
            "sub2": self.sub2,
            "sub3": self.sub3,
            "department_id": self.did,
            "teacher_id": self.tid
        }