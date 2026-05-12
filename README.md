# 📚 Grade Tracker v2.0

A command-line grade tracking application built with Python and SQLite.

## 🚀 Features
- Add students, courses, and assignments
- Calculate weighted course grades automatically
- Save course memos/notes to CSV
- SQLite database for persistent storage

## 🛠️ Tech Stack
- Python 3
- SQLite3
- CSV

## ⚙️ Setup

```bash
# Clone the repo
git clone https://github.com/KAUNGMYATPAINGTHAR-dev/grade-tracker.git
cd grade-tracker

# Run the app
python main_app.py
```

## 📋 Menu Options

| Option | Description |
|--------|-------------|
| 1 | Add a new student |
| 2 | Add a new course |
| 3 | Add assignment/score |
| 4 | Check grade report |
| 5 | Save a course memo |
| 6 | Exit |

## 🐛 Bug Fixes
- Fixed grade calculation always returning 100% (division error)
- Fixed typo: "parcentage" → "percentage"
- Added missing `database_setup.py`

## 📝 License
MIT
