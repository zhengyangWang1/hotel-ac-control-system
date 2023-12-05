from django.urls import path
# from django.conf.urls import url 这段代码已经过时，上面的re_path取代了之前版本的url
from manager import views

# from ..user import是从当前文件位置

urlpatterns = [

    # 管理员端
    path('', views.login),

]
