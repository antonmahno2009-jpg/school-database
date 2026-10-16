import sqlite3


# Pieslēgšanās skolas datubāzei
def connect():
    database = sqlite3.connect("school.db")
    database.execute("PRAGMA foreign_keys = ON")
    return database


# Pievienot priekšmetu
def add_subject(name, teacher):
    database = connect()
    cursor = database.cursor()

    cursor.execute(
        """
        INSERT INTO subjects(name, teacher_name)
        VALUES (?, ?)
        """,
        (name, teacher)
    )

    database.commit()
    subject_id = cursor.lastrowid
    database.close()

    return subject_id


# Pievienot mājasdarbu
def add_homework(subject_id, description, deadline, completed):
    database = connect()
    cursor = database.cursor()

    cursor.execute(
        """
        INSERT INTO homework(subject_id, description, deadline, completed)
        VALUES (?, ?, ?, ?)
        """,
        (subject_id, description, deadline, completed)
    )

    database.commit()
    homework_id = cursor.lastrowid
    database.close()

    return homework_id


# Pievienot atzīmi
def add_grade(subject_id, grade_value, grade_date):
    database = connect()
    cursor = database.cursor()

    cursor.execute(
        """
        INSERT INTO grades(subject_id, grade_value, grade_date)
        VALUES (?, ?, ?)
        """,
        (subject_id, grade_value, grade_date)
    )

    database.commit()
    grade_id = cursor.lastrowid
    database.close()

    return grade_id


# Pievienot personīgo attīstību (PD)
def add_pd(subject_id, pd_date):
    database = connect()
    cursor = database.cursor()

    cursor.execute(
        """
        INSERT INTO pd(subject_id, pd_date)
        VALUES (?, ?)
        """,
        (subject_id, pd_date)
    )

    database.commit()
    pd_id = cursor.lastrowid
    database.close()

    return pd_id


# Iegūt visus priekšmetus
def get_subjects():
    database = connect()
    cursor = database.cursor()

    cursor.execute(
        """
        SELECT prieksmeti_id, nosaukums, skolotajs
        FROM prieksmeti
        ORDER BY prieksmeti_id
        """
    )

    subjects = cursor.fetchall()
    database.close()

    return subjects


# Iegūt visus mājasdarbus
def get_homework():
    database = connect()
    cursor = database.cursor()

    cursor.execute(
        """
        SELECT
            majasdarbi.majasdarbi_id,
            prieksmeti.nosaukums,
            majasdarbi.apraksts,
            majasdarbi.termins
        FROM majasdarbi
        JOIN prieksmeti
            ON majasdarbi.prieksmeti_id = prieksmeti.prieksmeti_id
        ORDER BY majasdarbi.majasdarbi_id
        """
    )

    homework = cursor.fetchall()
    database.close()

    return homework


# Iegūt visas atzīmes
def get_grades():
    database = connect()
    cursor = database.cursor()

    cursor.execute(
        """
        SELECT
            atzimes.atzimes_id,
            prieksmeti.nosaukums,
            atzimes.atzime,
            atzimes.datums
        FROM atzimes
        JOIN prieksmeti
            ON atzimes.prieksmeti_id = prieksmeti.prieksmeti_id
        ORDER BY atzimes.atzimes_id
        """
    )

    grades = cursor.fetchall()
    database.close()

    return grades


# Iegūt visus PD ierakstus
def get_pd():
    database = connect()
    cursor = database.cursor()

    cursor.execute(
        """
        SELECT
            pd.pd_id,
            prieksmeti.nosaukums,
            pd.datums
        FROM pd
        JOIN prieksmeti
            ON pd.prieksmeti_id = prieksmeti.prieksmeti_id
        ORDER BY pd.pd_id
        """
    )

    pd_records = cursor.fetchall()
    database.close()

    return pd_records
