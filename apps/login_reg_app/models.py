from __future__ import unicode_literals
from django.db import models
import bcrypt, re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

ONLY_LETTERS = re.compile(r'^[a-zA-Z]+$')

class UserManager(models.Manager):
    def register(self, data):
        errors = []

        if not data["first_name"]:
            errors.append("First Name is required")
        elif len(data["first_name"]) < 3:
            errors.append("First Name must be at least 2 characters")
        elif not ONLY_LETTERS.match(data["first_name"]):
            errors.append("First Name must contain only letters")

        if not data["last_name"]:
            errors.append("Last Name is required")
        elif len(data["last_name"]) < 2:
            errors.append("Last Name must be at least 2 characters")
        elif not ONLY_LETTERS.match(data["last_name"]):
            errors.append("Last Name must contain only letters")

        if not data["email"]:
            errors.append("Please enter an E-mail address")
        elif not EMAIL_REGEX.match(data["email"]):
            errors.append("Not a valid E-mail")
        elif User.objects.filter(email=data['email']):
            errors.append("Email is in use")

        if not data["password"]:
            errors.append("Please enter a password")
        elif len(data["password"]) < 8:
            errors.append("Password must be 8 characters")
        elif data["password"] != data["confirm"]:
            errors.append("Password and confirm password must match")

        response = {}

        password = data["password"].encode()
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())

        if not errors:
            new_user = self.create(first_name=data['first_name'], last_name=data['last_name'], email=data['email'], password=hashed)
            response['added'] = True
            response['new_user'] = new_user
        else:
            response['added'] = False
            response['errors'] = errors
        return response

    def login(self, data):
        user = User.objects.filter(email=data['email'])

        if not user:
            return False
        else:
            user = user[0]

        password = data['password'].encode()

        if bcrypt.hashpw(password, user.password.encode()) == user.password.encode():
            return user
        else:
            return False


class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
# Create your models here.
