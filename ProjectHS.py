import pickle
import os
from tabulate import tabulate
from getpass import getpass
from datetime import datetime

class ReportCardSoftware:
    def __init__(self):
        self.data_file = "student_data.pkl"
        self.access_granted = False

    def admin_login(self):
        """Handles admin authentication."""
        print("\n!!! Warning: Authorized Access Only !!!\n")
        username = input("Enter username: ")
        password = getpass("Enter password: ")

        if username == "admin" and password == "admin":
            self.access_granted = True
            print("Access granted. Welcome!")
        else:
            print("\nIncorrect username or password. Access denied.\n")

    def load_data(self):
        """Loads student data from the file."""
        if os.path.exists(self.data_file):
            with open(self.data_file, "rb") as file:
                return pickle.load(file)
        return {}

    def save_data(self, data):
        """Saves student data to the file."""
        with open(self.data_file, "wb") as file:
            pickle.dump(data, file)

    def add_student(self):
        """Adds a new student to the system."""
        student_data = self.load_data()
        roll_number = input("Enter student roll number: ")

        if roll_number in student_data:
            print("Student with this roll number already exists.")
            return

        name = input("Enter student name: ")
        grade = input("Enter student grade: ")
        marks = float(input("Enter student marks: "))
        student_data[roll_number] = {
            "Name": name,
            "Grade": grade,
            "Marks": marks,
        }
        self.save_data(student_data)
        print("Student added successfully.")

    def view_students(self):
        """Displays all student records in a tabular format."""
        student_data = self.load_data()
        if not student_data:
            print("No student records found.")
            return

        table = [[roll, info["Name"], info["Grade"], info["Marks"]] for roll, info in student_data.items()]
        print(tabulate(table, headers=["Roll Number", "Name", "Grade", "Marks"], tablefmt="grid"))

    def delete_student(self):
        """Deletes a student record by roll number."""
        student_data = self.load_data()
        roll_number = input("Enter roll number of the student to delete: ")

        if roll_number in student_data:
            del student_data[roll_number]
            self.save_data(student_data)
            print("Student record deleted successfully.")
        else:
            print("Student with this roll number does not exist.")

    def menu(self):
        """Displays the main menu and handles user actions."""
        if not self.access_granted:
            print("Unauthorized access. Please log in first.")
            return

        while True:
            print("\n--- Main Menu ---")
            print("1. Add Student")
            print("2. View Students")
            print("3. Delete Student")
            print("4. Exit")

            choice = input("Enter your choice: ")
            if choice == "1":
                self.add_student()
            elif choice == "2":
                self.view_students()
            elif choice == "3":
                self.delete_student()
            elif choice == "4":
                print("Exiting the system. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    software = ReportCardSoftware()
    software.admin_login()
    software.menu()
