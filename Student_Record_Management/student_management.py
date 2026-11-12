
import csv
import json
import os
CSV_FILE = "students.csv"
JSON_FILE = "students.json"
students = []
def choose_storage():
    print("\nChoose Storage Format")
    print("1. CSV")
    print("2. JSON")
    choice = input("Enter choice: ")
    if choice == "1":
        return CSV_FILE
    elif choice == "2":
        return JSON_FILE
    else:
        print("Invalid choice!")
        return None
def load_students(filename):
    if not os.path.exists(filename):
        return []
    try:
        if filename.endswith(".csv"):
            with open(filename, "r", newline="") as file:
                return list(csv.DictReader(file))
        else:
            with open(filename, "r") as file:
                return json.load(file)
    except (OSError, json.JSONDecodeError, csv.Error) as e:
        print("Error reading file:", e)
        return []
def save_students(filename, data):
    try:
        if filename.endswith(".csv"):
            with open(filename, "w", newline="") as file:
                fields = ["ID", "Name", "Age", "Department", "Marks"]
                writer = csv.DictWriter(file, fieldnames=fields)
                writer.writeheader()
                writer.writerows(data)
        else:
            with open(filename, "w") as file:
                json.dump(data, file, indent=4)
        return True
    except (OSError, csv.Error, TypeError) as e:
        print("Error saving file:", e)
        return False
def add_student(filename, data):
    try:
        sid = input("Enter Student ID: ").strip()
        if any(s["ID"] == sid for s in data):
            print("Student ID already exists!")
            return
        name = input("Enter Name: ").strip()
        age = int(input("Enter Age: "))
        department = input("Enter Department: ").strip()
        marks = float(input("Enter Marks: "))
        if not sid or not name or not department:
            print("Fields cannot be empty!")
            return
        if age <= 0 or not 0 <= marks <= 100:
            print("Invalid age or marks!")
            return
        student = {
            "ID": sid,
            "Name": name,
            "Age": age,
            "Department": department,
            "Marks": marks
        }
        data.append(student)
        if save_students(filename, data):
            print("Student added successfully!")
    except ValueError:
        print("Please enter valid numbers!")
def view_students(data):
    if not data:
        print("No student records found!")
        return
    print("\n--- STUDENT RECORDS ---")
    for student in data:
        print(student)
def search_student(data):
    sid = input("Enter Student ID: ").strip()
    result = list(filter(lambda s: s["ID"] == sid, data))
    if result:
        print("Student Found:", result[0])
    else:
        print("Student not found!")
def update_student(filename, data):
    sid = input("Enter Student ID to update: ").strip()
    for student in data:
        if student["ID"] == sid:
            try:
                name = input("New Name: ").strip()
                age = int(input("New Age: "))
                department = input("New Department: ").strip()
                marks = float(input("New Marks: "))

                if not name or not department:
                    print("Fields cannot be empty!")
                    return
                if age <= 0 or not 0 <= marks <= 100:
                    print("Invalid age or marks!")
                    return
                student["Name"] = name
                student["Age"] = age
                student["Department"] = department
                student["Marks"] = marks
                if save_students(filename, data):
                    print("Student updated successfully!")
                return
            except ValueError:
                print("Invalid input!")
                return
    print("Student not found!")
def delete_student(filename, data):
    sid = input("Enter Student ID to delete: ").strip()
    new_data = [s for s in data if s["ID"] != sid]
    if len(new_data) == len(data):
        print("Student not found!")
        return
    if save_students(filename, new_data):
        data.clear()
        data.extend(new_data)
        print("Student deleted successfully!")
def main():
    filename = choose_storage()
    if filename is None:
        return
    data = load_students(filename)
    while True:
        print("\n===== STUDENT RECORD MANAGEMENT =====")
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Exit")
        try:
            choice = int(input("Enter your choice: "))
            if choice == 1:
                add_student(filename, data)
            elif choice == 2:
                view_students(data)
            elif choice == 3:
                search_student(data)
            elif choice == 4:
                update_student(filename, data)
            elif choice == 5:
                delete_student(filename, data)
            elif choice == 6:
                print("Thank you for using the system!")
                break
            else:
                print("Invalid choice!")
        except ValueError:
            print("Enter a valid menu number!")
        finally:
            print("Operation completed.")
if __name__ == "__main__":
    main()