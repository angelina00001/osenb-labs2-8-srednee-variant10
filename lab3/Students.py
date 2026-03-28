class Student:
    def __init__(self, name, age, grade):
        self.name = name
        self.age = age
        self.grade = grade
    
    def display_info(self):
        return f"Студент: {self.name}, Возраст: {self.age}, Оценка: {self.grade}"

class GraduateStudent(Student):
    def __init__(self, name, age, grade, thesis):
        super().__init__(name, age, grade)
        self.thesis = thesis
    
    def display_info(self):
        return f"Аспирант: {self.name}, Тема диссертации: {self.thesis}"

if __name__ == "__main__":
    print("Тест наследования и полиморфизма:")
    student = Student("Андрей", 19, 4.5)
    grad_student = GraduateStudent("Дегтярев", 27, 5.0, "Зов Припяти")
    
    print(student.display_info())
    print(grad_student.display_info())
    
    students = [student, grad_student]
    print("\nТест полиморфизма:")
    for s in students:
        print(s.display_info())
    
