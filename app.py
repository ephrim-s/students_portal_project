import os
import sqlite3
import uuid
from flask import Flask, flash, jsonify, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'student-portal-secret'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
DB_PATH = os.path.join(BASE_DIR, 'students_portal.db')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            address TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            date_of_birth TEXT NOT NULL,
            gender TEXT NOT NULL,
            country TEXT NOT NULL,
            course TEXT NOT NULL,
            image_name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


init_db()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        required_fields = [
            'first_name',
            'last_name',
            'address',
            'email',
            'phone',
            'date_of_birth',
            'gender',
            'country',
            'course',
        ]

        missing_fields = [field for field in required_fields if not request.form.get(field, '').strip()]
        if missing_fields:
            flash('Please fill in all required fields.', 'error')
            return render_template('registrationForm.html')

        image = request.files.get('image')
        if not image or image.filename == '':
            flash('Please upload an image.', 'error')
            return render_template('registrationForm.html')

        filename = secure_filename(image.filename)
        if '.' not in filename or filename.rsplit('.', 1)[1].lower() not in ALLOWED_EXTENSIONS:
            flash('Please upload a valid image file.', 'error')
            return render_template('registrationForm.html')

        name, ext = os.path.splitext(filename)
        unique_name = f'{name}_{uuid.uuid4().hex}{ext}'
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)

        try:
            image.save(image_path)
            conn = sqlite3.connect(DB_PATH)
            conn.execute(
                '''
                INSERT INTO students (
                    first_name, last_name, address, email, phone, date_of_birth,
                    gender, country, course, image_name
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''',
                (
                    request.form.get('first_name').strip(),
                    request.form.get('last_name').strip(),
                    request.form.get('address').strip(),
                    request.form.get('email').strip(),
                    request.form.get('phone').strip(),
                    request.form.get('date_of_birth').strip(),
                    request.form.get('gender').strip(),
                    request.form.get('country').strip(),
                    request.form.get('course').strip(),
                    unique_name,
                ),
            )
            conn.commit()
            conn.close()
            return redirect(url_for('success'))
        except Exception:
            if os.path.exists(image_path):
                os.remove(image_path)
            flash('Unable to save your details. Please try again.', 'error')
            return render_template('registrationForm.html')

    return render_template('registrationForm.html')


@app.route('/success')
def success():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    students = conn.execute(
        'SELECT id, first_name, last_name, email, phone, course, country FROM students ORDER BY id DESC'
    ).fetchall()
    conn.close()
    return render_template('success.html', students=students)


@app.route('/student/<int:student_id>')
def student_detail(student_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    student = conn.execute(
        'SELECT * FROM students WHERE id = ?', (student_id,)
    ).fetchone()
    conn.close()
    if not student:
        flash('Student not found.', 'error')
        return redirect(url_for('success'))
    return render_template('student_detail.html', student=dict(student))


@app.route('/api/options')
def api_options():
    return jsonify({
        'countries': ['Kenya', 'Uganda', 'Tanzania', 'Rwanda', 'Ethiopia'],
        'courses': ['Web Development', 'Data Science', 'Mobile Development', 'UI/UX Design', 'Cybersecurity']
    })


if __name__ == '__main__':
    app.run(debug=True)