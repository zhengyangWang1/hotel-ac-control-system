from django.urls import path
# from django.conf.urls import url 这段代码已经过时，上面的re_path取代了之前版本的url
from user import views  # from user import是从Django/HelloWorld往下找

# from ..user import是从当前文件位置

urlpatterns = [
    # 用户端
    path('', views.login, name='login'),  # 将根路径映射到登录页面
    path('login/', views.login),
    path('login_room/', views.login_room, name='login_room'),
    path('register/', views.register, name='register'),
    path('open_ac/', views.open_ac, name='open_ac'),
    path('change_ac_state/', views.change_ac_state, name='change_ac_state'),
    path('change_temp_wind/', views.change_temp_wind, name='change_temp_wind'),
    path('close_ac/', views.close_ac, name='close_ac'),

]
