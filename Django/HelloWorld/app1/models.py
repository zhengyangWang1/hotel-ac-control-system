from django.db import models


# Create your models here.

# 用户类
class User(models.Model):
    # 用户身份证号 主键
    user_id = models.CharField('user_id', primary_key=True, max_length=30)
    # 用户姓名
    user_name = models.CharField('user_name', max_length=20, null=False)
    # 用户性别
    user_sex = models.CharField('user_sex', max_length=10, null=False)
    # 用户年龄
    user_age = models.IntegerField('user_age', null=False)
    # 入住时间 添加和修改时都会更新时间
    # 1.用户首次入住 2.用户入住期间续住 3.用户第二次或第n次入住
    live_time = models.DateTimeField(auto_now=True)
    # 手机号码
    user_phone = models.CharField('user_phone', max_length=20, null=False)


# 房间类
class Room(models.Model):
    # 房间号 主键
    room_id = models.CharField('room_id', primary_key=True, max_length=10)
    # 房间空调的温度
    temp = models.IntegerField('温度', null=False)
    # 房间空调的风速
    wind_speed = models.CharField('wind_speed', max_length=10)
