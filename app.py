from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Simulated user data (hardcoded)
users = {
    "admin": "password123",
    "user1": "mypassword"
}

# Hardcoded user profile data
user_profiles = {
    "admin": {
        "first_name": "Admin",
        "last_name": "User",
        "email": "admin@example.com",
        "address": "123 Admin St"
    },
    "user1": {
        "first_name": "User1",
        "last_name": "Test",
        "email": "user1@example.com",
        "address": "456 User1 St"
    }
}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Retrieve username and password from the form
        username = request.form['username']
        password = request.form['password']
        
        # Check if the username exists and the password matches
        if username in users and users[username] == password:
            return redirect(url_for('index', username=username))
        else:
            # If the credentials don't match
            return render_template('login.html', error="Invalid username or password")
    
    # GET request, display the login form
    return render_template('login.html')


@app.route('/index/<username>')
def index(username):
    return render_template('index.html', username=username)


@app.route('/display/<username>')
def display(username):
    if username in user_profiles:
        user_profile = user_profiles[username]
        return render_template('display.html', username=username,
                               first_name=user_profile['first_name'],
                               last_name=user_profile['last_name'],
                               email=user_profile['email'],
                               address=user_profile['address'])
    else:
        return redirect(url_for('login'))  # Redirect if user not found


@app.route('/logout')
def logout():
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
