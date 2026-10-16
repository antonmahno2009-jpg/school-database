import sqlite3
from funkcijas import(connect, add_subject, add_homework, add_grade, add_pd)

database = sqlite3.connect("school.db")
cursor = database.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS subjects(
        subject_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        teacher_name TEXT NOT NULL)
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS homework(
        homework_id INTEGER PRIMARY KEY,
        subject_id INTEGER NOT NULL,
        description TEXT,
        deadline DATETIME NOT NULL,
        completed BOOLEAN NOT NULL DEFAULT 0,

        FOREIGN KEY (subject_id)
            REFERENCES subjects (subject_id)
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS grades(
        grade_id INTEGER PRIMARY KEY,
        subject_id INTEGER NOT NULL,
        grade_value INTEGER NOT NULL,
        grade_date DATE NOT NULL,
               
        FOREIGN KEY (subject_id)
            REFERENCES subjects(subject_id)
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS pd(
        pd_id INTEGER PRIMARY KEY,
        subject_id INTEGER NOT NULL,
        pd_date DATE NOT NULL,
               
        FOREIGN KEY (subject_id)
            REFERENCES subjects(subject_id)
    )
""")

#dati
cursor.execute("""
INSERT OR IGNORE INTO subjects(subject_id, name, teacher_name)
    VALUES(1, "Matematika", "Gita Rjabova")
""")
cursor.execute("""
INSERT OR IGNORE INTO subjects(subject_id, name, teacher_name)
    VALUES(2, "Latviesu valoda", "Inga Sokolova")
""")

cursor.execute("""
INSERT OR IGNORE INTO homework(homework_id, subject_id, description, deadline, completed)
    VALUES(1, 1, "Matemātikas mājas darbs", "2026-10-15 17:00:00", 0)
""")
cursor.execute("""
INSERT OR IGNORE INTO homework(homework_id, subject_id, description, deadline, completed)
    VALUES(2, 2, "dzejolis", "2026-11-01 09:00:00", 1)
""")

cursor.execute("""
INSERT OR IGNORE INTO grades(grade_id, subject_id, grade_value, grade_date)
    VALUES(1, 2, 10, "2026-10-16")
""")
cursor.execute("""
INSERT OR IGNORE INTO grades(grade_id, subject_id, grade_value, grade_date)
    VALUES(2, 1, 7, "2026-11-16")
""")

cursor.execute("""
INSERT OR IGNORE INTO pd(pd_id, subject_id, pd_date)
    VALUES(1, 1, "2026-10-20")
""")
cursor.execute("""
INSERT OR IGNORE INTO pd(pd_id, subject_id, pd_date)
    VALUES(1, 1, "2026-11-20")
""")

#execute
cursor.execute ("""
    SELECT *
    FROM subjects
""")

subjects = cursor.fetchall()

print("\nsubjects")

for s in subjects:
    print(subjects)

#select
cursor.execute ("""
SELECT
    homework.homework_id,
    homework.description,
    homework.deadline,
    homework.completed
FROM homework
JOIN subjects
    ON homework.subject_id = subjects.subject_id
WHERE subjects.subject_id = 2
""")
homework = cursor.fetchall()

print("\nHOMEWORK")

for hw in homework:
    print(hw)


database.commit()