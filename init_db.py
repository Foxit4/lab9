"""Недеструктивна ініціалізація SQLite: створює таблиці лише якщо їх немає,
навчальні дані додає лише в порожню БД. Безпечно викликати при кожному запуску."""
import sqlite3
from pathlib import Path
from werkzeug.security import generate_password_hash

SCHEMA = """
CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS disciplines (id INTEGER PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS grades (id INTEGER PRIMARY KEY,
  student_id INTEGER NOT NULL REFERENCES students(id),
  discipline_id INTEGER NOT NULL REFERENCES disciplines(id),
  value INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY,
  username TEXT NOT NULL UNIQUE, password_hash TEXT NOT NULL);
"""

USERS = [("teacher1", "ChangeMe#1"), ("викладач", "ChangeMe#2"), ("admin", "ChangeMe#3")]


def init_db(path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path)
    db.executescript(SCHEMA)
    if db.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0:
        for u, p in USERS:
            db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                       (u, generate_password_hash(p, method="scrypt")))
    if db.execute("SELECT COUNT(*) FROM students").fetchone()[0] == 0:
        db.executescript("""
INSERT INTO students (name) VALUES ('Іваненко Олена'),('Петренко Андрій'),('Коваль Марія');
INSERT INTO disciplines (name) VALUES ('Вебтехнології'),('Бази даних');
INSERT INTO grades (student_id, discipline_id, value) VALUES (1,1,90),(2,1,75),(3,2,82);
""")
    db.commit()
    db.close()


if __name__ == "__main__":
    import os
    d = os.environ.get("DATA_DIR", ".")
    init_db(os.environ.get("LAB_DB", os.path.join(d, "app.sqlite3")))
    print("БД ініціалізовано.")
