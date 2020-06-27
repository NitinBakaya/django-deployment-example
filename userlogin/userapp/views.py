from django.shortcuts import render
from userapp.myform import UserForm,UserInfoForm
from userapp.models import UserProfileInfo
# Create your views here.

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login,authenticate,logout


def index(request):
    return render(request,'userapp/index.html')

def register(request):

# registered variable for if the form is registered or not.
    registered = False
# if we got the POST request means the user wants to save the data.
    if request.method == "POST":
# grab the data from both the forms
        user_info = UserForm(request.POST)
        profile_info = UserInfoForm(request.POST)
# check if both the forms are valid or not
        if user_info.is_valid() and profile_info.is_valid():
# save intially what data was posted
            user = user_info.save()
# save the password as hash
            user.set_password(user.password)
# save the password hash to the model
            user.save()
# we have set the commit to false as we dont want to make the collision with the other form data
            profile = profile_info.save(commit=False)
# what we created one to one relationship, we are creating the same in the views file also
            profile.user = user
# We have to check weather we have any profile pic in the post request if so than we grab that and save it ot the model
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
# save the profile form data
            profile.save()
# At last the form is registered
            registered = True
# the else part shows if the form is not registered than errors are occured
        else:
            print(user_info.errors,profile_info.errors)
# This else part is for if the request is just an http request so we just display the forms
    else:
        user_info = UserForm()
        profile_info = UserInfoForm()

    return render(request,'userapp/register.html',{
                            'user_info':user_info,
                            'profile_info':profile_info,
                            'registered':registered})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def  user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Account is not Active")

        else:
            print("Login Failed.Please try again!!!")
            print("username:{} password:{}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request,'userapp/login.html',{})
