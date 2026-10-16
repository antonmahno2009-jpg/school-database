import tkinter as tk

from funkcijas import (
    add_subject,
    add_homework,
    add_grade,
    add_pd
)


def addSubjectFromWindow():
    name = name_input.get()
    teacher = teacher_input.get()

    add_subject(name, teacher)

    name_input.delete(0, tk.END)
    teacher_input.delete(0, tk.END)

    result.config(text="Priekšmets pievienots")


def addHomeworkFromWindow():
    subject_id = subject_input.get()
    description = description_input.get()
    deadline = deadline_input.get()
    completed = completed_input.get()

    add_homework(subject_id, description, deadline, completed)

    subject_input.delete(0, tk.END)
    description_input.delete(0, tk.END)
    deadline_input.delete(0, tk.END)
    completed_input.delete(0, tk.END)

    result2.config(text="Mājasdarbs pievienots")


def addGradeFromWindow():
    subject_id = grade_subject_input.get()
    grade_value = grade_input.get()
    grade_date = grade_date_input.get()

    add_grade(subject_id, grade_value, grade_date)

    grade_subject_input.delete(0, tk.END)
    grade_input.delete(0, tk.END)
    grade_date_input.delete(0, tk.END)

    result3.config(text="Atzīme pievienota")


def addPDFromWindow():
    subject_id = pd_subject_input.get()
    pd_date = pd_date_input.get()

    add_pd(subject_id, pd_date)

    pd_subject_input.delete(0, tk.END)
    pd_date_input.delete(0, tk.END)

    result4.config(text="PD pievienots")


window = tk.Tk()
window.title("Skolas datubāze")
window.geometry("800x950")

header = tk.Label(
    window,
    text="Skolas datubāze",
    font=("Arial", 20, "bold")
)
header.pack(pady=15)


# Priekšmeti
subject_block = tk.LabelFrame(
    window,
    text="Pievienot priekšmetu",
    padx=10,
    pady=1
)
subject_block.pack(fill="x", padx=20, pady=8)

tk.Label(subject_block, text="Priekšmeta nosaukums").pack()
name_input = tk.Entry(subject_block, width=60)
name_input.pack(pady=5)

tk.Label(subject_block, text="Skolotājs").pack()
teacher_input = tk.Entry(subject_block, width=60)
teacher_input.pack(pady=5)

tk.Button(
    subject_block,
    text="Pievienot priekšmetu",
    command=addSubjectFromWindow
).pack(pady=5)

result = tk.Label(subject_block, text="", fg="green")
result.pack(pady=5)


# Mājasdarbi
homework_block = tk.LabelFrame(
    window,
    text="Pievienot mājasdarbu",
    padx=10,
    pady=1
)
homework_block.pack(fill="x", padx=20, pady=8)

tk.Label(homework_block, text="Priekšmeta ID").pack()
subject_input = tk.Entry(homework_block, width=60)
subject_input.pack(pady=5)

tk.Label(homework_block, text="Mājasdarba apraksts").pack()
description_input = tk.Entry(homework_block, width=60)
description_input.pack(pady=5)

tk.Label(
    homework_block,
    text="Nodošanas termiņš (YYYY-MM-DD HH:MM:SS)"
).pack()
deadline_input = tk.Entry(homework_block, width=60)
deadline_input.pack(pady=5)

tk.Label(homework_block, text="Pabeigts (1 - Jā, 0 - Nē)").pack()
completed_input = tk.Entry(homework_block, width=60)
completed_input.pack(pady=5)

tk.Button(
    homework_block,
    text="Pievienot mājasdarbu",
    command=addHomeworkFromWindow
).pack(pady=5)

result2 = tk.Label(homework_block, text="", fg="green")
result2.pack(pady=5)


# Atzīmes
grade_block = tk.LabelFrame(
    window,
    text="Pievienot atzīmi",
    padx=10,
    pady=1
)
grade_block.pack(fill="x", padx=20, pady=8)

tk.Label(grade_block, text="Priekšmeta ID").pack()
grade_subject_input = tk.Entry(grade_block, width=60)
grade_subject_input.pack(pady=5)

tk.Label(grade_block, text="Atzīme").pack()
grade_input = tk.Entry(grade_block, width=60)
grade_input.pack(pady=5)

tk.Label(grade_block, text="Datums (YYYY-MM-DD)").pack()
grade_date_input = tk.Entry(grade_block, width=60)
grade_date_input.pack(pady=5)

tk.Button(
    grade_block,
    text="Pievienot atzīmi",
    command=addGradeFromWindow
).pack(pady=5)

result3 = tk.Label(grade_block, text="", fg="green")
result3.pack(pady=5)


# Personīgā attīstība (PD)
pd_block = tk.LabelFrame(
    window,
    text="Pievienot Parbaudes Darbus (PD)",
    padx=10,
    pady=1
)
pd_block.pack(fill="x", padx=20, pady=8)

tk.Label(pd_block, text="Priekšmeta ID").pack()
pd_subject_input = tk.Entry(pd_block, width=60)
pd_subject_input.pack(pady=5)

tk.Label(pd_block, text="Datums (YYYY-MM-DD)").pack()
pd_date_input = tk.Entry(pd_block, width=60)
pd_date_input.pack(pady=5)

tk.Button(
    pd_block,
    text="Pievienot PD",
    command=addPDFromWindow
).pack(pady=5)

result4 = tk.Label(pd_block, text="", fg="green")
result4.pack(pady=5)


window.mainloop()