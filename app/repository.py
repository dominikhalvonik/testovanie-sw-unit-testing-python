from sqlalchemy.orm import Session
from app.models import Student

class StudentRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, name: str, email: str) -> Student:
        student = Student(name=name, email=email)
        self.session.add(student)
        self.session.commit()
        self.session.refresh(student)
        return student

    def get_all(self) -> list[Student]:
        return self.session.query(Student).order_by(Student.id).all()

    def get_by_id(self, student_id: int) -> Student | None:
        return self.session.get(Student, student_id)

    def update(self, student_id: int, name: str, email: str) -> Student | None:
        student = self.session.get(Student, student_id)
        if not student:
            return None

        student.name = name
        student.email = email
        self.session.commit()
        self.session.refresh(student)
        return student

    def delete(self, student_id: int) -> bool:
        student = self.session.get(Student, student_id)
        if not student:
            return False

        self.session.delete(student)
        self.session.commit()
        return True