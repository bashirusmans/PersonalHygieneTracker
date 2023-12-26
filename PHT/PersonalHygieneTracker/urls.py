from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),
    path('update-user/', views.updateUser, name='update-user'),
    path('', views.home, name='home'),
    path('category/<str:pk>', views.category, name='category'),
]


