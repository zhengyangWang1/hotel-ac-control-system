
from django.urls import path
# from django.conf.urls import url 这段代码已经过时，上面的re_path取代了之前版本的url
from manager import views
import user

# from ..user import是从当前文件位置
app_name='manager'
urlpatterns = [
    # 管理员端
    path('', views.login),
    path('register_manager/',views.registration_manager,name='register_manager'),
    path('login_manager/',views.login_manager,name='login_manager'),
    path('monitor/',user.views.Reports.get_current_report),

    # path('register_manager/',views.registration_manager),
    # path('login_manager/',views.login_manager),

    path('front/',user.views.Reports.front),
    path('download/',user.views.Reports.download_file),
]
