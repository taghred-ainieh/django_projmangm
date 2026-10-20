from django.urls import path,include
from . import views 
from django.contrib.auth import views as auth_views 
urlpatterns = [
    path('',include('django.contrib.auth.urls')),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('register/', views.Registerview.as_view(), name='regester'),
    path('edit_profile/', views.edit_profile, name='edit_profile')

]
