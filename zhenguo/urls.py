"""zhenguo URL Configuration

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
from user.views import *
from good.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from django.conf.urls import url
from .settings import *
from django.views import static

urlpatterns = [
	path('user/login/', login, name='login'),
	path('user/register/', register, name='register'),
	path('user/email/', email, name='email'),
	path('user/logout/', logout, name='logout'),
	path('user/uploadimg/', uploadimg, name='uploadimg'),

 	path('good/uploadimg/', upload, name='upload'),
	path('category/', getcategory, name='category'),
    path('admin/', admin.site.urls),
	url(r'^img/(?P<path>.*)$', static.serve,{'document_root': settings.MEDIA_ROOT})
]