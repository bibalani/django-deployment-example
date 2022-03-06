import re
from django.shortcuts import render, redirect
from my_app.models import UserProfileInfo, User
from my_app.forms import UserForm, UserProfileInfoForm

from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    context = {}
    return render(request, 'my_app/index.html', context)

@login_required
def special(request):
    return render(request, 'my_app/special.html', {})
    # return HttpResponse('You have logged in, Nice!')    

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('my_app:index'))    

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        # if user passes authentication process
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('my_app:special'))
            else:
                return HttpResponse('ACCOUNT IS NOT ACTIVE')
        else:
            print('Someone palnned to login and failed')
            print('Username: {} and Password: {}'.format(user, password))    
            return HttpResponse('Invalid login details supplied')
    else:
        return render(request,'my_app/login.html',{})     


def registration(request):

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        user_profile_info_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and user_profile_info_form.is_valid():
            # grabbibg the user_form and save it to the databases and hashing the password (user.password) for saved password
            # and then saving new version of user into database
            user = user_form.save()
            

            user.set_password(user.password)
            user.save()

            profile = user_profile_info_form.save(commit=False)
            # save method convert a form to model
            # the user field in profile table is equalled with user id in user table
            profile.user = user

            # we boublecheck if there is a picture into new profile object
            # request.FILES = {'portfolio_site':'','profile_pic':''}
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            registered = True
        else:
            print(user_form.errors, user_profile_info_form.errors)
    else:
        user_form = UserForm()
        user_profile_info_form = UserProfileInfoForm()
    return render(request, 'my_app/registration.html',
                 {'user_form':user_form,
                 'user_profile_info_form':user_profile_info_form,
                 'registered':registered})



       











        
