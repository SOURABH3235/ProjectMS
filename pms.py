import json
from abc import ABC, abstractmethod
from pathlib import Path


database = Path(__file__).with_name("school_database.json")
default_data = {"students": [], "teachers": []}

data = default_data.copy()
if database.exists():
    try:
        content = database.read_text()
        if content.strip():
            loaded_data = json.loads(content)
            if isinstance(loaded_data, dict):
                data = loaded_data
    except (json.JSONDecodeError, OSError):
        data = default_data.copy()


def save_data():
    with open(database, "w") as file:
        json.dump(data, file, indent=2)


class Person(ABC):
    @abstractmethod
    def get_role(self):
        pass

    @abstractmethod
    def register(self):
        pass

    @abstractmethod
    def show_details(self):
        pass

    @staticmethod
    def validate_email(email):
        return "@" in email and "." in email


class Student(Person):
    def get_role(self):
        return "Student"

    def register(self):
        name = input("Enter student name: ")
        age = int(input("Enter student age: "))
        email = input("Enter student email: ")
        roll_number = input("Enter student roll number: ")

        if not Person.validate_email(email):
            print("Invalid email format. Registration failed.")
            return

        for student in data["students"]:
            if student["roll_number"] == roll_number:
                print("Student with this roll number already exists.")
                return

        student_data = {
            "name": name,
            "age": age,
            "email": email,
            "roll_number": roll_number,
            "marks": {},
        }
        data["students"].append(student_data)
        save_data()
        print(f"Student {name} registered successfully.")

    def show_details(self):
        details = input("Enter student roll number to view details: ")
        for student in data["students"]:
            if student["roll_number"] == details:
                print(f"Name: {student['name']}, Age: {student['age']}, Email: {student['email']}, Roll Number: {student['roll_number']}")
                if student.get("marks"):
                    print("Marks:")
                    for subject, marks in student["marks"].items():
                        print(f"  {subject}: {marks}")
                return
        print("Student not found.")

    def add_marks(self):
        roll_number = input("Enter student roll number: ")
        for student in data["students"]:
            if student["roll_number"] == roll_number:
                subject = input("Enter subject name: ")
                try:
                    marks = float(input("Enter marks: "))
                except ValueError:
                    print("Invalid marks entered.")
                    return

                student.setdefault("marks", {})[subject] = marks
                save_data()
                print(f"Marks added successfully for {student['name']} in {subject}.")
                return
        print("Student not found.")


class Teacher(Person):
    def get_role(self):
        return "Teacher"

    def register(self):
        name = input("Enter teacher name: ")
        age = int(input("Enter teacher age: "))
        email = input("Enter teacher email: ")
        subject = input("Enter teacher subject: ")

        if not Person.validate_email(email):
            print("Invalid email format. Registration failed.")
            return

        for teacher in data["teachers"]:
            if teacher["email"] == email:
                print("Teacher with this email already exists.")
                return

        teacher_data = {"name": name, "age": age, "email": email, "subject": subject}
        data["teachers"].append(teacher_data)
        save_data()
        print(f"Teacher {name} registered successfully.")

    def show_details(self):
        email = input("Enter teacher email to view details: ")
        for teacher in data["teachers"]:
            if teacher["email"] == email:
                print(f"Name: {teacher['name']}, Age: {teacher['age']}, Email: {teacher['email']}, Subject: {teacher['subject']}")
                return
        print("Teacher not found.")


if __name__ == "__main__":
    while True:
        print("\npress 1 to register a student")
        print("press 2 to register a teacher")
        print("press 3 to add marks of student")
        print("press 4 to view teacher details")
        print("press 5 to view student details")
        print("press 0 to exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            Student().register()
        elif choice == "2":
            Teacher().register()
        elif choice == "3":
            Student().add_marks()
        elif choice == "4":
            Teacher().show_details()
        elif choice == "5":
            Student().show_details()
        elif choice == "0":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

