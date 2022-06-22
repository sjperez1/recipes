from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe

@app.route("/recipes/<int:id>")
def view_instructions(id):
    if User.validate_user_session("user_id") == True:
        data = {
            "id" : id
        }
        return render_template("view_recipe.html", one_recipe = Recipe.get_recipe(data))
    else:
        return redirect("/")

@app.route("/recipes/delete/<int:id>")
def delete_user(id):
    data = {
        "id" : id
    }
    Recipe.delete_recipe(data)
    return redirect("/dashboard")

@app.route("/recipes/new")
def display_create_recipe():
    if User.validate_user_session("user_id"):
        return render_template("new_recipe.html")
    else:
        return redirect("/")

@app.route("/recipes/new", methods = ['POST'])
def create_recipe():
    # cannot do request.form here because the user_id needs to be included to attach the recipe to a user and this is in session, not the form.
    data = {
        "name" : request.form['name'],
        "description" : request.form['description'],
        "instructions" : request.form['instructions'],
        "under_30_minutes" : request.form['under_30_minutes'],
        "created_at" : request.form['created_at'],
        "user_id" : session['user_id']
    }
    if Recipe.validate_new_recipe(request.form) == False:
        return redirect("/recipes/new")
    else:
        Recipe.create(data)
        return redirect("/dashboard")

@app.route("/recipes/edit/<int:id>")
def display_edit_recipes(id):
    if User.validate_user_session("user_id"):
        data = {
            "id" : id
        }
        return render_template("edit_recipe.html", one_recipe = Recipe.get_recipe(data))
    else:
        return redirect("/")

@app.route("/recipes/edit/<int:id>", methods = ['POST'])
def update_recipe(id):
    # must add created at here because it defaults to when it was entered, but they can change the date to be another day that they made this recipe.
    # cannot just do request.form because the user_id is coming from the session and the id is going url into the query.
    data = {
        "id" : id,
        "name" : request.form['name'],
        "description" : request.form['description'],
        "instructions" : request.form['instructions'],
        "under_30_minutes" : request.form['under_30_minutes'],
        "created_at" : request.form['created_at'],
        "user_id" : session['user_id']
    }
    Recipe.update_recipe(data)
    return redirect("/dashboard")

