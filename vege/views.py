from multiprocessing import context
from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url="/login-page/")
def recipe(request):
    if request.method == "POST":
        data = request.POST
        recipeImage = request.FILES.get('recipeImage')
        recipeName = data.get('recipeName')
        recipeDescription = data.get('recipeDescription')
        
        Recipe.objects.create(
            Recipe_name = recipeName,
            recipe_description = recipeDescription,
            recipe_image =recipeImage,
        ) 
        return redirect('/recipes/')
    
    queryset = Recipe.objects.all()
    
    if request.GET.get('search'):
        queryset = queryset.filter(Recipe_name__icontains = request.GET.get('search'))
    
    context = {'recipes': queryset}
    return render(request,"recipe.html",context)

@login_required(login_url="/login-page/")
def home(request):
    return redirect('/login-page/')

@login_required(login_url="/login-page/")
def update_recipe(request,id):
    queryset = Recipe.objects.get(id = id)
    context = {'recipe': queryset}
    
    if request.method == "POST":
        data = request.POST
        recipeImage = request.FILES.get('recipeImage')
        recipeName = data.get('recipeName')
        recipeDescription = data.get('recipeDescription')
        
        queryset.Recipe_name = recipeName
        queryset.recipe_description = recipeDescription
        
        if recipeImage:
            queryset.recipe_image = recipeImage
            
        queryset.save()
        return redirect('/recipes/')
        
    
    return render(request,"update_recipe.html",context)

@login_required(login_url="/login-page/")
def delete_recipe(request,id):
    queryset = Recipe.objects.get(id = id)
    queryset.delete()
    return redirect('/recipes/')

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not User.objects.filter(username = username).exists():
            messages.error(request,"Invalid Username")
            return redirect('/login-page/')
        
        user = authenticate(username = username , password = password)
        
        if user is None:
            messages.error(request,"Invalid Password")
        else:
            login(request,user)
            return redirect('/recipes/')
        
    return render(request,"login.html")


def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = User.objects.filter(username = username)
        
        if user.exists():
            messages.error(request, "Username already taken")
            return redirect('/register-page/')
        
        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username
        )
        user.set_password(password)
        user.save()
        messages.success(request,"Account created successfully")
        return redirect('/register-page/')
    
    return render(request,"register.html")

def logout_page(request):
    logout(request)
    return redirect('/login/')