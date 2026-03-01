from app.db import Base, get_engine, get_session_factory
from app.repository import StudentRepository
from app.service import StudentService

#DB_URL = "mysql+mysqlconnector://root:@localhost:3306/testing_demo"
#DB_URL = "mysql+mysqlconnector://root:rootpass@localhost:3306/testing_demo"
# Na jednoduché lokálne skúšanie môžeme použiť aj:
DB_URL = "sqlite:///students.db"

def init_db():
    engine = get_engine(DB_URL)
    Base.metadata.create_all(engine)
    return engine

def main():
    engine = init_db()
    SessionLocal = get_session_factory(engine)

    with SessionLocal() as session:
        repo = StudentRepository(session)
        service = StudentService(repo)

        while True:
            print("\n--- STUDENT APP ---")
            print("1. Create student")
            print("2. List students")
            print("3. Update student")
            print("4. Delete student")
            print("5. Exit")

            choice = input("Choose option: ").strip()

            try:
                if choice == "1":
                    name = input("Name: ")
                    email = input("Email: ")
                    student = service.create_student(name, email)
                    print(f"Created: {student}")

                elif choice == "2":
                    students = service.list_students()
                    if not students:
                        print("No students found.")
                    for s in students:
                        print(s)

                elif choice == "3":
                    student_id = int(input("Student ID: "))
                    name = input("New name: ")
                    email = input("New email: ")
                    updated = service.update_student(student_id, name, email)
                    print(f"Updated: {updated}")

                elif choice == "4":
                    student_id = int(input("Student ID: "))
                    service.delete_student(student_id)
                    print("Deleted.")

                elif choice == "5":
                    print("Bye.")
                    break

                else:
                    print("Invalid option.")

            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    main()