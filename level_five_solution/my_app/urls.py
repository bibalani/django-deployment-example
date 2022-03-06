from django.urls import path, include
from my_app import views



app_name = 'my_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('user_login/', views.user_login, name='user_login'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('special/', views.special, name='special'),
    path('registration/', views.registration, name='registration'),
]

