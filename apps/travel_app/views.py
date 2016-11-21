from django.shortcuts import render, redirect
from .models import Plan
from ..login_reg_app.models import User
from django.contrib import messages

def index(request):
    if 'user_id' not in request.session:
        return redirect("login_reg:index")

    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'plans': Plan.objects.filter(user_plans__id=request.session['user_id'])|Plan.objects.filter(all_users__id=request.session['user_id']),
        'others_plans': Plan.objects.all().exclude(user_plans__id=request.session['user_id'])
    }
    return render(request, "travel_app/index.html", context)

def logoff(request):
    request.session.clear()
    return redirect("login_reg:index")

def show(request, id):
    context = {
        "destination": Plan.objects.filter(id=id),
        "other_users": User.objects.filter(all_plans__id=id)
    }
    return render(request, "travel_app/show.html", context)

def add_page(request):
    return render(request, "travel_app/add.html")

def add_trip(request):
    res = Plan.objects.validate(request.POST)

    if res['added']:
        Plan.objects.create(destination=request.POST['destination'], description=request.POST['description'], travel_date_from=request.POST['travel_date_from'], travel_date_to=request.POST['travel_date_to'], user_plans=User.objects.get(id=request.session['user_id']))
    else:
        for error in res['errors']:
            messages.error(request, error)
        return redirect('travel_app:add_page')

    return redirect("travel_app:index")

def join(request, id):
    user = User.objects.get(id=request.session['user_id'])
    trip = Plan.objects.get(id=id)
    trip.all_users.add(user)

    return redirect('travel_app:index')
