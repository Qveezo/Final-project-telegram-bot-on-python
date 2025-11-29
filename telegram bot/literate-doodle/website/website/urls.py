"""
URL configuration for website project.

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

from mathbot_site import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_page),
    path('commands/', views.commands_page, name='bot_cmd'),
    path('payment/', views.payment_page, name='pay'),
    path('about/', views.about_page, name='about_us'),
    path('bot/', views.bot_page, name='about_bot'),
]
