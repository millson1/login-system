from flask import Flask, render_template, request, redirect, url_for, session
import bcrypt

app = Flask(__name__)

app.secret_key = 'randomsecretkey'

def check_credentials(username, password):
    with open('passwords.txt') as file:
        for line in file:
            stored_username, stored_password_hash = line.strip().split(':')
            if username == stored_username:
                if bcrypt.checkpw(password.encode('utf-8'), stored_password_hash.encode('utf-8')):
                    return True
    return False

def save_user(username, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    with open('passwords.txt', 'a') as file:
        file.write(f"{username}:{hashed_password}\n")

@app.route("/", methods=["GET", "POST"])
def login():
    error_message = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if check_credentials(username, password):
            session['username'] = username
            return redirect(url_for('logged_on'))
        else:
            error_message = "Invalid credentials"

    return render_template("login.html", error_message=error_message)

@app.route("/loggedon")
def logged_on():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    return render_template("loggedon.html", username=session['username'])

@app.route("/logout")
def logged_out():
    session.pop('username', None)
    return render_template("logout.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    error_message = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        invite_code = request.form.get("invite_code")

        if invite_code != "SECRETINVITE10":
            error_message = "Invalid invitation code!"
        else:
            save_user(username, password)
            return redirect(url_for('login'))
    
    return render_template("register.html", error_message=error_message)

if __name__ == "__main__":
    app.run(debug=True)
