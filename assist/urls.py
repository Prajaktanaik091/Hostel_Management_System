"""
URL configuration for assist project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from home.views import Home,  roomate_search, updates, menu_checking, login_page, logout_page, register, room_photos,add_notice,delete_notice,update_form,complains,complains_check



urlpatterns = [
    path("", Home, name="home"),
    
    path("roomate_search/", roomate_search, name="roomate_search"),
    path("updates/", updates, name="updates"),
    path("menu_checking/", menu_checking, name="menu_checking"),
    path("login_page/", login_page, name="login_page"),
    path("logout_page/", logout_page, name="logout_page"),
    path("register/", register, name="register"),
    
    path('room_photos/', room_photos, name='room'),
    path('add_notice/', add_notice, name='add_notice'),
    path('update_form/', update_form, name='update_form'),
    path('delete_notice/', delete_notice, name='delete_notice'),
    path('complain/', complains, name='complains'),
    path('complains_check/', complains_check, name='complains_check'),
    path("admin/", admin.site.urls),
]
