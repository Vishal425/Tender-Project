"""tender URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from  tender_app import views
# from tender_app import scrap
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView,LogoutView
# from django.conf.urls import url

urlpatterns = [

    path('admin/', admin.site.urls),
    # path('show/',views.show),
    path('show/',views.show, name='keyword'),
    path('index', views.show, name = 'index'),
    #search 
    #  path('results/',SearchView.as_view(), name='search'),
    path('show/search', views.search, name='search'),

    path('demo',views.indexView,name="home"),
    path('dashboard/',views.dashboardView,name="dashboard"),
    path('login/',LoginView.as_view(),name="login_url"),
    path('register/',views.registerView,name="register_url"),
    path('logout/',views.logout,name="logout"),
    path('',views.demo,name="demo"),
    path('base',views.base,name="base"),
    path('sample',views.sample,name="sam")
]
