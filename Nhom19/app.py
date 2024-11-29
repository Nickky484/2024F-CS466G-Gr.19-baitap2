import bcrypt
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from csdl import create_data
app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_db_connection():
        b = sqlite3.connect('lst.db')
        b.row_factory = sqlite3.Row
        return b
def add_user(username, password, email, role):
    # Mã hóa mật khẩu trước khi lưu vào cơ sở dữ liệu
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    tu = get_db_connection()
    tu.execute('''
        INSERT INTO person (username, password, email,role)
        VALUES (?, ?, ?,?)
    ''', (username, hashed_password, email,role))
    tu.commit()
    tu.close()
@app.route('/', methods=['GET', 'POST'])
def signup():
    create_data()
    if request.method == 'POST':
        username = request.form['username1']
        password = request.form['password1']
        email = request.form['email']
        role = "admin"
        if username and email and password:
            add_user(username, password, email,role)
            return redirect(url_for('login'))
        else:
            flash('Invalid', 'danger')
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username2']
        password = request.form['password2']

        # Kiểm tra thông tin đăng nhập bằng database cho các tài khoản khác
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM person WHERE username = ? ', (username,)).fetchone()
        conn.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html')
@app.route('/dashboard')
def dashboard():
   return render_template('user.html')
if __name__ == '__main__':
    app.run(debug=True)