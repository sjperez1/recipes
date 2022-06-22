from flask_app import DATABASE
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under_30_minutes = data['under_30_minutes']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes;"
        query_result = connectToMySQL(DATABASE).query_db(query)
        # the if query result and return [] are saying that if recipes is an empty list (no values found in the table), then it would normally return false, but we want to avoid that, so return and empty list if query_result is empty list with no dictionaries.
        if query_result:
            recipes = []
            for recipe in query_result:
                recipes.append(cls(recipe))
            print(recipes[0])
            return recipes
        return []

    @classmethod
    def get_recipe(cls, data):
        query = "SELECT * "
        query += "FROM recipes "
        query += "WHERE id = %(id)s;"
        # Put the following in result so that the first entry can later be selected. The query, which comes back as a list of dictionaries, will be stored in a variable that I am calling result. One item in the list will be a dictionary. Use print statements to visualize.
        result = connectToMySQL(DATABASE).query_db(query, data)
        print(result)
        # Need result[0] because result is a list of dictionaries and I want to look at the first dictionary in the result list to to get the user with that id. Found this out by printing result and refreshing page and looking at the list in my terminal.
        # This line: one_recipe = cls(result[0])   is creating an instance of a recipe. one_recipe is like the variable name for this recipe that I can use in other files that use this classmethod. cls is like saying the class name Recipe and the result[0] in parentheses has all of the info that each recipe will have, as specified at the top of this file in def __init__(self, data). Use print to visualize one_recipe. Return the instance of the class at the end.
        # When you make a query, the database knows its a recipe, but these python files do not know that it is recipe, which is why an instance of a recipe still has to be made after the query.
        one_recipe = cls(result[0])
        print(one_recipe)
        return one_recipe

    @classmethod
    def delete_recipe(id, data):
        query = "DELETE FROM recipes "
        query += "WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def create(cls, data):
        query = "INSERT INTO recipes(name, description, instructions, under_30_minutes, created_at, user_id) VALUES( %(name)s, %(description)s, %(instructions)s, %(under_30_minutes)s, %(created_at)s, %(user_id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def update_recipe(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, under_30_minutes = %(under_30_minutes)s, created_at = %(created_at)s WHERE id = %(id)s;"

        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def validate_new_recipe(data):
        isValid = True
        if data['name'] == "":
            flash("You must provide a name.", "error_name")
            isValid = False
        if len(data['name']) < 3:
            flash("Your name must be at least 3 characters long.", "error_name")
            isValid = False
        if data['description'] == "":
            flash("You must provide a description.", "error_description")
            isValid = False
        if len(data['description']) < 3:
            flash("Your description must be at least 3 characters long.", "error_description")
            isValid = False
        if data['instructions'] == "":
            flash("You must provide instructions.", "error_instructions")
            isValid = False
        if len(data['instructions']) < 3:
            flash("Your instructions must be at least 3 characters long.", "error_instructions")
            isValid = False
        if data['created_at'] == "":
            flash("You must select the date the recipe was made.", "error_created_at")
            isValid = False
        if data['under_30_minutes'] == "":
            flash("You must select 'yes' or 'no'.", "error_under_30_minutes")
            isValid = False
        return isValid