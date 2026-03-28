import sqlite3

conn = sqlite3.connect("my3.db")
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS faculties (
        faculty_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        dean TEXT
    )
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        student_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        age INTEGER,
        faculty_id INTEGER,
        FOREIGN KEY (faculty_id) REFERENCES faculties(faculty_id)
    )
""")

cur.execute("DELETE FROM students")
cur.execute("DELETE FROM faculties")

faculties = [
    ("Факультет информационных технологий", "Иванов А.А."),
    ("Экономический факультет", "Петрова М.И."),
    ("Юридический факультет", "Сидоров В.В."),
    ("Факультет иностранных языков", "Кузнецова О.П.")
]

cur.executemany("INSERT INTO faculties (name, dean) VALUES (?, ?)", faculties)

students = [
    ("Алексей", "Смирнов", 20, 1),
    ("Мария", "Иванова", 21, 2),
    ("Дмитрий", "Петров", 19, 1),
    ("Ольга", "Сидорова", 22, 3),
    ("Иван", "Кузнецов", 20, 2),
    ("Елена", "Васильева", 21, 1),
    ("Сергей", "Павлов", 23, 4),
    ("Анна", "Николаева", 19, 3),
    ("Андрей", "Федоров", 20, None),
    ("Наталья", "Михайлова", 21, 99)
]

cur.executemany("INSERT INTO students (first_name, last_name, age, faculty_id) VALUES (?, ?, ?, ?)", students)

conn.commit()

print("Данные успешно добавлены!")
print(f"Факультетов: {cur.execute('SELECT COUNT(*) FROM faculties').fetchone()[0]}")
print(f"Студентов: {cur.execute('SELECT COUNT(*) FROM students').fetchone()[0]}")

cur.execute("""
    SELECT 
        s.first_name,
        s.last_name,
        s.age,
        f.name as faculty_name
    FROM students s
    INNER JOIN faculties f ON s.faculty_id = f.faculty_id
    ORDER BY s.last_name
""")

print("Студенты с факультетами (INNER JOIN):")
for student in cur.fetchall():
    print(f"{student[0]:10} {student[1]:12} | Возраст: {student[2]:2} | Факультет: {student[3]}")
