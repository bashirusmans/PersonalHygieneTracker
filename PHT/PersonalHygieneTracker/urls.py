from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),
    path('update-user/', views.updateUser, name='update-user'),
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('category/<str:pk>/', views.category, name='category'),
    path('routine/<str:pk>/', views.routine, name='routine'),
    path('delete-category/<str:pk>/', views.deleteCategory, name='delete-category'),
    path('delete-routine/<str:pk>/', views.deleteRoutine, name='delete-routine'),
    path('profile/<str:pk>/', views.profile, name='profile'),
    path('add-category/', views.addCategory, name='add-category'),
    path('add-routine/<str:pk>', views.addRoutine, name='add-routine'),

]


