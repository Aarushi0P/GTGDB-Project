from flask import Flask, render_template, request, session, redirect
import db
import time

app = Flask(__name__)
app.secret_key = "gtg"

# Rate limiting for login attempts
failed_attempts = {}  # username: {'count': int, 'last_attempt': timestamp}

@app.route("/")
def Home():
    guessData = db.GetAllGuesses()
    return render_template("index.html", guesses=guessData)

@app.route("/login", methods=["GET", "POST"])
def Login():

    if session.get('username') is not None:
        return redirect("/")

    # They sent us data, get the username and password
    # then check if their details are correct.
    if request.method == "POST":
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        current_time = time.time()

        # Check rate limiting
        if username in failed_attempts:
            attempts = failed_attempts[username]
            if attempts['count'] >= 5 and current_time - attempts['last_attempt'] < 300:  # 5 failed attempts, 5 min lockout
                return render_template("login.html")  # Silently deny, or could add error message

        # Did they provide good details
        user = db.CheckLogin(username, password)
        if user:
            # Yes! Save their username then
            session['username'] = user['username']
            session['id'] = user['id']

            # Reset failed attempts on successful login
            failed_attempts[username] = {'count': 0, 'last_attempt': current_time}

            # Send them back to the homepage
            return redirect("/")
        else:
            # Failed login, increment attempts
            if username not in failed_attempts:
                failed_attempts[username] = {'count': 1, 'last_attempt': current_time}
            else:
                failed_attempts[username]['count'] += 1
                failed_attempts[username]['last_attempt'] = current_time

    return render_template("login.html")

@app.route("/logout")
def Logout():
    session.clear()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def Register():

    if session.get('username') is not None:
        return redirect("/")

    # If they click the submit button, let's register
    if request.method == "POST":
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        # Try and add them to the DB
        if db.RegisterUser(username, password):
            # Success! Let's go to the homepage
            return redirect("/")
        
    return render_template("register.html")

##################################
### New code starts here
##################################
@app.route("/add", methods=["GET","POST"])
def Add():

    # Check if they are logged in first
    if session.get('username') == None:
        return redirect("/")

    # Did they click submit?
    if request.method == "POST":
        user_id = session['id']
        date = request.form['date'].strip()
        game = request.form['game'].strip()
        score = request.form['score'].strip()

        # Send the data to add our new guess to the db
        if db.AddGuess(user_id, date, game, score):
            return redirect("/")
        # If validation failed, fall through to render template again

    return render_template("add.html")

##################################
### New code ends here
##################################

app.run(debug=True, port=5000)
