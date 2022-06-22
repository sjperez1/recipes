from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def display_login_registration():
    # If I put if validate_user_session() == True: return redirect("/dashboard"), this causes the flash to show up on the first page as well. So, do if "id" in session.
    if "id" in session:
        return redirect("/dashboard")
    else:
        return render_template("login_registration.html")

@app.route("/register", methods = ['POST'])
def register_user():
    if User.validate_user_registration(request.form) == False:
        return redirect("/")
    else:
        # The following is saying if there is no matching email stored in the database, then create it. The else statement will say that there already is one and you need to use a different one.
        if User.get_one_user_email({"email" : request.form['email']}) == None:
            data = {
                "first_name" : request.form['first_name'],
                "last_name" : request.form['last_name'],
                "email" : request.form['email'],
                "password" : bcrypt.generate_password_hash(request.form['password']),
                "confirm_password" : request.form['confirm_password']
            }
            user_id = User.create_user(data)
            # result is one instance of a user. Look at the function to understand this better.
            session['first_name'] =  request.form['first_name']
            session['last_name'] = request.form['last_name']
            session['email'] = request.form['email']
            # Needed to add the session id part here so that def get_user_by_id can get the user id
            session['user_id'] = user_id
            return redirect("/dashboard")
        else:
            flash("This email is already in use. Use a different email to register or log in.", "error_email_registration")
            return redirect("/")

@app.route("/login", methods = ['POST'])
def login_user():
    login_info = User.get_one_user_email(request.form)
    if request.form['email'] == "" and request.form['password'] == "":
        flash("Your email and password is required for login.", "error_login_user")
        return redirect("/")
    if request.form['email'] == "":
        flash("Your email is required for login.", "error_login_user")
        return redirect("/")
    if request.form['password'] == "":
        flash("Your password is required for login.", "error_login_user")
        return redirect("/")
    elif login_info == None:
        flash("This email does not belong to an existing user. Try again.", "error_login_user")
        return redirect("/")
    else:
        if not bcrypt.check_password_hash(login_info.password, request.form['password']):
            flash("This password does not belong to an existing user. Try again.", "error_login_user")
            return redirect("/")
        else:
            # login_info is one instance of a user that has an email matching what they typed in, as seen with the User.get_one_user_email() function. This else is saying that if the login occurs properly, add the user's info into session
            session['first_name'] = login_info.first_name
            session['last_name'] = login_info.last_name
            session['email'] = login_info.email
            # Needed to add the session id part here so that def get_one_user_email can get the user id
            session['user_id'] = login_info.id
            return redirect("/dashboard")


@app.route("/dashboard")
def display_dashboard():
    if User.validate_user_session("user_id"):
        return render_template("dashboard.html", recipes = Recipe.get_all_recipes())
    else:
        return redirect ("/")

@app.route("/logout", methods = ['POST'])
def logout():
    session.clear()
    return redirect ("/")