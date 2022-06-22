from flask_app import DATABASE
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.recipe import Recipe
from flask import flash, session
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_one_user_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)

        if len(result) > 0:
            return cls(result[0])
        else:
            return None
    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users(first_name, last_name, email, password) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_all_recipes(cls, data):
        query = "SELECT * FROM users JOIN recipes ON users.id = recipes.user_id WHERE users.id = %(id)s;"

        result = connectToMySQL(DATABASE).query_db(query, data)
        # print to visualize what steps need to be taken next to make an instance of a user and create instances of recipes in the user.
        # print(result)

        if result:
            # we are making an instance of a user. Bc it is an object, we can add an attribute and the list will be an attribute.
            one_user = cls(result[0])
            print(result[0])
            recipes_list = []
            for row in result:
                one_recipe = {
                    # do recipes.column because recipes is the table that it comes from.
                    'id' : row['recipes.id'],
                    'name' : row['name'],
                    'description' : row['description'],
                    'instructions' : row['instructions'],
                    'date_made_on' : row['date_made_on'],
                    'under_30_minutes' : row['under_30_minutes'],
                    'created_at' : row['recipes.created_at'],
                    'updated_at' : row['recipes.updated_at'],
                    'user_id' : row['user_id']
                }
                # create instance of a recipe
                recipe = Recipe(one_recipe)
                # put recipe instances in a list
                recipes_list.append(recipe)
            # make an instance of user with an attribute that equals a list of recipes.
            one_user.recipes_list = recipes_list
            print(one_user.recipes_list)
            return one_user
        return []

    @staticmethod
    def validate_user_registration(data):
        isValid = True
        if data['first_name'] == "":
            flash("Your first name is required for registration.", "error_first_registration")
            isValid = False
        if len(data['first_name']) < 2:
            flash("Your first name must be at least 2 characters long for registration.", "error_first_registration")
            isValid = False
        if data['last_name'] == "":
            flash("Your last name is required for registration.", "error_last_registration")
            isValid = False
        if len(data['last_name']) < 2:
            flash("Your last name must be at least 2 characters long for registration.", "error_last_registration")
            isValid = False
        if data['email'] == "":
            flash("Your email is required for registration.", "error_email_registration")
            isValid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("You must provide a valid email for registration.", "error_email_registration")
            isValid = False
        if data['password'] == "":
            flash("You must provide a password.", "error_password_registration")
            isValid = False
        if len(data['password']) < 8:
            flash("Your password must be at least 8 characters long.", "error_password_registration")
            isValid = False
        if data["confirm_password"] != data['password']:
            flash("Your password and password confirmation must match.", "error_confirm_password_registration")
            isValid = False
        return isValid

    @staticmethod
    def validate_user_session(keyname):
        if keyname in session:
            return True
        else:
            flash("You must login to view this page.", "error_must_login")
            return False