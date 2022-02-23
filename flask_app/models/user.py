from flask_app.config.mysqlconnection import connectToMySQL
import re
from datetime import date, datetime
from flask import flash
from flask_app import app
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]')
PASS_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d\w\W]{8,}$')
todays_date = date.today()
minimum_age_string = f'{todays_date.year - 13}-{todays_date.month}-{todays_date.day}'
minimum_age_date = datetime.strptime(minimum_age_string, '%Y-%m-%d')

class User:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.date_of_birth = data['date_of_birth']
        self.fav_lang = data['fav_lang']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    @staticmethod
    def validate_user(first_name, last_name, email, date_of_birth, language, password, pass_confirm):
        is_valid = True
        if len(first_name) < 2:
            flash("First name must be at least 2 characters.", "register")
            is_valid = False
        if not NAME_REGEX.match(first_name):
            flash("First name must only contain letters.", "register")
            is_valid = False
        if len(last_name) < 2:
            flash("Last name must be at least 2 characters.", "register")
            is_valid = False
        if not NAME_REGEX.match(last_name):
            flash("Last name must only contain letters.", "register")
            is_valid = False
        if not EMAIL_REGEX.match(email):
            flash("Please enter a valid email address.", "register")
            is_valid = False
        if date_of_birth == '':
            flash("Must enter a date of birth.", "register")
            is_valid = False
        if not date_of_birth == '':
            if not datetime.strptime(date_of_birth, '%Y-%m-%d') <= minimum_age_date:
                flash("Must be 13 years of age to register.", "register")
                is_valid = False
        if language == "none":
            flash("Must select a favorite programming language option.", "register")
            is_valid = False
        if password == '':
            flash("Must enter a password.")
            is_valid = False
        if not PASS_REGEX.match(password):
            flash("Password must be a minimum of 8 characters, and contain at least one uppercase letter, lowercase letter, and number.", "register")
            is_valid = False
        if not pass_confirm == password:
            flash("Passwords do not match.", "register")
            is_valid = False
        return is_valid
    @classmethod
    def register_new_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, date_of_birth, fav_lang, password, created_at, updated_at) VALUE (%(first_name)s, %(last_name)s, %(email)s, %(date_of_birth)s, %(fav_lang)s, %(password)s, NOW(), NOW());"
        results = connectToMySQL('login_and_registration_schema').query_db(query, data)
        return results
    @classmethod
    def get_user(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL('login_and_registration_schema').query_db(query, data)
        return results