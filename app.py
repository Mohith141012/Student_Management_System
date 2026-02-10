# Top-level imports and app config
from flask import Flask, render_template, request, redirect, url_for, session, Response
from functools import wraps
import mysql.connector as mysql
import csv
from io import StringIO
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date

app = Flask(__name__)

# Session secret key
app.secret_key = "user_key"

# Session cookie security settings (place here, near top with other config)
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
# Optional: enable only if you serve over HTTPS
# app.config['SESSION_COOKIE_SECURE'] = True


# -----------------------------
# Helper functions / decorators
# -----------------------------

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def roles_required(*roles):
    """
    Usage:
        @roles_required('Admin')
        @roles_required('Admin', 'Staff')
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('login'))
            if 'role' not in session or session['role'] not in roles:
                return "Access denied: insufficient permissions", 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# Helper for age calculation (used by CSV export)
def compute_age(dob):
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))


def calculate_marks_info(subject1, subject2, subject3):
    if subject1 is None or subject2 is None or subject3 is None:
        return None
    total = subject1 + subject2 + subject3
    percentage = round(total / 3, 2)
    if percentage >= 90:
        grade = "A+"
    elif percentage >= 75:
        grade = "A"
    elif percentage >= 60:
        grade = "B"
    elif percentage >= 50:
        grade = "C"
    else:
        grade = "Fail"
    result = "Pass" if percentage >= 50 else "Fail"
    return {
        "subject1": subject1,
        "subject2": subject2,
        "subject3": subject3,
        "total": total,
        "percentage": percentage,
        "grade": grade,
        "result": result,
    }


# Creating the connection to mysql database
con = mysql.connect(host="localhost", user="root", password="123456789", database="sms")

# Creating cursor to execute sql queries
cur = con.cursor()


# Home page
@app.route('/')
def home():
    return render_template('home.html')


# About page
@app.route('/about')
def about():
    return render_template('about.html')


# Contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')


# Data page
@app.route('/data')
@roles_required('Admin', 'Staff')
def data():
    cur.execute("select * from students")
    result = cur.fetchall()
    return render_template('data.html', students=result)


# Signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        location = request.form['location']
        mobileno = request.form['mobileno']
        zipcode = request.form['zipcode']
        role = request.form.get('role', 'Student').strip()
        if role not in ('Admin', 'Staff', 'Student'):
            role = 'Student'

        # Check if email already exists in users table
        cur.execute("select id from users where email=%s", (email,))
        existing_user = cur.fetchone()
        if existing_user:
            return "Email already registered. Please login or use a different email.", 400

        hashed_password = generate_password_hash(password)
        query = """insert into users(firstname,lastname,email,password,location,mobileno,zipcode,role)
                   values (%s,%s,%s,%s,%s,%s,%s,%s)"""
        values = (firstname, lastname, email, hashed_password, location, mobileno, zipcode, role)
        cur.execute(query, values)
        con.commit()

        # If role is Student, create a basic student record (only if it doesn't exist)
        if role == 'Student':
            # Check if student record already exists with this email
            cur.execute("select id from students where email=%s", (email,))
            existing_student = cur.fetchone()

            if not existing_student:
                # Student record doesn't exist, create one
                # Get additional student info from form (you'll need to add these fields to signup.html)
                phone = request.form.get('phone', mobileno)  # Use mobile number as phone
                dob = request.form.get('dob', '2000-01-01')  # Default or from form
                gender = request.form.get('gender', 'Other')  # From form
                course = request.form.get('course', 'Not Assigned')  # From form
                year = request.form.get('year', 1)  # From form
                roll_number = request.form.get('roll_number', f'STU{cur.lastrowid}')  # Auto-generate or from form
                city = location  # Use location as city

                student_query = """insert into students(first_name, last_name, email, phone, date_of_birth,
                                  gender, course, year, roll_number, city)
                                  values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                student_values = (firstname, lastname, email, phone, dob, gender, course, year, roll_number, city)
                cur.execute(student_query, student_values)
                con.commit()
            # If student record exists, it will be linked automatically by email

        return redirect(url_for('login'))
    return render_template('signup.html')


# Update student page
@app.route('/update/<id>', methods=['GET', 'POST'])
@roles_required('Admin')
def update(id):
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        phone = request.form['phone']
        dob = request.form['dob']
        gender = request.form['gender']
        course = request.form['course']
        year = request.form['year']
        roll_number = request.form['roll_number']
        city = request.form['city']
        query = """update students set first_name=%s, last_name=%s, email=%s, phone=%s,
                   date_of_birth=%s, gender=%s, course=%s, year=%s, roll_number=%s, city=%s
                   where id=%s"""
        values = (firstname, lastname, email, phone, dob, gender, course, year, roll_number, city, id)
        cur.execute(query, values)
        con.commit()
        return redirect(url_for('data'))
    cur.execute("select * from students where id=%s", (id,))
    result = cur.fetchone()
    return render_template('update.html', data=result)


# Delete student
@app.route('/delete/<id>', methods=['POST'])
@roles_required('Admin')
def delete(id):
    query = "delete from students where id=%s"
    cur.execute(query, (id,))
    con.commit()
    return redirect('/data')


# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        query = "select id, firstname, lastname, email, password, role from users where email=%s"
        cur.execute(query, (email,))
        result = cur.fetchone()
        if result and check_password_hash(result[4], password):
            session['user_id'] = result[0]
            session['firstname'] = result[1]
            session['lastname'] = result[2]
            session['email'] = result[3]
            session['role'] = result[5]
            session.permanent = True
            return redirect(url_for('home'))
        else:
            return "Invalid username or password"
    return render_template('login.html')


# Dashboard page
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=session['firstname'], role=session.get('role'))


# Student profile page - only for logged-in students, shows their own record
@app.route('/student/profile')
@roles_required('Student')
def student_profile():
    user_email = session.get('email')
    user_id = session.get('user_id')

    # Debug: Check what email we're looking for
    print(f"Looking for student with email: {user_email}")

    cur.execute("select * from students where email=%s", (user_email,))
    student = cur.fetchone()

    if not student:
        # Student record doesn't exist - show helpful message
        error_msg = f"""
        <h2>Profile Not Found</h2>
        <p>No student profile found for email: <strong>{user_email}</strong></p>
        <p>This could happen if:</p>
        <ul>
            <li>You signed up before the student profile feature was added</li>
            <li>Your account needs to be linked to a student record by an administrator</li>
        </ul>
        <p><a href="{url_for('dashboard')}">Back to Dashboard</a></p>
        """
        return error_msg, 404

    # Fetch marks for the student
    cur.execute("select subject1, subject2, subject3 from student_marks where student_id=%s", (student[0],))
    marks = cur.fetchone()

    marks_info = None
    if marks:
        marks_info = calculate_marks_info(marks[0], marks[1], marks[2])

    return render_template('student_profile.html', student=student, marks_info=marks_info)


# Admin/Staff full-profile view used by data.html
@app.route('/student/<int:id>')
@roles_required('Admin', 'Staff')
def view_student(id):
    cur.execute("select * from students where id=%s", (id,))
    student = cur.fetchone()
    if not student:
        return "Student not found", 404

    cur.execute("select subject1, subject2, subject3 from student_marks where student_id=%s", (id,))
    marks = cur.fetchone()

    marks_info = None
    if marks:
        marks_info = calculate_marks_info(marks[0], marks[1], marks[2])

    return render_template('student_profile.html', student=student, marks_info=marks_info)


# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# Export students as CSV (Admin only)
@app.route('/export/students', methods=['GET'])
@roles_required('Admin')
def export_students():
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Name', 'Age', 'Course', 'Email'])
    cur.execute("select first_name, last_name, date_of_birth, course, email from students")
    for first_name, last_name, dob, course, email in cur.fetchall():
        age = compute_age(dob)
        writer.writerow([f"{first_name} {last_name}", age, course, email])
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=students.csv'}
    )


# Users management page (Admin only)
@app.route('/users', methods=['GET'])
@roles_required('Admin')
def users():
    cur.execute("select id, firstname, lastname, email, role from users")
    users = cur.fetchall()
    return render_template('users.html', users=users)


# Delete user (Admin only)
@app.route('/users/delete/<id>', methods=['POST'])
@roles_required('Admin')
def delete_user(id):
    cur.execute("delete from users where id=%s", (id,))
    con.commit()
    return redirect(url_for('users'))


# Debug route - check database records (remove in production)
@app.route('/debug/check-student')
@login_required
def debug_check_student():
    user_email = session.get('email')

    # Check users table
    cur.execute("select id, firstname, lastname, email, role from users where email=%s", (user_email,))
    user_record = cur.fetchone()

    # Check students table
    cur.execute("select id, first_name, last_name, email, course from students where email=%s", (user_email,))
    student_record = cur.fetchone()

    # Get all students (for debugging)
    cur.execute("select id, email from students")
    all_students = cur.fetchall()

    output = f"""
    <h2>Database Check for: {user_email}</h2>

    <h3>User Record (users table):</h3>
    <pre>{user_record}</pre>

    <h3>Student Record (students table):</h3>
    <pre>{student_record}</pre>

    <h3>All Student Emails in Database:</h3>
    <ul>
    """
    for student in all_students:
        output += f"<li>ID: {student[0]} - Email: {student[1]}</li>"

    output += """
    </ul>
    <p><a href="/dashboard">Back to Dashboard</a></p>
    """

    return output


if __name__ == "__main__":
    app.run(debug=True)