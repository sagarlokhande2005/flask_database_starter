"""
Part 1: Basic Flask with SQLite Database
=========================================
Your first step into databases! Moving from hardcoded lists to real database.
"""

from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

DATABASE = 'students.db'


# =============================================================================
# DATABASE HELPER FUNCTIONS
# =============================================================================

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            course TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


# =============================================================================
# ROUTES
# =============================================================================

@app.route('/')
def index():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return render_template('index.html', students=students)


@app.route('/add')
def add_sample_student():
    conn = get_db_connection()

    # Insert multiple students correctly
    conn.executemany(
        'INSERT INTO students (name, email, course) VALUES (?, ?, ?)',
        [
            ('John Doe', 'john@example.com', 'Python'),
            ('Sagar Lokhande', 'sagarlo123@gmail.com', 'Java'),('amol','amol123@gmail.com','python')
        ]
    )

    conn.commit()
    conn.close()

    return 'Students added successfully! <a href="/">Go back to home</a>'



@app.route('/delete/<int:id>')
def delete_student(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM students WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')  # Go back to home page


# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':
    init_db()
    app.run(debug=True)