import sqlite3
import csv
from datetime import datetime


class Student:
    """Simple data model for a student."""
    def __init__(self, id, first_name, last_name, email):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email


class Course:
    """Simple data model for a course."""
    def __init__(self, id, student_id, name, credit_hours):
        self.id = id
        self.student_id = student_id
        self.name = name
        self.credit_hours = credit_hours


class Assignment:
    """Simple data model for an assignment."""
    def __init__(self, id, course_id, name, category, weight, score_num, score_den):
        self.id = id
        self.course_id = course_id
        self.name = name
        self.category = category
        self.weight = weight
        self.score_numerator = score_num
        self.score_denominator = score_den
        self.score_percent = (score_num / score_den) * 100 if score_den and score_num is not None else 0


class GradeTracker:
    """Handles all data insertion, grade calculation, and memo saving."""

    def __init__(self, db_manager):
        self.conn = db_manager.conn
        if not self.conn:
            raise ConnectionError("FATAL: Could not connect to the database.")

    # --- Data Insertion Methods ---

    def add_student(self, first_name, last_name, email):
        sql = 'INSERT INTO students(first_name, last_name, email) VALUES(?,?,?)'
        try:
            cur = self.conn.cursor()
            cur.execute(sql, (first_name, last_name, email))
            self.conn.commit()
            print(f"[SUCCESS] Student added. ID: {cur.lastrowid}")
            return cur.lastrowid
        except sqlite3.IntegrityError:
            print(f"[ERROR] Student email '{email}' already exists.")
            return None

    def add_course(self, student_id, name, credit_hours):
        sql = 'INSERT INTO courses(student_id, name, credit_hours) VALUES(?,?,?)'
        try:
            cur = self.conn.cursor()
            cur.execute(sql, (student_id, name, credit_hours))
            self.conn.commit()
            print(f"[SUCCESS] Course '{name}' added. Course ID: {cur.lastrowid}")
            return cur.lastrowid
        except sqlite3.IntegrityError as e:
            if "FOREIGN KEY" in str(e):
                print(f"[ERROR] Student ID {student_id} not found!")
            else:
                print(f"[ERROR] Course '{name}' already exists for student {student_id}.")
            return None

    def add_assignment(self, course_id, name, category, weight, score_num, score_den):
        sql = '''INSERT INTO assignments
                 (course_id, name, category, weight, score_numerator, score_denominator)
                 VALUES(?,?,?,?,?,?)'''
        try:
            cur = self.conn.cursor()
            cur.execute(sql, (course_id, name, category, weight, score_num, score_den))
            self.conn.commit()
            print(f"[SUCCESS] Assignment '{name}' logged.")
            return cur.lastrowid
        except sqlite3.Error as e:
            print(f"[DB ERROR] Could not add assignment: {e}")
            return None

    # --- CSV Memo ---

    def save_memo(self, course_name, memo_text, filename='memos.csv'):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = [timestamp, course_name, memo_text]
        try:
            needs_header = False
            try:
                with open(filename, 'r') as f:
                    if f.read().strip() == '':
                        needs_header = True
            except FileNotFoundError:
                needs_header = True

            with open(filename, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                if needs_header:
                    writer.writerow(['Timestamp', 'Course', 'Memo'])
                writer.writerow(data)

            print(f"[MEMO] Saved note for '{course_name}'.")
            return True
        except IOError as e:
            print(f"[ERROR] Failed to save memo to CSV: {e}")
            return False

    # --- Grade Calculation Logic ---

    def calculate_course_grade(self, course_id):
        """Calculates the current weighted grade for a course."""
        sql = "SELECT weight, score_numerator, score_denominator FROM assignments WHERE course_id = ?"
        cur = self.conn.cursor()
        cur.execute(sql, (course_id,))
        assignments = cur.fetchall()

        if not assignments:
            print("No assignments found for this course ID.")
            return 0.0, 0.0

        total_weighted_points = 0.0
        total_weight_completed = 0.0

        for assign in assignments:
            weight = assign['weight']
            score_num = assign['score_numerator']
            score_den = assign['score_denominator']

            if score_den and score_num is not None:
                # Convert to percentage
                percent_score = (score_num / score_den)
                # Multiply by weight
                weighted_contribution = percent_score * weight
                # Add them up
                total_weighted_points += weighted_contribution
                # Track total weight
                total_weight_completed += weight
            else:
                print(f"(Skipping ungraded item with weight {weight:.1f}.)")

        if total_weight_completed > 0:
            # BUG FIX: was (total_weighted_points / total_weighted_points) → always 100%
            weighted_grade = (total_weighted_points / total_weight_completed) * 100
            return weighted_grade, total_weight_completed
        else:
            print("No graded items completed yet.")
            return 0.0, 0.0
