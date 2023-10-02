from flask import Flask, render_template, request, url_for, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/face_recognization2'
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a strong secret key
db = SQLAlchemy(app)

# Register_page class
class Register3page(db.Model):
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), primary_key=True, nullable=False) 
    password = db.Column(db.String(20), nullable=True)
    con_password = db.Column(db.String(20), nullable=True)


# student_page class
class Student(db.Model):
    sno = db.Column(db.Integer, primary_key=True, nullable=False)
    S_first_name = db.Column(db.String(20), nullable=False)
    S_last_name = db.Column(db.String(20), nullable=False)
    S_Gr_No = db.Column(db.String(20), nullable=False)
    S_email_id = db.Column(db.String(20), nullable=False)
    S_branch = db.Column(db.String(20), nullable=False)
    S_class = db.Column(db.String(20))
    S_div = db.Column(db.String(20)) 
    S_roll_no = db.Column(db.String(20), nullable=False)
    S_date = db.Column(db.DateTime, default=datetime.utcnow)
 
@app.route("/new-user.html", methods=['GET', 'POST'])
def register3_page():
    if request.method == 'POST':
        # Add entry to the database
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        con_password = request.form.get('con_password')
   
        if password == con_password:
            entry = Register3page(first_name=first_name, last_name=last_name, email=email, password=password,
                                 con_password=con_password)
            db.session.add(entry)
            db.session.commit()
            
    return render_template('new-user.html')

@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = Register3page.query.filter_by(email=email).first()
        
        if user and user.password == password:
            # Successful login
            session['user_email'] = user.email  # Store user email in the session
            return redirect(url_for('home'))
        else:
            # Invalid credentials
            return redirect(url_for('index'))

    return render_template('index.html')

@app.route("/home")
def home():
    if 'user_email' not in session:
        return redirect(url_for('index'))
    
    return render_template('home.html')

@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/student", methods=['GET', 'POST'])
def student():
    if request.method == 'POST':
        S_first_name = request.form.get('S_first_name')
        S_last_name = request.form.get('S_last_name')
        S_Gr_No = request.form.get('S_Gr_No')
        S_email_id = request.form.get('S_email_id')
        S_branch = request.form.get('S_branch')
        S_class = request.form.get('S_class')
        S_div = request.form.get('S_div')
        S_roll_no = request.form.get('S_roll_no')

        entry = Student(
            S_first_name=S_first_name,
            S_last_name=S_last_name,
            S_Gr_No=S_Gr_No,
            S_email_id=S_email_id,
            S_branch=S_branch,
            S_class=S_class,
            S_div=S_div,
            S_roll_no=S_roll_no
        )

        db.session.add(entry)
        db.session.commit()

    # Query all entries after the data has been added to the database
    all_entries = Student.query.all()
    
    return render_template('student.html', all_entries=all_entries)


@app.route("/teacher")
def teacher():
    return render_template('teacher.html')

@app.route("/attendance")
def attendance():
    return render_template('attendance.html')

@app.route("/analysis")
def analysis():
    return render_template('analysis.html')



if __name__ == "__main__":
    app.run(debug=True)
