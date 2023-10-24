"""
URL configuration for hotel project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
# from django.contrib import admin
# from django.urls import path
#
# urlpatterns = [
#     path("admin/", admin.site.urls),
# ]

from django.urls import path
# from django.conf.urls import url 这段代码已经过时，上面的re_path取代了之前版本的url
from app1 import views

# from ..app1 import是从当前文件位置

urlpatterns = [
    # path('hello/', views.hello),

    # www.xxx.com/index/
    path('something/', views.something),

    path('login/', views.login),

    path('add_user/', views.add_user),

    path('form/<int:user_id>/<int:room_id>/', views.create_form, name='create_form'),

    path('registration', views.registration)
]