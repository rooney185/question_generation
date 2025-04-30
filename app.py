from flask import Flask, render_template, request, send_file, redirect, url_for, session
from werkzeug.utils import secure_filename
from subjective import generate_subjective_questions
from objective import generate_objective_questions
from xhtml2pdf import pisa
from flask_sqlalchemy import SQLAlchemy
import io
import os
import json
import pytesseract
from PIL import Image

# SET TESSERACT PATH
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = Flask(__name__)
app.secret_key = 'your_super_secret_key' 

# Folder to store uploaded images temporarily
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Create database
with app.app_context():
    db.create_all()

# Routes

@app.route('/')
def root():
    return render_template('login.html')

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Check if file was uploaded
    file = request.files.get('image')
    input_text = ""

    if file and file.filename != '':
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Extract text from image using pytesseract
        input_text = pytesseract.image_to_string(Image.open(filepath))

        # Optionally delete file afterwards
        os.remove(filepath)

    else:
        input_text = request.form['text']  # fallback to manual text input

    question_type = request.form['question_type']

    if question_type == "Subjective":
        num_2marks = int(request.form['num_2marks'])
        num_5marks = int(request.form['num_5marks'])
        num_10marks = int(request.form['num_10marks'])
        questions = generate_subjective_questions(input_text, num_2marks, num_5marks, num_10marks)
    else:  # Objective
        num_questions = int(request.form['num_questions'])
        questions = generate_objective_questions(input_text, num_questions)
        for q in questions:
            if 'answer' not in q:
                q['answer'] = None

    questions = sorted(questions, key=lambda x: x['marks'])
    return render_template('result.html', questions=questions)

@app.route('/download-pdf', methods=['POST'])
def download_pdf():
    questions_json = request.form['questions']
    questions = json.loads(questions_json)

    html = render_template('pdf_template.html', questions=questions)
    pdf = io.BytesIO()
    pisa_status = pisa.CreatePDF(src=html, dest=pdf)

    if not pisa_status.err:
        pdf.seek(0)
        return send_file(pdf, as_attachment=True, download_name="questions.pdf", mimetype='application/pdf')
    else:
        return "Error generating PDF"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            return "Username or email already exists. Try again."

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return "Invalid credentials. Try again."

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)