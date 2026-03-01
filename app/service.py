import re
from app.repository import StudentRepository

class StudentService:
    def __init__(self, repository: StudentRepository):
        self.repository = repository

    def create_student(self, name: str, email: str):
        if not name or len(name.strip()) < 2:
            raise ValueError("Name must have at least 2 characters.")

        if not self._is_valid_email(email):
            raise ValueError("Invalid email address.")

        return self.repository.create(name.strip(), email.strip().lower())

    def list_students(self):
        return self.repository.get_all()

    def update_student(self, student_id: int, name: str, email: str):
        if student_id <= 0:
            raise ValueError("student_id must be > 0")

        if not self._is_valid_email(email):
            raise ValueError("Invalid email address.")

        updated = self.repository.update(student_id, name.strip(), email.strip().lower())
        if updated is None:
            raise ValueError("Student not found.")

        return updated

    def delete_student(self, student_id: int):
        if student_id <= 0:
            raise ValueError("student_id must be > 0")

        deleted = self.repository.delete(student_id)
        if not deleted:
            raise ValueError("Student not found.")

        return True

    def _is_valid_email(self, email: str) -> bool:
        pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        return re.match(pattern, email or "") is not None