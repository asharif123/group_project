from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index),
    path('registration', views.registration),
    path('registered', views.registered),
    path('login', views.login),
    path('cookbook', views.cookbook),
    path('logout', views.logout),
    path('founders', views.founders),
    path('privacypolicy', views.privacypolicy),
    path('terms', views.terms),
    path('userprofile/<int:id>', views.userprofile),
    path('search', views.search),
    path('adding_profile_pic/<int:id>', views.adding_profile_pic),
    path('deletepicture', views.deleteprofilepicture),
    ####################Ricky
    # main dishes
    path('welcome', views.welcome),
    path('recipe/create', views.create_recipe),
    path('recipe/add', views.add_recipe),
    path('recipe/best', views.dish_of_the_week),
    path('recipe/info/<int:id>', views.recipe_info),
    path('recipe/delete/<int:id>', views.delete_recipe),
    path('recipe/edit/<int:id>', views.edit_recipe),
    path('recipe/update/<int:id>', views.update_recipe),
    path('review/add', views.add_review_to_recipe),
    path('review/delete', views.delete_review),
    path('recipe/filter', views.filter_recipe),
    # DESSERTS
    path('desserts/page', views.desserts),
    path('desserts/create', views.create_dessert),
    path('desserts/add', views.add_dessert),
    path('dessert/info/<int:id>', views.dessert_info),
    path('dessert/update/<int:id>', views.update_dessert),
    path('dessert/best', views.dessert_of_the_week),
    path('dessert/filter', views.filter_dessert)






] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)