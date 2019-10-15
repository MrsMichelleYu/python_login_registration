from __future__ import unicode_literals
from django.db import models
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        date_of_birth = datetime.strptime(postData['birthday'], "%Y-%m-%d")
        rdelta = relativedelta(datetime.now(), date_of_birth)
        # age = int(datetime.now() - date_of_birth)
        # year = timedelta(days=365)
        # thirteen_years = 13 * year
        check_email = User.objects.filter(email=postData["email"])
        if len(postData["first_name"]) < 2:
            errors["first_name"] = "First name must be entered and should be at least 2 characters"
        if len(postData["last_name"]) < 2:
            errors["last_name"] = "Last name must be entered and should be at least 2 characters"
        if not EMAIL_REGEX.match(postData["email"]): 
            errors["email"] = "Not a valid email address" 
        if len(check_email) > 0: 
            errors["email"] = "This email address already exists in the system" 
        if len(postData["password"]) < 8:
            errors["password"] = "Password must be more than 8 characters"
        if postData["password"] != postData["confirm_password"]:
            errors["confirm_password"] = "Passwords do not match"
        if datetime.now() <= date_of_birth: #as datetime progresses, it gets larger. So if current datetime is smaller number than birthday, then you are putting the current date in the past and it's not valid.
            errors["birthday"] = "Birthday must not be in the future"
        if (rdelta.years < 13):
            errors["birthday"] = "You must be at least 13 years to register"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=255)
    birthday = models.DateTimeField()
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
