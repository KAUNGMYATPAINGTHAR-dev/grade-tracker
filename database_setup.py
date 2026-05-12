import sqlite3

class DatabaseManager:
    """Handles database connection and table creation."""

    DB_NAME = "grades.db"

    def __init__(self):
        self.conn = None
        self._connect()
        self._create_tables()

    def _connect(self):
        try:
            self.conn = sqlite3.connect(self.DB_NAME)
            self.conn.row_factory = sqlite3.Row
            self.conn.execute("PRAGMA foreign_keys = ON")
            print(f"[DB] Connected to '{self.DB_NAME}'.")
        except sqlite3.Error as e:
            print(f"[DB ERROR] Could not connect: {e}")
            self.conn = None

    def _create_tables(self):
        if not self.conn:
            return
        sql_statements = [
            """CREATE TABLE IF NOT EXISTS students (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name  TEXT NOT NULL,
                email      TEXT NOT NULL UNIQUE
            );""",
            """CREATE TABLE IF NOT EXISTS courses (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id   INTEGER NOT NULL,
                name         TEXT NOT NULL,
                credit_hours REAL NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students(id),
                UNIQUE(student_id, name)
            );""",
            """CREATE TABLE IF NOT EXISTS assignments (
                id                INTEGER PRIMARY KEY AUTOINCREMENT,
                course_id         INTEGER NOT NULL,
                name              TEXT NOT NULL,
                category          TEXT,
                weight            REAL NOT NULL,
                score_numerator   REAL,
                score_denominator REAL NOT NULL,
                FOREIGN KEY (course_id) REFERENCES courses(id)
            );""",
        ]
        try:
            cur = self.conn.cursor()
            for sql in sql_statements:
                cur.execute(sql)
            self.conn.commit()
            print("[DB] Tables ready.")
        except sqlite3.Error as e:
            print(f"[DB ERROR] Could not create tables: {e}")

    def close(self):
        if self.conn:
            self.conn.close()
            print("[DB] Connection closed.")
