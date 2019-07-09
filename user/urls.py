from django.urls import path
from .views import *

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register_url'),
    path('login/', UserLoginView.as_view(), name='login_url')
]
