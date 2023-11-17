"""
URL configuration for ac_control project.

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

from django.urls import path, include
# from django.conf.urls import url 这段代码已经过时，上面的re_path取代了之前版本的url
from user import views as user_views  # from user import是从Django/HelloWorld往下找
from manager import views as manager_views

# from ..user import是从当前文件位置

urlpatterns = [

    path('', include("user.urls")),
    path('manager/', include("manager.urls")),

]
