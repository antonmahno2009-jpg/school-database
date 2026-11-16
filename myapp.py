from datetime import date, datetime
from tkinter import ttk, messagebox

import customtkinter as ctk

import funkcijas as db

ctk.set_appearance_mode("System")  # "System", "Dark", "Light"
ctk.set_default_color_theme("blue")

# Krāsas (gaišais, tumšais)
BG, CARD, BORDER = ("#F5F6F8", "#141517"), ("#FFFFFF", "#1E1F23"), ("#E4E6EA", "#2C2E33")
TEXT, MUTED = ("#1F2328", "#ECECEC"), ("#6B7280", "#8B909A")
ACCENT, DANGER, HOVER = ("#2F6FDE", "#4C8DFF"), ("#C0392B", "#E5675A"), ("#F0F1F4", "#26282D")

HINTS = {"date": "GGGG-MM-DD", "datetime": "GGGG-MM-DD HH:MM", "grade": "1–10"}
FORMATS = {"date": "%Y-%m-%d", "datetime": "%Y-%m-%d %H:%M"}

# Sadaļa: (tabula, get, add, kolonnas, lauki)
PAGES = {
    "Priekšmeti": ("subjects", db.get_subjects, db.add_subject,
                   ["ID", "Nosaukums", "Skolotājs"],
                   [("Nosaukums", "text"), ("Skolotājs", "text")]),
    "Mājasdarbi": ("homework", db.get_homework, db.add_homework,
                   ["ID", "Priekšmets", "Apraksts", "Termiņš", "Statuss"],
                   [("Priekšmets", "subject"), ("Apraksts", "text"),
                    ("Termiņš", "datetime"), ("Pabeigts", "done")]),
    "Atzīmes": ("grades", db.get_grades, db.add_grade,
                ["ID", "Priekšmets", "Atzīme", "Datums"],
                [("Priekšmets", "subject"), ("Atzīme", "grade"), ("Datums", "date")]),
    "Pārbaudes darbi": ("pd", db.get_pd, db.add_pd,
                        ["ID", "Priekšmets", "Datums"],
                        [("Priekšmets", "subject"), ("Datums", "date")]),
}


def font(size, bold=False):
    return ctk.CTkFont(size=size, weight="bold" if bold else "normal")


def card(parent):
    return ctk.CTkFrame(parent, fg_color=CARD, corner_radius=12,
                        border_width=1, border_color=BORDER)


def ghost(parent, text, command, color):
    return ctk.CTkButton(parent, text=text, command=command, height=32,
                         fg_color="transparent", border_width=1,
                         border_color=BORDER, text_color=color, hover_color=HOVER)


def style_tree():
    dark = ctk.get_appearance_mode() == "Dark"
    bg, fg, head, sel = (("#1E1F23", "#ECECEC", "#26282D", "#2D4F8A") if dark
                         else ("#FFFFFF", "#1F2328", "#F0F1F4", "#D6E4FB"))
    s = ttk.Style()
    s.theme_use("clam")
    s.configure("Treeview", background=bg, fieldbackground=bg, foreground=fg,
                rowheight=34, borderwidth=0, font=(None, 11))
    s.configure("Treeview.Heading", background=head, foreground=fg,
                relief="flat", padding=(10, 8), font=(None, 10, "bold"))
    s.map("Treeview", background=[("selected", sel)], foreground=[("selected", fg)])
    s.map("Treeview.Heading", background=[("active", head)])


def read(kind, widget, subjects):
    """Nolasa un pārbauda lauka vērtību; kļūdas gadījumā met ValueError."""
    value = widget.get() if kind == "done" else widget.get().strip()
    if kind == "done":
        return value
    if kind == "subject":
        if value not in subjects:
            raise ValueError("Vispirms pievieno priekšmetu.")
        return subjects[value]
    if not value:
        raise ValueError("Aizpildi visus laukus.")
    try:
        if kind == "grade":
            value = int(value)
            if not 1 <= value <= 10:
                raise ValueError
        elif kind in FORMATS:
            datetime.strptime(value, FORMATS[kind])
    except ValueError:
        raise ValueError(f"Nederīga vērtība ({HINTS[kind]}).")
    return value


class Page(ctk.CTkFrame):
    def __init__(self, master, title, table, get, add, columns, fields):
        super().__init__(master, fg_color="transparent")
        self.table, self.get, self.add, self.fields = table, get, add, fields
        self.subjects = {}
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        ctk.CTkLabel(self, text=title, text_color=TEXT, font=font(26, True)
                     ).grid(row=0, sticky="w", pady=(0, 16))

        # Forma
        form = card(self)
        form.grid(row=1, sticky="ew")
        self.widgets = []
        for i, (label, kind) in enumerate(fields):
            form.grid_columnconfigure(i, weight=0 if kind == "done" else 1)
            ctk.CTkLabel(form, text=label, text_color=MUTED
                         ).grid(row=0, column=i, sticky="w", padx=(16, 0), pady=(14, 0))
            if kind == "subject":
                w = ctk.CTkOptionMenu(form, values=["—"], height=36, anchor="w",
                                      dynamic_resizing=False)
            elif kind == "done":
                w = ctk.CTkSwitch(form, text="")
            else:
                w = ctk.CTkEntry(form, height=36, placeholder_text=HINTS.get(kind, ""))
                if kind == "date":
                    w.insert(0, date.today().isoformat())
            w.grid(row=1, column=i, sticky="ew", padx=(16, 0), pady=(4, 16))
            self.widgets.append(w)
        ctk.CTkButton(form, text="Pievienot", width=110, height=36, command=self.submit
                      ).grid(row=1, column=len(fields), padx=16, pady=(4, 16))

        self.status = ctk.CTkLabel(self, text="", anchor="w")
        self.status.grid(row=2, sticky="ew", pady=8)

        # Tabula
        box = card(self)
        box.grid(row=3, sticky="nsew")
        box.grid_columnconfigure(0, weight=1)
        box.grid_rowconfigure(0, weight=1)
        self.tree = ttk.Treeview(box, columns=columns, show="headings", selectmode="browse")
        for c in columns:
            self.tree.heading(c, text=c, anchor="w")
            self.tree.column(c, width=60 if c == "ID" else 200, anchor="w", stretch=c != "ID")
        self.tree.grid(row=0, column=0, sticky="nsew", padx=6, pady=6)
        bar = ctk.CTkScrollbar(box, command=self.tree.yview)
        bar.grid(row=0, column=1, sticky="ns", padx=4, pady=8)
        self.tree.configure(yscrollcommand=bar.set)

        # Rīki zem tabulas
        tools = ctk.CTkFrame(self, fg_color="transparent")
        tools.grid(row=4, sticky="ew", pady=(10, 0))
        self.count = ctk.CTkLabel(tools, text="", text_color=MUTED)
        self.count.pack(side="left")
        ghost(tools, "Dzēst atlasīto", self.delete, DANGER).pack(side="right")
        if table == "homework":
            ghost(tools, "Pabeigts / nepabeigts", self.toggle, ACCENT).pack(side="right", padx=8)

    def say(self, text, error=False):
        self.status.configure(text=text, text_color=DANGER if error else ACCENT)
        self.after(3000, lambda: self.status.configure(text=""))

    def refresh(self):
        self.subjects = {f"{name} (ID {i})": i for i, name, _ in db.get_subjects()}
        for w, (_, kind) in zip(self.widgets, self.fields):
            if kind == "subject":
                values = list(self.subjects) or ["—"]
                w.configure(values=values)
                if w.get() not in values:
                    w.set(values[0])
        rows = self.get()
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert("", "end", iid=str(row[0]), values=row)
        self.count.configure(text=f"Ieraksti: {len(rows)}")

    def submit(self):
        try:
            args = [read(k, w, self.subjects)
                    for w, (_, k) in zip(self.widgets, self.fields)]
        except ValueError as error:
            return self.say(str(error), error=True)
        self.add(*args)
        for w, (_, k) in zip(self.widgets, self.fields):
            if k in ("text", "datetime", "grade"):
                w.delete(0, "end")
        self.refresh()
        self.say("Pievienots.")

    def selected(self):
        sel = self.tree.selection()
        if not sel:
            self.say("Atlasi ierakstu tabulā.", error=True)
        return int(sel[0]) if sel else None

    def delete(self):
        record_id = self.selected()
        if record_id and messagebox.askyesno("Dzēst", "Dzēst atlasīto ierakstu?"):
            db.delete_record(self.table, record_id)
            self.refresh()

    def toggle(self):
        record_id = self.selected()
        if record_id:
            db.toggle_homework(record_id)
            self.refresh()


class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=BG)
        db.init_db()
        style_tree()
        self.title("Skolas datubāze")
        self.geometry("1100x720")
        self.minsize(900, 600)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        side = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color=CARD)
        side.grid(row=0, column=0, sticky="ns")
        side.grid_propagate(False)
        ctk.CTkLabel(side, text="Skolas datubāze", text_color=TEXT, font=font(17, True)
                     ).pack(anchor="w", padx=24, pady=(28, 24))

        main = ctk.CTkFrame(self, fg_color="transparent")
        main.grid(row=0, column=1, sticky="nsew", padx=32, pady=28)
        main.grid_columnconfigure(0, weight=1)
        main.grid_rowconfigure(0, weight=1)

        self.pages, self.nav = {}, {}
        for name, config in PAGES.items():
            self.pages[name] = Page(main, name, *config)
            self.pages[name].grid(row=0, column=0, sticky="nsew")
            self.nav[name] = ctk.CTkButton(
                side, text=name, anchor="w", height=38, fg_color="transparent",
                text_color=MUTED, hover_color=HOVER, font=font(14),
                command=lambda n=name: self.show(n))
            self.nav[name].pack(fill="x", padx=12, pady=2)
        self.show("Priekšmeti")

    def show(self, name):
        for n, button in self.nav.items():
            button.configure(fg_color=HOVER if n == name else "transparent",
                             text_color=ACCENT if n == name else MUTED)
        self.pages[name].refresh()
        self.pages[name].tkraise()


if __name__ == "__main__":
    App().mainloop()
