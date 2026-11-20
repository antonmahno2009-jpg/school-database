import sqlite3

KEYS = {"subjects": "subject_id", "homework": "homework_id",
        "grades": "grade_id", "pd": "pd_id",
        "lessons": "lesson_id", "notes": "note_id",
        "absences": "absence_id", "pd_topics": "topic_id"}


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

    # --- Jaunās tabulas ---
    # Stundu saraksts -> subjects
    run("""CREATE TABLE IF NOT EXISTS lessons(
        lesson_id INTEGER PRIMARY KEY,
        subject_id INTEGER NOT NULL,
        weekday INTEGER NOT NULL CHECK (weekday BETWEEN 1 AND 5),
        lesson_number INTEGER NOT NULL,
        room TEXT NOT NULL,
        FOREIGN KEY (subject_id) REFERENCES subjects (subject_id))""")
    # Piezīmes -> subjects
    run("""CREATE TABLE IF NOT EXISTS notes(
        note_id INTEGER PRIMARY KEY,
        subject_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        note_date DATE NOT NULL,
        FOREIGN KEY (subject_id) REFERENCES subjects (subject_id))""")
    # Kavējumi -> lessons (un caur to uz subjects)
    run("""CREATE TABLE IF NOT EXISTS absences(
        absence_id INTEGER PRIMARY KEY,
        lesson_id INTEGER NOT NULL,
        absence_date DATE NOT NULL,
        reason TEXT NOT NULL,
        excused BOOLEAN NOT NULL DEFAULT 0,
        FOREIGN KEY (lesson_id) REFERENCES lessons (lesson_id))""")
    # Pārbaudes darbu tēmas -> pd
    run("""CREATE TABLE IF NOT EXISTS pd_topics(
        topic_id INTEGER PRIMARY KEY,
        pd_id INTEGER NOT NULL,
        topic TEXT NOT NULL,
        prepared BOOLEAN NOT NULL DEFAULT 0,
        FOREIGN KEY (pd_id) REFERENCES pd (pd_id))""")


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


def add_lesson(subject_id, weekday, lesson_number, room):
    run("INSERT INTO lessons(subject_id, weekday, lesson_number, room) VALUES (?, ?, ?, ?)",
        (subject_id, weekday, lesson_number, room))


def add_note(subject_id, title, content, note_date):
    run("INSERT INTO notes(subject_id, title, content, note_date) VALUES (?, ?, ?, ?)",
        (subject_id, title, content, note_date))


def add_absence(lesson_id, absence_date, reason, excused):
    run("INSERT INTO absences(lesson_id, absence_date, reason, excused) VALUES (?, ?, ?, ?)",
        (lesson_id, absence_date, reason, excused))


def add_topic(pd_id, topic, prepared):
    run("INSERT INTO pd_topics(pd_id, topic, prepared) VALUES (?, ?, ?)",
        (pd_id, topic, prepared))


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


def get_lessons():
    return run("""
        SELECT l.lesson_id, s.name,
               CASE l.weekday WHEN 1 THEN 'Pirmdiena' WHEN 2 THEN 'Otrdiena'
                              WHEN 3 THEN 'Trešdiena' WHEN 4 THEN 'Ceturtdiena'
                              ELSE 'Piektdiena' END,
               l.lesson_number, l.room
        FROM lessons l JOIN subjects s ON l.subject_id = s.subject_id
        ORDER BY l.weekday, l.lesson_number""")


def get_notes():
    return run("""
        SELECT n.note_id, s.name, n.title, n.content, n.note_date
        FROM notes n JOIN subjects s ON n.subject_id = s.subject_id
        ORDER BY n.note_date DESC""")


def get_absences():
    return run("""
        SELECT a.absence_id, s.name, a.absence_date, a.reason,
               CASE a.excused WHEN 1 THEN 'Attaisnots' ELSE 'Neattaisnots' END
        FROM absences a
        JOIN lessons l ON a.lesson_id = l.lesson_id
        JOIN subjects s ON l.subject_id = s.subject_id
        ORDER BY a.absence_date DESC""")


def get_topics():
    return run("""
        SELECT t.topic_id, s.name, p.pd_date, t.topic,
               CASE t.prepared WHEN 1 THEN 'Sagatavots' ELSE 'Jāmācās' END
        FROM pd_topics t
        JOIN pd p ON t.pd_id = p.pd_id
        JOIN subjects s ON p.subject_id = s.subject_id
        ORDER BY p.pd_date, t.prepared""")


# Dzēst
def delete_record(table, record_id):
    if table == "subjects":
        run("""DELETE FROM absences WHERE lesson_id IN
               (SELECT lesson_id FROM lessons WHERE subject_id = ?)""", (record_id,))
        run("""DELETE FROM pd_topics WHERE pd_id IN
               (SELECT pd_id FROM pd WHERE subject_id = ?)""", (record_id,))
        for child in ("homework", "grades", "pd", "lessons", "notes"):
            run(f"DELETE FROM {child} WHERE subject_id = ?", (record_id,))
    elif table == "lessons":
        run("DELETE FROM absences WHERE lesson_id = ?", (record_id,))
    elif table == "pd":
        run("DELETE FROM pd_topics WHERE pd_id = ?", (record_id,))
    if table in KEYS:
        run(f"DELETE FROM {table} WHERE {KEYS[table]} = ?", (record_id,))


# tabula: (BOOLEAN kolonna, atslēga)
FLAGS = {"homework": ("completed", "homework_id"),
         "absences": ("excused", "absence_id"),
         "pd_topics": ("prepared", "topic_id")}


def toggle_flag(table, record_id):
    column, key = FLAGS[table]
    run(f"UPDATE {table} SET {column} = 1 - {column} WHERE {key} = ?", (record_id,))


def toggle_homework(homework_id):
    run("UPDATE homework SET completed = 1 - completed WHERE homework_id = ?", (homework_id,))