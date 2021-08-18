from django.urls import path
from django.urls.conf import include
from account import views

urlpatterns = [
    path('logout/', views.logoutUser),
    path('login/', views.loginUser),
    path('signup/', views.signup),
    path('reset-password/', views.resetPass),
    
]
