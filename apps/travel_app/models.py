from __future__ import unicode_literals
from django.db import models
from ..login_reg_app.models import User
from datetime import datetime

class PlanManager(models.Manager):
    def validate(self, data):
        errors = []

        if not data["destination"]:
            errors.append("Destination is required")

        if not data["description"]:
            errors.append("Description is required")

        if not data["travel_date_from"]:
            errors.append("Travel Date From is required")
        elif data["travel_date_from"] < str(datetime.today()):
            errors.append("Travel Date must not be in the past")

        if not data["travel_date_to"]:
            errors.append("Travel Date To is required")
        elif data['travel_date_to'] < data['travel_date_from']:
            errors.append("Travel Date To must be after Travel Date From")

        response = {}

        if not errors:
            response['added'] = True
        else:
            response['added'] = False
            response['errors'] = errors
        return response



class Plan(models.Model):
    destination = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    travel_date_from = models.DateField(auto_now_add=False, auto_now=False)
    travel_date_to = models.DateField(auto_now_add=False, auto_now=False)
    user_plans = models.ForeignKey(User)
    all_users = models.ManyToManyField(User, related_name='all_plans')

    objects = PlanManager()
