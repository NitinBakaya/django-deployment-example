from django.urls import path
from userapp import views

app_name = 'userapp'

urlpatterns = [
    path('register/',views.register,name='register'),
    path('user_login/',views.user_login,name='user_login'),
]
