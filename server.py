from flask_app.controllers import users, recipes
from flask_app import app
from flask import Flask

if __name__ == "__main__":
    app.run(debug=True)