from django.db import models
from django.utils import timezone

from threading import Timer
import time
import django
from datetime import datetime
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
    # 入住日期
    begin_date = models.DateField('begin_date', max_length=30, auto_now=True)  # 在用户入住时修改 是否需要时间
    # 退房日期
    out_date = models.DateTimeField('out_date', max_length=30, auto_now=True)  # 在用户退房时修改

    # 指定表名
    class Meta:
        db_table = 'User'

# 储存所有房间的每个请求  详单表

class Room(models.Model):
    # 风速范围
    FAN_SPEED = [
        (3, "HIGH"),
        (2, "MIDDLE"),
        (1, "LOW"),
    ]
    # 房间状态
    ROOM_STATE = [
        (1, "SERVING"),
        (2, "WAITING"),
        (3, "SHUTDOWN"),
        (4, "BACKING")  # 休眠
    ]
    # 新的详单记录产生条件
    OPERATION_CHOICE = [
        (1, '调温'),
        (2, '调风'),
        (3, '开机'),
        (4, '关机')
    ]

    # 请求号 主键 默认自增
    request_id = models.AutoField('operation_id', primary_key=True)
    # 请求时间
    request_time = models.DateTimeField(verbose_name="请求发出时间", null=True)
    # 服务开始时间
    sever_begin_time = models.DateTimeField(verbose_name="服务开始时间", null=True)
    # 服务结束时间
    sever_over_time = models.DateTimeField(verbose_name="服务结束时间", null=True)
    # 当前服务时长
    serve_time = models.IntegerField(verbose_name='当前服务时长', default=0)
    # 当前等待时长
    wait_time = models.IntegerField(verbose_name='当前等待时长', default=0)
    # 房间号
    room_id = models.CharField('room_id', max_length=10)
    # 目前的用户
    user_id = models.CharField('user_id', max_length=30, null=True)
    # 初始温度
    init_temp = models.IntegerField('初始温度', null=False, default=22.0)
    # 当前温度
    current_temp = models.IntegerField('当前温度', null=False, default=26.0)
    # 目标温度
    target_temp = models.IntegerField('目标温度', null=False, default=22.0)
    # 房间空调的风速
    fan_speed = models.IntegerField(verbose_name='风速', choices=FAN_SPEED, default=2)
    # 房间状态
    state = models.IntegerField(verbose_name='服务状态', choices=ROOM_STATE, default=3)
    # 操作类型
    operation = models.IntegerField(verbose_name='操作类型', choices=OPERATION_CHOICE, default=0)
    # 调度次数
    scheduling_num = models.IntegerField(verbose_name='调度次数', default=0)
    # 费用
    fee = models.FloatField(verbose_name='费用', default=0.0)
    # 费率
    fee_rate = models.FloatField(verbose_name='费率', default=0.0)

    # 指定表名
    class Meta:
        db_table = 'Room'





# python manage.py makemigrations
# python manage.py migrate