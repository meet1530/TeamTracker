from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3, os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DATABASE = 'data/teamtrackr.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    if 'user' in session:
        return render_template('dashboard.html')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pw = request.form['password']
        if user == 'admin' and pw == 'admin123':  # Simple login, replace with DB check
            session['user'] = user
            return redirect(url_for('index'))
        return render_template('login.html', error='Invalid Credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        with sqlite3.connect(DATABASE) as db:
            db.execute("CREATE TABLE IF NOT EXISTS members (id INTEGER PRIMARY KEY, name TEXT, role TEXT, department TEXT, joined TEXT)")
            db.execute("CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY, name TEXT, date TEXT)")
            db.execute("CREATE TABLE IF NOT EXISTS attendance (id INTEGER PRIMARY KEY, member_id INTEGER, event_id INTEGER, status TEXT)")
            db.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, title TEXT, description TEXT, team TEXT, member TEXT, date TEXT)")
    app.run(debug=True)
