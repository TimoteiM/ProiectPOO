import pymongo
import tkinter as tk
from tkinter import messagebox
from bson.objectid import ObjectId
from Models.Student_model import Student
from config import *



class StudentManager:
    def __init__(self):
        self.client = MongoClient("localhost", 27017)
        self.db = self.client["student_db"]
        self.collection = self.db["students"]
        
    def add_student(self, name, grades):
        student = Student(name, grades)
        student_dict = student.to_dict()
        result = self.collection.insert_one(student_dict)
        return result.inserted_id
        
    def get_student(self, name):
        student_dict = self.collection.find_one({"name": name})
        return Student(student_dict["name"], student_dict["grades"]) if student_dict else None
    
    def get_all_students(self):
        student_dicts = self.collection.find({})
        return [Student(student_dict["name"], student_dict["grades"]) for student_dict in student_dicts]
    
    def update_student(self, name, grades):
        student_dict = self.collection.find_one({"name": name})
        if student_dict:
            student_dict["grades"] = grades
            result = self.collection.update_one({"_id": ObjectId(student_dict["_id"])}, {"$set": student_dict})
            return result.modified_count
        else:
            return 0
    
    def delete_student(self, name):
        result = self.collection.delete_one({"name": name})
        return result.deleted_count
        
    def evaluate_student(self, name):
        query = {"name": name}
        student = self.collection.find_one(query)
        if student:
            grades = student["grades"]
            avg_grade = sum(grades.values()) / len(grades)
            return avg_grade
        return None


class StudentGUI:
    def __init__(self, manager):
        self.manager = manager
        self.window = tk.Tk()
        self.window.title("Student Manager")
        
        # Creare caseta pentru numele studentului
        name_label = tk.Label(self.window, text="Name")
        name_label.grid(row=0, column=0)
        self.name_entry = tk.Entry(self.window)
        self.name_entry.grid(row=0, column=1)
        
        # Create caseta pentru fiecare disciplina si notele acestora
        self.subjects = ["Matematica", "Engleza", "Programare"]
        self.grade_boxes = {}
        for i, subject in enumerate(self.subjects):
            label = tk.Label(self.window, text=subject)
            label.grid(row=i+1, column=0)
            grade_box = tk.Text(self.window, height=1, width=20)
            grade_box.grid(row=i+1, column=1)
            self.grade_boxes[subject] = grade_box

        def get_grades(self):
            grades = {}
            for subject, grade_box in self.grade_boxes.items():
                grades[subject] = [int(grade) for grade in grade_box.get("1.0", tk.END).strip().split(";")]
            return grades
        
        # Creare buton de agaudare a studentului
        add_button = tk.Button(self.window, text="Add Student", command=self.add_student)
        add_button.grid(row=len(self.subjects)+1, column=0)

        update_button = tk.Button(self.window, text="Update Student", command=self.update_student)
        update_button.grid(row=len(self.subjects)+1, column=1)
        
        # Creare lista 
        self.student_listbox = tk.Listbox(self.window)
        self.student_listbox.grid(row=0, column=2, rowspan=len(self.subjects)+2)
        self.refresh_students()
        
        # Afisare metoda aleasa
        self.student_listbox.bind('<<ListboxSelect>>', self.display_student)
        
        # Creare buton pentru a vizualiza toti studentii
        view_all_students_button = tk.Button(self.window, text="View All Students", command=self.view_all_students)
        view_all_students_button.grid(row=len(self.subjects)+2, column=0)
        
        # Creare buton de stergere a unui student
        delete_button = tk.Button(self.window, text="Delete Student", command=self.delete_student)
        delete_button.grid(row=len(self.subjects)+2, column=1)
        
        # Creare lista studenti
        self.student_listbox = tk.Listbox(self.window)
        self.student_listbox.grid(row=0, column=2, rowspan=len(self.subjects)+3)
        self.refresh_students()
        
        #Afisare metoda studenti
        self.student_listbox.bind('<<ListboxSelect>>', self.display_student)
        
        #Ruleaza main-ul intr-un loop
        self.window.mainloop()
    def add_student(self):
        name = self.name_entry.get()
        grades = {}
        for subject in self.subjects:
            grade_input = self.grade_boxes[subject].get("1.0", tk.END).strip()
            if grade_input:
                grade_list = grade_input.split()
                grade_list = [int(grade) for grade in grade_list]
                grades[subject] = grade_list
        self.manager.add_student(name, grades)
        self.refresh_students()
    
    
    def update_student(self):
        name = self.name_entry.get()
        grades = {}
        for subject in self.subjects:
            grade_input = self.grade_boxes[subject].get("1.0", tk.END).strip()
            if grade_input:
                grade_list = grade_input.split()
                grade_list = [int(grade) for grade in grade_list]
                grades[subject] = grade_list
        count = self.manager.update_student(name, grades)
        if count:
            self.refresh_students()
            messagebox.showinfo("Success", f"Student '{name}' has been updated.")
        else:
            messagebox.showerror("Error", f"Could not find student '{name}'.")
        self.window.mainloop()
    
    def display_student(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            name = self.student_listbox.get(index)
            student = self.manager.get_student(name)
            if student:
                self.name_entry.delete(0, tk.END)
                self.name_entry.insert(0, student.name)
                for subject, grade_box in self.grade_boxes.items():
                    grade_box.delete("1.0", tk.END)
                    if subject in student.grades:
                        grade_list = student.grades[subject]
                        grade_str = " ".join(str(grade) for grade in grade_list)
                        grade_box.insert("1.0", grade_str)
                    else:
                        grade_box.insert("1.0", "")

    def refresh_students(self):
        self.student_listbox.delete(0, tk.END)
        for student in self.manager.get_all_students():
            self.student_listbox.insert(tk.END, student.name)
    def view_all_students(self):
        students = self.manager.get_all_students()
        message = ""
        for student in students:
            message += f"{student.name}: {student.grades}\n"
        if not message:
            message = "No students found."
        messagebox.showinfo("All Students", message)

    def delete_student(self):
        selection = self.student_listbox.curselection()
        if selection:
            index = selection[0]
            name = self.student_listbox.get(index)
            self.manager.delete_student(name)
            self.refresh_students()
        else:
            messagebox.showwarning("Warning", "Please select a student to delete.")
    
            
    