from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import User

def index(request):
    return render(request,"login_app/index.html")

def registration(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        if request.method == "POST":
            new_first_name = request.POST["first_name"]
            new_last_name = request.POST["last_name"]
            new_email = request.POST["email"]
            new_birthday = request.POST["birthday"]
            new_password = request.POST["password"]
            hash1 = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
            print(hash1)
            new_user = User.objects.create(first_name=new_first_name, last_name=new_last_name, email=new_email, birthday=new_birthday, password=hash1)
            messages.success(request,"You have sucessfully registered. Please Login")
            return redirect("/")

def login(request):
    valid = True
    if len(request.POST['email']) < 1:
        valid = False
        messages.error(request, "You must enter an email to login")
    if len(request.POST['password']) < 8: 
        valid = False
        messages.error(request, "Password must be longer than 8 characters")
        return redirect('/')
    else:
        if request.method == "POST":
            user = User.objects.filter(email=request.POST['email'])
            print(user)
            if len(user) == 0: 
                messages.error(request,"Records do not match, please try again")
                return redirect('/')
            else:
                person = user[0]
                if bcrypt.checkpw(request.POST['password'].encode(),person.password.encode()):
                    request.session['id'] = person.id
                    return redirect("/success")
                else:
                    messages.error(request,"Records do not match, please try again")
                    return redirect('/')

def success(request):
    if 'id' not in request.session:
        messages.error(request,"You must be logged in first")
        return redirect("/")
    else:
        context = {
            "user" : User.objects.get(id=request.session['id'])
        }
        return render(request,"login_app/success.html", context)

def logout(request):
    del request.session['id']
    return redirect("/")