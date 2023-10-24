from django.db import models
from django.utils import timezone
import datetime


# Create your models here.

# 用户类
class User(models.Model):
    # 用户身份证号 主键
    user_id = models.CharField('user_id', primary_key=True, max_length=30)
    # 用户姓名
    user_name = models.CharField('user_name', max_length=20, null=False)
    # 用户性别
    # user_sex = models.CharField('user_sex', max_length=10, null=False)
    # 用户年龄
    user_age = models.IntegerField('user_age', null=False)

    # 入住时间 添加和修改时都会更新时间
    # 1.用户首次入住 2.用户入住期间续住 3.用户第二次或第n次入住
    # live_time = models.DateTimeField(auto_now=True)  # auto_now：在数据更新时自动更新时间
    # # 手机号码
    # user_phone = models.CharField('user_phone', max_length=20, null=False)
    # # 房间号
    # room_id = models.CharField('room_id', max_length=10)

    # 指定表名
    class Meta:
        db_table = 'User'


# 房间类
class Room(models.Model):
    # 主键 没什么含义
    operation_id = models.AutoField('operation_id', primary_key=True)
    # 房间号
    room_id = models.CharField('room_id', max_length=10)
    # 目前的用户
    user_id = models.CharField('user_id', max_length=30)
    # 房间空调的温度
    temp = models.IntegerField('温度', null=False)
    # 房间空调的风速
    wind_speed = models.IntegerField('wind_speed', null=False)  # 1-10代表风速
    # 开启时间
    open_time = models.DateTimeField()  # 可以为null
    # 关闭时间
    close_time = models.DateTimeField()  # 可以为null

    # 指定表名
    class Meta:
        db_table = 'Room'


# def create_example():
#     current_time = timezone.now()
#     rooms = [
#         Room(room_id='123', user_id='456', temp=25, wind_speed=3, open_time=timezone.now(),
#              close_time=current_time + datetime.timedelta(minutes=10)),
#         Room(room_id='789', user_id='012', temp=22, wind_speed=2, open_time=timezone.now(),
#              close_time=current_time + datetime.timedelta(minutes=20)),
#     ]
#     Room.objects.bulk_create(rooms)


def calculate_electricity_cost(room_records):
    # 获取该用户在该房间内的所有记录
    total_cost = 0.0
    for i in range(len(room_records)):
        record = room_records[i]
        # 计算使用时长
        duration = record.close_time - record.open_time
        # 计算电费（示例计算方法）
        electricity_cost = duration.total_seconds() * record.wind_speed * 0.001  # 假设电费计算公式为使用时长 * 风速 * 0.001
        total_cost += electricity_cost
    return total_cost
