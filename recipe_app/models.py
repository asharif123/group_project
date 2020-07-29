from PIL import Image
import re, bcrypt
from django.db import models

# Create your models here.

class Users_Manager(models.Manager):

    def registration_validator(self, postData):
        errors = {}

        if len(postData["First_Name"]) < 2:
            errors["First_Name"] = "First Name must have at least 2 characters!"

        if len(postData["Last_Name"]) < 2:
            errors["Last_Name"] = "Last Name must have at least 2 characters!"

        # see if email is either in correct format or in the database
        REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not REGEX.match(postData['Email']):                
            errors['Email'] = ("Invalid email address format!")

        email = Users.objects.filter(email=postData["Email"])
        if len(email) > 0:
            errors["Email"] = ("Account already exists!")

        if len(postData["Password"]) < 8:
            errors["Password"] = ("Password must be at least 8 characters!")

        if (postData["Password"] != postData["Confirm"]):
            errors["Password"] = ("Password and Confirm password do not match!")

        return errors

    def login_validator(self,postData):
        errors = {}

        REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not REGEX.match(postData["Email"]):                
            errors['Email'] = ("Invalid email address format!")

        if len(postData["Password"]) < 8:
            errors["Password"] = ("Password must be at least 8 characters!")

        # check if login email is in the database!
        #if login email in database, see if the password entered matches to stored password for that email in the database
        user = Users.objects.filter(email=postData["Email"])

        if len(user) == 0:
            errors["Email"] = ("Email does not exists, please register or try a different account!")

        else:
            user = Users.objects.filter(email=postData["Email"])[0]
            if not bcrypt.checkpw(postData["Password"].encode(), user.password.encode()):
                errors["Password"] = ("Password is incorrect!")

        return errors

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
        if len(postData["Review"]) < 10:
            errors["Review"] = "Review must be at least 10 characters long!"

        return errors


class Users(models.Model):

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Users_Manager()

class Recipes(models.Model):
    name = models.CharField(max_length=255)
    summary = models.TextField()
    ingredients = models.TextField()
    steps = models.TextField()
    image = models.ImageField()
    owner = models.ForeignKey(Users,related_name="recipes_of_user",on_delete = models.CASCADE)
    is_dessert = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Recipes_Manager()


class Reviews(models.Model):
    content = models.TextField()
    rating = models.IntegerField()
    reviewer = models.ForeignKey(Users,related_name="reviews_of_user",on_delete = models.CASCADE)
    recipe = models.ForeignKey(Recipes,related_name="reviews_of_recipe",on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    objects = Reviews_Manager()


