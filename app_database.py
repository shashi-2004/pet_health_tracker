from flask import Flask, request, render_template, jsonify, redirect, url_for, session
from flask_cors import CORS
from flask_bcrypt import Bcrypt
import sqlite3
import logging

# Logging setup
logging.basicConfig(level=logging.DEBUG)

# Flask app setup
app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = "your_secret_key_here"  # Change this to a secure key
CORS(app)
bcrypt = Bcrypt(app)

# Database setup function
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS pets (pet_id INTEGER PRIMARY KEY, name TEXT, age INTEGER, breed TEXT, medical_history TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS pet_activities (activity_id INTEGER PRIMARY KEY, pet_id INTEGER, steps INTEGER, food TEXT, calories INTEGER, problem TEXT, suggestion TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS vaccination_records (vaccination_id INTEGER PRIMARY KEY, pet_id INTEGER, vaccination_type TEXT, vaccination_date TEXT)''')
    conn.commit()
    conn.close()

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.form
        username = data['username']
        password = data['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        try:
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            conn.close()
            return jsonify({"message": "Signup successful! Please login."})
        except sqlite3.IntegrityError:
            return jsonify({"error": "Username already exists!"})
    return render_template("signup.html")

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        username = data['username']
        password = data['password']
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        conn.close()
        if user and bcrypt.check_password_hash(user[2], password):
            session['username'] = username
            return jsonify({"message": "Login successful!", "redirect": url_for('dashboard')})
        return jsonify({"error": "Invalid username or password"})
    return render_template("login.html")

# Home route
@app.route('/')
def home():
    return redirect(url_for('login'))

# Dashboard route (Fixed Here)
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template("dashboard.html", username=session['username'])  # Changed 'политика_template' to 'render_template'

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# Add pet route
@app.route('/add_pet', methods=['POST'])
def add_pet():
    if 'username' not in session:
        return jsonify({"error": "Please login to add a pet"}), 401
    data = request.form
    name = data['name']
    age = int(data['age'])
    breed = data['breed']
    medical_history = data['medical_history']
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO pets (name, age, breed, medical_history) VALUES (?, ?, ?, ?)",
              (name, age, breed, medical_history))
    conn.commit()
    pet_id = c.lastrowid
    conn.close()
    return jsonify({"message": "Pet added successfully!", "pet_id": pet_id})

# Save steps route
@app.route('/save_steps', methods=['POST'])
def save_steps():
    if 'username' not in session:
        return jsonify({"error": "Please login to save steps"}), 401
    data = request.form
    pet_id = data['pet_id']
    steps = int(data['steps'])
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO pet_activities (pet_id, steps) VALUES (?, ?)", (pet_id, steps))
    conn.commit()
    conn.close()
    return jsonify({"message": "Steps saved successfully!"})

# Save food route
@app.route('/save_food', methods=['POST'])
def save_food():
    if 'username' not in session:
        return jsonify({"error": "Please login to save food"}), 401
    data = request.form
    pet_id = data['pet_id']
    food = data['food']
    calories = int(data['calories'])
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO pet_activities (pet_id, food, calories) VALUES (?, ?, ?)",
              (pet_id, food, calories))
    conn.commit()
    conn.close()
    return jsonify({"message": "Food and calories saved successfully!"})

# Save medical route
@app.route('/save_medical', methods=['POST'])
def save_medical():
    if 'username' not in session:
        return jsonify({"error": "Please login to save medical data"}), 401
    data = request.form
    pet_id = data['pet_id']
    problem = data['problem']
    suggestion = data['suggestion']
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO pet_activities (pet_id, problem, suggestion) VALUES (?, ?, ?)",
              (pet_id, problem, suggestion))
    conn.commit()
    conn.close()
    return jsonify({"message": "Medical data saved successfully!"})

# Save vaccination route
@app.route('/save_vaccination', methods=['POST'])
def save_vaccination():
    if 'username' not in session:
        return jsonify({"error": "Please login to save vaccination data"}), 401
    data = request.form
    pet_id = data['pet_id']
    vaccination_type = data['vaccination_type']
    vaccination_date = data['vaccination_date']
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO vaccination_records (pet_id, vaccination_type, vaccination_date) VALUES (?, ?, ?)",
              (pet_id, vaccination_type, vaccination_date))
    conn.commit()
    conn.close()
    return jsonify({"message": "Vaccination record saved successfully!"})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
