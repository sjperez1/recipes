from flask import Flask
app = Flask(__name__)

app.secret_key = "shhhh"

# The following allows easy changing of database name throughout our files
DATABASE = 'recipes_schema'