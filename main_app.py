# main_app.py - The Grade Manager App Runner
# Run this file to start the application!

from database_setup import DatabaseManager
from grade_function import GradeTracker


def main():
    print("\n\n*** Welcome to the Grade Tracker v2.0! ***")

    db_manager = DatabaseManager()

    try:
        app_tracker = GradeTracker(db_manager)
    except ConnectionError as e:
        print(e)
        return

    while True:
        print("\n--- MENU ---")
        print("1. Add New Student (Get Student ID)")
        print("2. Add New Course (Needs Student ID)")
        print("3. Add Assignment/Score (Needs Course ID)")
        print("4. Check Course Grade Report")
        print("5. Save Course Memo (Note)")
        print("6. Exit")

        choice = input("Select an option (1-6): ")

        try:
            if choice == '1':
                first = input("Student First Name: ")
                last = input("Student Last Name: ")
                email = input("Student Email (unique): ")
                app_tracker.add_student(first, last, email)

            elif choice == '2':
                student_id = int(input("Enter Student ID: "))
                name = input("Course Name: ")
                credits = float(input("Credit Hours (e.g., 3.0): "))
                app_tracker.add_course(student_id, name, credits)

            elif choice == '3':
                course_id = int(input("Enter Course ID: "))
                name = input("Assignment Name: ")
                category = input("Category (Quiz/Exam/Project): ")
                weight = float(input("Weight % (e.g., 20.0): "))
                score_den = float(input("Max Score: "))
                score_num_input = input("Your Score (Leave blank if ungraded): ")

                score_num = None
                if score_num_input.strip() != "":
                    score_num = float(score_num_input)

                app_tracker.add_assignment(course_id, name, category, weight, score_num, score_den)

            elif choice == '4':
                course_id = int(input("Enter Course ID to check: "))
                grade, weight_done = app_tracker.calculate_course_grade(course_id)

                if weight_done > 0.0:
                    print("\n--- CURRENT GRADE REPORT ---")
                    print(f"Course ID {course_id}: Current Grade = {grade:.2f}%")
                    print(f"Weight Graded So Far: {weight_done:.1f}%")

            elif choice == '5':
                course_name = input("Course Name for Memo: ")
                memo_text = input("Your Note/Memo: ")
                app_tracker.save_memo(course_name, memo_text)

            elif choice == '6':
                print("Exiting app. Thanks for grading!")
                break

            else:
                print("Invalid choice. Try again!")

        except ValueError:
            print("[INPUT ERROR] Please make sure you enter numbers for IDs, scores, and weights.")
        except Exception as e:
            print(f"[UNKNOWN ERROR] Something unexpected happened: {e}")

    db_manager.close()


if __name__ == '__main__':
    main()
