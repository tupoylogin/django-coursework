from django.shortcuts import render, redirect
from django import template
from django.template.loader import get_template
from py.forms import UserForm
from py.models import Tours
from django.contrib.auth import login as auth_login, logout, authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm


def home(request):
    return render(request,'index.html')


@login_required
def user_cab(request):
    return render(request,'usercab.html')


def login(request):
    return render(request,'login.html')


def registration(request):
    return render(request,'registration.html')


@login_required
def search(request):
    return render(request,'search.html')


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user_form.save(commit=True)
            registered = True
            return HttpResponseRedirect(reverse('user_login'))
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    return render(request, 'registration.html', {'user_form': user_form, 'registered': registered})


@login_required
def special(request):
    return HttpResponse("You are already logged in")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('user_login'))


def user_login(request):
    if request.method == 'POST':
        auth_form = AuthenticationForm(data=request.POST)
        if auth_form.is_valid():
            user = auth_form.get_user()
            auth_login(request, user)
            return HttpResponseRedirect(reverse('search'))
        else:
            print(auth_form.errors)
    else:
        auth_form = AuthenticationForm()
        return render(request, 'login.html', {'auth_form': auth_form})


def rendr(request):
    events = Tours.objects.only('country')
    t = get_template('search.html')
    context = {
        'events': events
        }
    c = template.Context(context)
    r = t.render(c)
    return HttpResponse(r)


def search_result(request):
    if request.method=="POST":
        search_query = request.POST['search_query']
    else:
        search_query =''

    tours = Tours.objects.filter(country=search_query).only('place','description')

    return render({'tours': tours}, template_name='search_results.html')