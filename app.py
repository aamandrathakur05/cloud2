from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    """Initialize the database and create the users table if not exists."""
    with sqlite3.connect('users.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                      username TEXT UNIQUE, 
                      password TEXT, 
                      firstname TEXT, 
                      lastname TEXT, 
                      email TEXT, 
                      address TEXT)''')
        conn.commit()

# Initialize the database
init_db()

@app.route('/')
def index():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    firstname = request.form['first_name']
    lastname = request.form['last_name']
    email = request.form['email']
    address = request.form['address']
    
    try:
        with sqlite3.connect('users.db') as conn:
            c = conn.cursor()
            c.execute("""
                INSERT INTO users (username, password, firstname, lastname, email, address) 
                VALUES (?, ?, ?, ?, ?, ?)
            """, (username, password, firstname, lastname, email, address))
            conn.commit()
    except sqlite3.IntegrityError:
        return "Username already exists!"  # Handle duplicate username error
    
    return redirect(url_for('profile', username=username))

@app.route('/profile/<username>')
def profile(username):
    with sqlite3.connect('users.db') as conn:
        c = conn.cursor()
        c.execute("SELECT username, firstname, lastname, email, address FROM users WHERE username=?", (username,))
        user = c.fetchone()
    
    if user:
        return render_template('profile.html', user=user)
    else:
        return "User not found!", 404

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        with sqlite3.connect('users.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            user = c.fetchone()
        
        if user:
            return redirect(url_for('profile', username=username))
        else:
            return "Invalid credentials, please try again."
    
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
