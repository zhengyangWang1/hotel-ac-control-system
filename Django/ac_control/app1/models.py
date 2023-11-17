from django.db import models


# Create your models here.

# 用户类
class User(models.Model):
    # 用户身份证号 主键
    user_id = models.CharField('user_id', primary_key=True, max_length=30)
    # 用户姓名
    # user_name = models.CharField('user_name', max_length=20, null=False)
    # 用户性别
    # user_sex = models.CharField('user_sex', max_length=10, null=False)
    # 用户年龄
    # user_age = models.IntegerField('user_age', null=False)

    # 入住时间 添加和修改时都会更新时间
    # 1.用户首次入住 2.用户入住期间续住 3.用户第二次或第n次入住
    # live_time = models.DateTimeField(auto_now=True)  # auto_now：在数据更新时自动更新时间
    # # 手机号码
    # user_phone = models.CharField('user_phone', max_length=20, null=False)
    # 房间号
    room_id = models.CharField('room_id', max_length=10)
    # 密码
    password = models.CharField('password', max_length=30)

    # 指定表名
    class Meta:
        db_table = 'User'


# 储存所有房间的每个请求
class Room(models.Model):
    # 请求号 主键 默认自增
    request_id = models.AutoField('operation_id', primary_key=True)
    # 房间号
    room_id = models.CharField('room_id', max_length=10)
    # 目前的用户
    user_id = models.CharField('user_id', max_length=30)
    # 房间空调的温度
    temp = models.IntegerField('温度', null=False)
    # 房间空调的风速
    wind_speed = models.IntegerField('wind_speed', null=False)  # 1-10代表风速
    # 开启时间
    open_time = models.DateTimeField(null=True, blank=True)  # 可以为null
    # 关闭时间
    close_time = models.DateTimeField(null=True, blank=True)  # 可以为null
    # 调整参数
    change_time = models.DateTimeField(null=True, blank=True)  # 可以为null

    # 指定表名
    class Meta:
        db_table = 'Room'


# 储存每个房间的空调状态
class AirCondition(models.Model):
    # 房间号 主键
    room_id = models.CharField('room_id', max_length=10, primary_key=True)
    # 用户id
    user_id = models.CharField('user_id', max_length=20, null=False)
    # 房间空调的温度
    temp = models.IntegerField('温度', null=False)
    # 房间空调的风速
    wind_speed = models.IntegerField('wind_speed', null=False)  # 1-10代表风速

    class Meta:
        db_table = 'AirCondition'



