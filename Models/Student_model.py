class Student:
    def __init__(self, name, grades=None):
        self.name = name
        self.grades = grades or {}
    
    def add_grade(self, subject, grade):
        if subject in self.grades:
            self.grades[subject].append(grade)
        else:
            self.grades[subject] = [grade]
    
    def to_dict(self):
        return {
            "name": self.name,
            "grades": self.grades
        }