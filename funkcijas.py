import sqlite3

KEYS = {"subjects": "subject_id", "homework": "homework_id",
        "grades": "grade_id", "pd": "pd_id"}


def connect():
    database = sqlite3.connect("school.db")
    database.execute("PRAGMA foreign_keys = ON")
    return database


def run(sql, params=()):
    database = connect()
    rows = database.execute(sql, params).fetchall()
    database.commit()
    database.close()
    return rows


def init_db():
    run("""CREATE TABLE IF NOT EXISTS subjects(
        subject_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        teacher_name TEXT NOT NULL)""")
    run("""CREATE TABLE IF NOT EXISTS homework(
        homework_id INTEGER PRIMARY KEY,
        subject_id INTEGER NOT NULL,
        description TEXT,
        deadline DATETIME NOT NULL,
        completed BOOLEAN NOT NULL DEFAULT 0,
        FOREIGN KEY (subject_id) REFERENCES subjects (subject_id))""")
    run("""CREATE TABLE IF NOT EXISTS grades(
        grade_id INTEGER PRIMARY KEY,
        subject_id INTEGER NOT NULL,
        grade_value INTEGER NOT NULL,
        grade_date DATE NOT NULL,
        FOREIGN KEY (subject_id) REFERENCES subjects (subject_id))""")
    run("""CREATE TABLE IF NOT EXISTS pd(
        pd_id INTEGER PRIMARY KEY,
        subject_id INTEGER NOT NULL,
        pd_date DATE NOT NULL,
        FOREIGN KEY (subject_id) REFERENCES subjects (subject_id))""")


# Pievienot
def add_subject(name, teacher):
    run("INSERT INTO subjects(name, teacher_name) VALUES (?, ?)", (name, teacher))


def add_homework(subject_id, description, deadline, completed):
    run("INSERT INTO homework(subject_id, description, deadline, completed) VALUES (?, ?, ?, ?)",
        (subject_id, description, deadline, completed))


def add_grade(subject_id, grade_value, grade_date):
    run("INSERT INTO grades(subject_id, grade_value, grade_date) VALUES (?, ?, ?)",
        (subject_id, grade_value, grade_date))


def add_pd(subject_id, pd_date):
    run("INSERT INTO pd(subject_id, pd_date) VALUES (?, ?)", (subject_id, pd_date))


# Iegūt
def get_subjects():
    return run("SELECT subject_id, name, teacher_name FROM subjects ORDER BY subject_id")


def get_homework():
    return run("""
        SELECT h.homework_id, s.name, h.description, h.deadline,
               CASE h.completed WHEN 1 THEN 'Pabeigts' ELSE 'Jāizdara' END
        FROM homework h JOIN subjects s ON h.subject_id = s.subject_id
        ORDER BY h.completed, h.deadline""")


def get_grades():
    return run("""
        SELECT g.grade_id, s.name, g.grade_value, g.grade_date
        FROM grades g JOIN subjects s ON g.subject_id = s.subject_id
        ORDER BY g.grade_date DESC""")


def get_pd():
    return run("""
        SELECT p.pd_id, s.name, p.pd_date
        FROM pd p JOIN subjects s ON p.subject_id = s.subject_id
        ORDER BY p.pd_date""")


# Dzēst
def delete_record(table, record_id):
    if table == "subjects":
        for child in ("homework", "grades", "pd"):
            run(f"DELETE FROM {child} WHERE subject_id = ?", (record_id,))
    if table in KEYS:
        run(f"DELETE FROM {table} WHERE {KEYS[table]} = ?", (record_id,))


def toggle_homework(homework_id):
    run("UPDATE homework SET completed = 1 - completed WHERE homework_id = ?", (homework_id,))
