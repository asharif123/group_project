from django.shortcuts import render, redirect, HttpResponse
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
import bcrypt
from .models import *

##############################################################################################################

def index(request):
    return render(request, 'index.html')

def registration(request):
    errors = User.objects.basic_validator(request.POST, 'registration')
    if len(errors)>0:
        for key,value in errors.items():
            messages.error(request,value)
        return redirect('/')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        print(pw_hash)
        
        User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = pw_hash)

        return redirect('/registered')

def registered(request):
    return redirect('/')

def login(request):
    errors = User.objects.basic_validator(request.POST, 'login')
    if len(errors)>0:
        for key,value in errors.items():
            messages.error(request,value)
        return redirect('/')
    else:
        user = User.objects.filter(email=request.POST['email'])
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['userid'] = logged_user.id
                return redirect("/cookbook") #redirect to success route
        # return redirect('/')

def cookbook(request):
    user = User.objects.get(id = request.session['userid'])
    context = {
        'user':user,
    }
    return render(request, 'cookbook.html',context)

def logout(request):
    request.session.flush()
    return redirect('/')

def founders(request):
    user = User.objects.get(id = request.session['userid'])
    context = {
        'user':user,
    }
    return render(request, "founders.html", context)

def privacypolicy(request):
    user = User.objects.get(id = request.session['userid'])
    context = {
        'user':user,
    }
    return render(request, "privacypolicy.html", context)

def terms(request):
    user = User.objects.get(id = request.session['userid'])
    context = {
        'user':user,
    }
    return render(request, "terms.html", context)

def userprofile(request, id):
    user = User.objects.get(id = request.session['userid'])
    context = {
        'user':user,
    }
    return render(request, "userprofile.html", context)

def search(request):
    user = User.objects.get(id = request.session['userid'])
    pass



################################################################################################################

def welcome(request):
    if 'userid' not in request.session:
        return redirect('/')

    user = User.objects.get(id=request.session['userid'])
    recipes = Recipes.objects.all()
    all_reviews = []
    all_recipes = []
    sorted_recipes = []
    for recipe in recipes:
        if recipe.is_dessert == False:
            all_recipes.append(recipe)
            all_reviews.append(len(recipe.reviews_of_recipe.all()))
    all_reviews = sorted(all_reviews, reverse=True)
    i = 0
    for i in range(len(all_reviews)):
        for recipe in all_recipes:
            if (all_reviews[i] == len(recipe.reviews_of_recipe.all())):
                sorted_recipes.append(recipe)
    # for recipe in sorted_recipes:
    #     print(len(recipe.reviews_of_recipe.all()))
    top_recipes = sorted_recipes

    context = {
        "user": user,
        "Top_Recipes": top_recipes
    }
    return render(request,'welcome.html', context)

def filter_recipe(request):
    if 'userid' not in request.session:
        return redirect('/')
    filtered_recipes = []
    user = User.objects.get(id=request.session['userid'])
    recipes = Recipes.objects.all()
    for recipe in recipes:
        if (request.POST["Filter"] in (recipe.name)):
            filtered_recipes.append(recipe)
    context = {
        "User": user,
        "Filtered_Recipes": filtered_recipes
    }
    return render(request,'filtered_recipes.html',context)
    
def filter_dessert(request):
    # if 'userid' not in request.session:
    #     return redirect('/')
    filtered_recipes = []
    user = User.objects.get(id=request.session['userid'])
    recipes = Recipes.objects.all()
    for recipe in recipes:
        if (request.POST["Filter"] in (recipe.name)):
            filtered_recipes.append(recipe)
    context = {
        "User": user,
        "Filtered_Recipes": filtered_recipes
    }
    return render(request,'filtered_recipes.html',context)



def create_recipe(request):
    if 'userid' not in request.session:
        return redirect('/')

    user = User.objects.get(id=request.session['userid'])
    context = {
        "user": user
    }

    return render(request, 'add_recipe.html', context)

def add_recipe(request):
    if 'userid' not in request.session:
        return redirect('/')

    errors = Recipes.objects.recipe_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/recipe/create')
    # print(request.POST["Description"])
    if request.method == "POST":
        # request.Files used for uploading anything
        pic = request.FILES["Image"]
    fs = FileSystemStorage()
    user_pic = fs.save(pic.name, pic)
    url = fs.url(user_pic)
    recipe = Recipes.objects.create(name=request.POST["Recipe_Name"],summary=request.POST["Description"],ingredients=request.POST["Ingredients"],steps=request.POST["Steps"], image=user_pic, owner=User.objects.get(id=request.session['userid']), is_dessert=False)
    # print(recipe.ingredients)
    return redirect(f'/recipe/info/{recipe.id}')



def dish_of_the_week(request):
    if 'userid' not in request.session:
        return redirect('/')
    recipes = Recipes.objects.all()

    all_reviews = []
    all_recipes = []
    sorted_recipes = []
    # print(['*']*100)
    for recipe in recipes:
        if recipe.is_dessert == False:
            all_recipes.append(recipe)
            all_reviews.append(len(recipe.reviews_of_recipe.all()))
    all_reviews = sorted(all_reviews, reverse=True)
    i = 0
    for i in range(len(all_reviews)):
        for recipe in all_recipes:
            if (all_reviews[i] == len(recipe.reviews_of_recipe.all())):
                sorted_recipes.append(recipe)
    # for recipe in sorted_recipes:
    #     print(len(recipe.reviews_of_recipe.all()))
    top_recipe = sorted_recipes[0]
    ingredients = top_recipe.ingredients.split('\n')
    summary = top_recipe.summary.split('\n')
    steps = top_recipe.steps.split('\n')
    rating = 0
    for review in top_recipe.reviews_of_recipe.all():
        rating += review.rating
    if len(top_recipe.reviews_of_recipe.all()) > 0:
        average_rating = round(rating / len(top_recipe.reviews_of_recipe.all()),2)
    else:
        average_rating = 0
    reviews = top_recipe.reviews_of_recipe.all()

    context = {
        'User': User.objects.get(id=request.session['userid']),
        "recipes": top_recipe,
        "summary": summary,
        "ingredients": ingredients,
        "steps": steps,
        "rating": average_rating,
        "Reviews": reviews
    }


    
    return render(request,'dish_of_the_week.html',context)


def delete_recipe(request,id):
    if 'userid' not in request.session:
        return redirect('/')

    recipe_to_delete = Recipes.objects.get(id=id)
    recipe_to_delete.delete()
    return redirect('/welcome')

def edit_recipe(request,id):
    if 'userid' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['userid'])
    recipe = Recipes.objects.get(id=id)
    context = {
        "User": user,
        "recipe": recipe
    }

    return render(request, 'edit_recipe.html', context)

def update_recipe(request,id):
    if 'userid' not in request.session:
        return redirect('/')
    recipe_to_update = Recipes.objects.get(id=id)
    errors = Recipes.objects.recipe_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/recipe/edit/{recipe_to_update.id}')

    else:
        recipe_to_update.name = request.POST["Recipe_Name"]
        recipe_to_update.summary = request.POST["Description"]
        recipe_to_update.ingredients = request.POST["Ingredients"]
        recipe_to_update.steps = request.POST["Steps"]
        if request.method == "POST":

        # request.Files used for uploading anything
            pic = request.FILES["Image"]
            fs = FileSystemStorage()
            user_pic = fs.save(pic.name, pic)
            recipe_to_update.image = user_pic
        recipe_to_update.save()

        recipe_to_update.save()
        return redirect(f'/recipe/info/{recipe_to_update.id}')

def recipe_info(request,id):
    if 'userid' not in request.session:
        return redirect('/')

    recipe = Recipes.objects.get(id=id)
    # grab the ingredients, split by new line
    ingredients = recipe.ingredients.split('\n')
    summary = recipe.summary.split('\n')
    steps = recipe.steps.split('\n')
    rating = 0
    for review in recipe.reviews_of_recipe.all():
        rating += review.rating
    if len(recipe.reviews_of_recipe.all()) > 0:
        average_rating = round(rating / len(recipe.reviews_of_recipe.all()),2)
    else:
        average_rating = 0


    context = {
        'user': User.objects.get(id=request.session['userid']),
        'recipe': Recipes.objects.get(id=id),
        'ingredients': ingredients,
        'summaries': summary,
        'steps': steps,
        "Reviews": recipe.reviews_of_recipe.all().order_by("-created_at"),
        "rating": average_rating
    }

    # return render(request,'recipe_info.html',context)
    return render(request,'recipe_info.html',context)

def add_review_to_recipe(request):
    if 'userid' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['userid'])
    recipe = Recipes.objects.get(id=request.POST["recipe_id"])
    errors = Reviews.objects.reviews_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        # return redirect('/review/add')
        # return redirect(f'/recipe/info/{recipe.id}')
    else:
        review = Reviews.objects.create(content=request.POST["Review"],rating=request.POST["Rating"],reviewer=User.objects.get(id=request.session['userid']),recipe=recipe)
        context = {
            "Reviews": recipe.reviews_of_recipe.all().order_by('-created_at'),
            "User": user
        }
        return render(request,'add_review_ajax.html',context)


def delete_review(request):
    if 'userid' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['userid'])
    recipe = Recipes.objects.get(id=request.POST["recipe_id"])

    review = Reviews.objects.get(id=request.POST["review_id"])
    review_to_delete = review.delete()
    print(['*']*100)
    print(review)
    # return redirect(f'/recipe/info/{recipe_id}')
    # context = {
    #     "Reviews": recipe.reviews_of_recipe.all().order_by('-created_at'),
    #     "User": user
    # }

    return HttpResponse(review_to_delete)


def desserts(request):
    recipes = Recipes.objects.all()
    all_reviews = []
    all_recipes = []
    sorted_recipes = []
    for recipe in recipes:
        if (recipe.is_dessert == True):
            all_recipes.append(recipe)
            all_reviews.append(len(recipe.reviews_of_recipe.all()))
    for recipe in all_recipes:
        print(recipe.name)
    all_reviews = sorted(all_reviews, reverse=True)
    i = 0
    for i in range(len(all_reviews)):
        for recipe in all_recipes:
            if (all_reviews[i] == len(recipe.reviews_of_recipe.all())):
                sorted_recipes.append(recipe)
    # for recipe in sorted_recipes:
    #     print(len(recipe.reviews_of_recipe.all()))
    top_recipes = sorted_recipes

    context = {
        "user": User.objects.get(id=request.session['userid']),
        "Top_Recipes": top_recipes
    }
    return render(request,'dessert.html',context)

def create_dessert(request):
    if 'userid' not in request.session:
        return redirect('/')

    user = User.objects.get(id=request.session['userid'])
    context = {
        "User": user
    }

    return render(request, 'add_dessert.html', context)

def add_dessert(request):
    if 'userid' not in request.session:
        return redirect('/')

    errors = Recipes.objects.recipe_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/desserts/create')
    # print(request.POST["Description"])
    if request.method == "POST":
        # request.Files used for uploading anything
        pic = request.FILES["Image"]
    fs = FileSystemStorage()
    user_pic = fs.save(pic.name, pic)
    url = fs.url(user_pic)
    print(['*']*100)
    print(url)
    recipe = Recipes.objects.create(name=request.POST["Recipe_Name"],summary=request.POST["Description"],ingredients=request.POST["Ingredients"],steps=request.POST["Steps"], image=user_pic, owner=User.objects.get(id=request.session['userid']),is_dessert=True)
    # print(recipe.ingredients)
    return redirect(f'/dessert/info/{recipe.id}')

def dessert_info(request,id):
    if 'userid' not in request.session:
        return redirect('/')

    recipe = Recipes.objects.get(id=id)
    # grab the ingredients, split by new line
    ingredients = recipe.ingredients.split('\n')
    summary = recipe.summary.split('\n')
    steps = recipe.steps.split('\n')
    rating = 0
    for review in recipe.reviews_of_recipe.all():
        rating += review.rating
    if len(recipe.reviews_of_recipe.all()) > 0:
        average_rating = round(rating / len(recipe.reviews_of_recipe.all()),2)
    else:
        average_rating = 0


    context = {
        'User': User.objects.get(id=request.session['userid']),
        'recipe': recipe,
        'ingredients': ingredients,
        'summaries': summary,
        'steps': steps,
        "Reviews": recipe.reviews_of_recipe.all().order_by("-created_at"),
        "rating": average_rating

    }

    return render(request,'dessert_info.html',context)

def add_review_to_dessert(request):
    if 'userid' not in request.session:
        return redirect('/')

    recipe = Recipes.objects.get(id=request.POST["recipe_id"])
    print(['*']*100)
    errors = Reviews.objects.reviews_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/dessert/info/{recipe.id}')
    review = Reviews.objects.create(content=request.POST["Review"],rating=request.POST["Rating"],reviewer=User.objects.get(id=request.session['userid']),recipe=recipe)
    # return redirect(f'/dessert/info/{recipe.id}')
    context = {
        "Reviews": recipe.reviews_of_recipe.all()
    }
    return render(request,'add_review_ajax.html',context)

def delete_dessert(request,id):
    if 'userid' not in request.session:
        return redirect('/')

    dessert_to_delete = Recipes.objects.get(id=id)
    dessert_to_delete.delete()
    return redirect('/desserts/page')

def edit_dessert(request,id):
    if 'userid' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['userid'])
    recipe = Recipes.objects.get(id=id)
    context = {
        "User": user,
        "recipe": recipe
    }

    return render(request, 'edit_dessert.html', context)

def update_dessert(request,id):
    if 'userid' not in request.session:
        return redirect('/')
    recipe_to_update = Recipes.objects.get(id=id)
    errors = Recipes.objects.recipe_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/dessert/edit/{recipe_to_update.id}')

    else:
        recipe_to_update.name = request.POST["Recipe_Name"]
        recipe_to_update.summary = request.POST["Description"]
        recipe_to_update.ingredients = request.POST["Ingredients"]
        recipe_to_update.steps = request.POST["Steps"]
        if request.method == "POST":

        # request.Files used for uploading anything
            pic = request.FILES["Image"]
            fs = FileSystemStorage()
            user_pic = fs.save(pic.name, pic)
            url = fs.url(user_pic)

            recipe_to_update.image = user_pic
        recipe_to_update.save()
        return redirect(f'/dessert/info/{recipe_to_update.id}')



def dessert_of_the_week(request):
    if 'userid' not in request.session:
        return redirect('/')
    recipes = Recipes.objects.all()

    all_reviews = []
    all_recipes = []
    sorted_recipes = []
    # print(['*']*100)
    for recipe in recipes:
        if recipe.is_dessert:
            all_recipes.append(recipe)
        all_reviews.append(len(recipe.reviews_of_recipe.all()))
    all_reviews = sorted(all_reviews, reverse=True)
    i = 0
    for i in range(len(all_reviews)):
        for recipe in all_recipes:
            if (all_reviews[i] == len(recipe.reviews_of_recipe.all())):
                sorted_recipes.append(recipe)
    # for recipe in sorted_recipes:
    #     print(len(recipe.reviews_of_recipe.all()))
    top_recipe = sorted_recipes[0]
    print(['*']*100)
    # print(top_recipe.name)
    ingredients = top_recipe.ingredients.split('\n')
    summary = top_recipe.summary.split('\n')
    steps = top_recipe.steps.split('\n')
    rating = 0
    for review in top_recipe.reviews_of_recipe.all():
        rating += review.rating
    if len(top_recipe.reviews_of_recipe.all()) > 0:
        average_rating = round(rating / len(top_recipe.reviews_of_recipe.all()),2)
    else:
        average_rating = 0
    reviews = top_recipe.reviews_of_recipe.all().order_by('-created_at')
    # print("ALL")
    # for review in reviews:
    #     print(review.content)

    context = {
        'User': User.objects.get(id=request.session['userid']),
        "recipes": top_recipe,
        "summary": summary,
        "ingredients": ingredients,
        "steps": steps,
        "rating": average_rating,
        "Reviews": reviews
    }


    
    return render(request,'dessert_of_the_week.html',context)








    



