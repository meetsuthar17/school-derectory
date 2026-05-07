from fastapi import FastAPI, Depends, HTTPException, Form
from sqlalchemy.orm import Session

import models

from database import engine, SessionLocal


# ---------------- CREATE TABLES ----------------

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="School Directory")


# ---------------- DATABASE DEPENDENCY ----------------

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# ---------------- STARTUP DATA ----------------

@app.on_event("startup")
def startup_data():

    db = SessionLocal()

    try:

        # ---------------- DEPARTMENTS ----------------

        if db.query(models.Department).count() == 0:

            departments = [

                # models.Department(
                #     did=101,
                #     dname="IT"
                # ),

                # models.Department(
                #     did=102,
                #     dname="CS"
                # ),

                # models.Department(
                #     did=103,
                #     dname="Data Science"
                # )
            ]

            db.add_all(departments)

        # ---------------- TEACHERS ----------------

        if db.query(models.Teacher).count() == 0:

            teachers = [

                # models.Teacher(
                #     tid=1,
                #     tname="Avinash",
                #     did=101
                # ),

                # models.Teacher(
                #     tid=2,
                #     tname="Ram",
                #     did=102
                # ),

                # models.Teacher(
                #     tid=3,
                #     tname="Karan",
                #     did=103
                # )
            ]

            db.add_all(teachers)

        # ---------------- SUBJECTS ----------------

        if db.query(models.Subject).count() == 0:

            subjects = [

                # models.Subject(
                #     sub1="Python",
                #     sub2="Java",
                #     sub3="C++",
                #     tid=1,
                #     did=101
                # ),

                # models.Subject(
                #     sub1="DBMS",
                #     sub2="Networking",
                #     sub3="Microprocessor",
                #     tid=2,
                #     did=102
                # )
            ]

            db.add_all(subjects)

        db.commit()

    except Exception as e:

        db.rollback()

        print("Startup Error:", e)

    finally:
        db.close()


# ---------------- HOME ----------------

@app.get("/",tags=["Root Directory"])
def home():

    return {
        "message": "School Directory"
    }


# ---------------- GET DEPARTMENTS ----------------

@app.get("/departments", tags=["Departments"])
def get_departments(
    db: Session = Depends(get_db)
):

    try:

        departments = db.query(models.Department).all()

        return departments

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ---------------- GET TEACHERS ----------------

@app.get("/teachers", tags=["Teachers"])
def get_teachers(
    db: Session = Depends(get_db)
):

    try:

        teachers = db.query(models.Teacher).all()

        return teachers

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ---------------- GET SUBJECTS ----------------

@app.get("/subjects", tags=["Subjects"])
def get_subjects(
    db: Session = Depends(get_db)
):

    try:

        subjects = db.query(models.Subject).all()

        return subjects

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ---------------- ADD STUDENT ----------------

@app.post("/students", tags=["Students"])
def add_student(

    sid: int = Form(...),

    sname: str = Form(...),

    rollno: int = Form(...),

    did: int = Form(...),

    db: Session = Depends(get_db)

):

    try:

        # CHECK DEPARTMENT

        department = db.query(models.Department).filter(
            models.Department.did == did
        ).first()

        if not department:

            raise HTTPException(
                status_code=404,
                detail="Department not found"
            )

        # CHECK TEACHER

        teacher = db.query(models.Teacher).filter(
            models.Teacher.did == did
        ).first()

        if not teacher:

            raise HTTPException(
                status_code=404,
                detail="Teacher not found"
            )

        # CHECK EXISTING STUDENT

        existing_student = db.query(models.Student).filter(
            models.Student.sid == sid
        ).first()

        if existing_student:

            raise HTTPException(
                status_code=400,
                detail="Student ID already exists"
            )

        # CREATE STUDENT

        new_student = models.Student(

            sid=sid,

            sname=sname,

            rollno=rollno,

            tid=teacher.tid,

            did=department.did
        )

        db.add(new_student)

        db.commit()

        db.refresh(new_student)

        return {
            "message": "Student added successfully",
            "student": new_student.student_dict()
        }

    except HTTPException:

        raise

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ---------------- GET STUDENTS ----------------

@app.get("/students", tags=["Students"])
def get_students(
    db: Session = Depends(get_db)
):

    try:

        students = db.query(models.Student).all()

        return students

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# ---------------- UPDATE STUDENT ----------------

@app.put("/students/{sid}", tags=["Students"])
def update_student(

    sid: int,

    sname: str = Form(...),

    rollno: int = Form(...),

    did: int = Form(...),

    db: Session = Depends(get_db)

):

    try:

        # ---------------- FIND STUDENT ----------------

        student = db.query(models.Student).filter(
            models.Student.sid == sid
        ).first()

        if not student:

            raise HTTPException(
                status_code=404,
                detail="Student not found"
            )

        # ---------------- CHECK DEPARTMENT ----------------

        department = db.query(models.Department).filter(
            models.Department.did == did
        ).first()

        if not department:

            raise HTTPException(
                status_code=404,
                detail="Department not found"
            )

        # ---------------- CHECK TEACHER ----------------

        teacher = db.query(models.Teacher).filter(
            models.Teacher.did == did
        ).first()

        if not teacher:

            raise HTTPException(
                status_code=404,
                detail="Teacher not found"
            )

        # ---------------- UPDATE DATA ----------------

        student.sname = sname

        student.rollno = rollno

        student.did = did

        student.tid = teacher.tid

        # ---------------- SAVE ----------------

        db.commit()

        db.refresh(student)

        return {

            "message": "Student updated successfully",

            "updated_student": student.student_dict()
        }

    except HTTPException:

        raise

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ---------------- SEARCH STUDENT ----------------

@app.get("/students/{sid}", tags=["Students"])
def search_student(
    sid: int,
    db: Session = Depends(get_db)
):

    try:

        student = db.query(models.Student).filter(
            models.Student.sid == sid
        ).first()

        if not student:

            raise HTTPException(
                status_code=404,
                detail="Student not found"
            )

        return student.student_dict()

    except HTTPException:

        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
# ---------------- GET SUBJECTS BY TEACHER ID ----------------

@app.get("/teachers/{tid}/subjects", tags=["Teachers", "Subjects"])
def get_subjects_by_teacher(

    tid: int,
    db: Session = Depends(get_db)

):

    try:

        # ---------------- VALIDATE TEACHER ----------------

        teacher = db.query(models.Teacher).filter(
            models.Teacher.tid == tid
        ).first()

        if not teacher:
            raise HTTPException(
                status_code=404,
                detail="Teacher not found"
            )

        # ---------------- FETCH SUBJECTS ----------------

        subjects = db.query(models.Subject).filter(
            models.Subject.tid == tid
        ).all()

        if not subjects:
            raise HTTPException(
                status_code=404,
                detail="No subjects assigned to this teacher"
            )

        # ---------------- RETURN RESPONSE ----------------

        return {
            "teacher_id": tid,
            "teacher_name": teacher.tname,
            "subjects": [
                subject.subject_dict()
                for subject in subjects
            ]
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching subjects: {str(e)}"
        )
        
# ---------------- GET SUBJECTS BY TEACHER ID ----------------

@app.get("/teachers/{tid}/subjects", tags=["Teachers", "Subjects"])
def get_subjects_by_teacher(

    tid: int,
    db: Session = Depends(get_db)

):

    try:

        # ---------------- CHECK TEACHER ----------------

        teacher = db.query(models.Teacher).filter(
            models.Teacher.tid == tid
        ).first()

        if not teacher:
            raise HTTPException(
                status_code=404,
                detail="Teacher not found"
            )

        # ---------------- FETCH SUBJECTS ----------------

        subjects = db.query(models.Subject).filter(
            models.Subject.tid == tid
        ).all()

        if not subjects:
            raise HTTPException(
                status_code=404,
                detail="No subjects found for this teacher"
            )

        # ---------------- FORMAT RESPONSE ----------------

        return {
            "teacher_id": teacher.tid,
            "teacher_name": teacher.tname,
            "subjects": [
                {
                    "code": subject.code,
                    "sub1": subject.sub1,
                    "sub2": subject.sub2,
                    "sub3": subject.sub3,
                    "department_id": subject.did
                }
                for subject in subjects
            ]
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching subjects: {str(e)}"
        )
    
# ---------------- SEARCH DEPARTMENT STUDENT ----------------

@app.get("/students/department/{did}",tags=["Students","Departments"])
def search_student(
    did: int,
    db: Session = Depends(get_db)
):

    try:

        students = db.query(models.Student).filter(
            models.Student.did == did
        ).all()

        if not students:

            raise HTTPException(
                status_code=404,
                detail="Department not found or no students available"
            )

        return [
            student.student_dict()
            for student in students
        ]

    except HTTPException:

        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ---------------- DELETE STUDENT ----------------

@app.delete("/students/{sid}",tags=["Students"])
def delete_student(
    sid: int,
    db: Session = Depends(get_db)
):

    try:

        student = db.query(models.Student).filter(
            models.Student.sid == sid
        ).first()

        if not student:

            raise HTTPException(
                status_code=404,
                detail="Student not found"
            )

        db.delete(student)

        db.commit()

        return {
            "message": "Student deleted successfully"
        }

    except HTTPException:

        raise

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )