from __future__ import unicode_literals
import re, bcrypt
from django.db import models

#######################################################################


class UserManager(models.Manager):
    def basic_validator(self, postData, sign_in):
        errors = {}
        if sign_in == 'registration':
            if len(postData['first_name'])<2:
                errors['first_name'] = "First name needs to be longer than 2 characters"
            if len(postData['last_name'])<2:
                errors['last_name'] = "Last name needs to be longer than 2 characters"
            if len(postData['password'])<8:
                errors['password'] = "Password needs to be longer than 8 characters"
            if postData['confirm_password'] != postData['password']:
                errors['confirm_password'] = "Passwords do NOT match"

            EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
            if not EMAIL_REGEX.match(postData['email']): # test whether a field matches the pattern
                errors['email'] = ("Invalid email address!")

        elif sign_in == 'login':
            user = User.objects.filter(email=postData['email'])
            if not user:
                errors['user_login'] = 'Incorrect email'
            else:
                if not bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):
                    errors['user_password'] = 'Incorrect Password'

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profilepic = models.CharField(null=True, max_length=255)
    objects = UserManager()


# Create your models here.


# Create your models here.

class Recipes_Manager(models.Manager):

    def recipe_validator(self,postData):
        errors = {}
        if len(postData["Recipe_Name"]) < 3:
            errors["Recipe_Name"] = "Recipe name must have at least 3 characters!"

        if len(postData["Description"]) < 5:
            errors["Description"] = "Description must have at least 5 characters!"

        if len(postData["Ingredients"]) < 10:
            errors["Ingredients"] = "Ingredients must have at least 10 characters!"

        if len(postData["Steps"]) < 10:
            errors["Steps"] = "Steps must have at least 10 characters!"

        return errors
        

class Reviews_Manager(models.Manager):
    def reviews_validator(self,postData):
        errors = {}
        if len(postData["Review"]) < 1:
            errors["Review"] = "Review must be at least 10 characters long!"

        return errors




class Recipes(models.Model):
    name = models.CharField(max_length=255)
    summary = models.TextField()
    ingredients = models.TextField()
    steps = models.TextField()
    image = models.ImageField()
    owner = models.ForeignKey(User,related_name="recipes_of_user",on_delete = models.CASCADE)
    is_dessert = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Recipes_Manager()


class Reviews(models.Model):
    content = models.TextField()
    rating = models.IntegerField()
    reviewer = models.ForeignKey(User,related_name="reviews_of_user",on_delete = models.CASCADE)
    recipe = models.ForeignKey(Recipes,related_name="reviews_of_recipe",on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    objects = Reviews_Manager()

##########################################################################################################



