
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required

import sweetify
from datetime import datetime
from .models import Enquiry


from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth, Group

import sweetify
from .forms import EnquiryForm



def login_view(request):
  
        if request.user.is_authenticated:
            return redirect('/')
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                usergroup = Group.objects.get(name='farmer')
                if request.user.groups.filter(name=usergroup).exists():
                    request.session['group_value'] = 'farmer'
                    sweetify.success(request, 'Log in Successful! \n hello, ' + str(request.user))
                    return redirect('/admin_dashboard/')
                else:
                    request.session['group_value'] = 'customer'
                    sweetify.success(request, 'Log in Successful! \n hello, ' + str(request.user))
                    return redirect('/')
            else:
                sweetify.error(request, 'User doesn\'t exist - register to canteen ')

        return render(request, 'login.html')
   

def signup_view(request):
   
        if request.user.is_authenticated:
            return redirect('/')
        userg = Group.objects.all()[:2]
        print(userg)
        if request.method == 'POST':
            full_name = request.POST['fullname']
            name = full_name.split(" ", 2)
            first_name = name[0]
            try:
                name[1].exists()
                last_name = name[1]
            except Exception as e:
                last_name = ''
            username = request.POST['username']
            email = request.POST['email']
            gender = request.POST['gender']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            user_type = request.POST['user_type']
            if password1 == password2:
                if User.objects.filter(username=username).exists():
                    sweetify.error(request, ' Username taken ')
                    return render(request, 'register_form.html', {'userg': userg})
                if User.objects.filter(email=email).exists():
                    sweetify.error(request, ' Email already registered... ')
                    return render(request, 'register_form.html', {'userg': userg})
                else:
                    user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                                    email=email, password=password1)
                    usergroup = Group.objects.get(name=user_type)
                   
                    if user_type == 'farmer':
                        
                        usergroup.user_set.add(user)
                        user.is_active = False
                        user.save()
                        
                        sweetify.success(request, 'User creation Successful!')
                    elif user_type == 'customer':
                        
                        usergroup.user_set.add(user)
                        user.is_active = True
                        user.save()
                        
                        sweetify.success(request, 'User creation Successful!')
                        return redirect('/accounts/login')
                    return redirect('accounts:profile')
                    
            else:
                sweetify.error(request, 'password not matching ')
        return render(request, 'register_form.html', {'userg': userg})
    



def logout_view(request):
 
        if request.user.is_authenticated:
            auth.logout(request)
        return redirect('/')
  
def enquiry(request):
    # if request.user.is_authenticated:
        if request.method == "POST":
            name = request.POST.get('name')
            email = request.POST.get('email')
            firm = request.POST.get('firm')
            register = Enquiry(name=name, email=email, firm=firm, date=datetime.today())
            register.save()
        return render(request, 'main/home.html')
@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
                                #    u_form.is_valid() and
        if  p_form.is_valid():
            # u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('/')
 
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
 
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
 
    return render(request, 'profile.html', context)                