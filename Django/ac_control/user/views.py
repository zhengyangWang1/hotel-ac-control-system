from django.shortcuts import render, redirect, HttpResponseRedirect
from user import models
import datetime
from manager.views import Scheduler
from django.http import JsonResponse
from user.models import Room
from user.models import User
from django.db import models
from django.utils import timezone
from django.db.models import Sum
from datetime import timedelta
# from dateutil.relativedelta import relativedelta
import csv
import os
import json


# Create your views here.
class RoomsInfo:  # 监控器使用
    def __init__(self, rooms):
        self.dic = {
            "room_id": [0],
            "state": [""],
            "fan_speed": [""],
            "current_temp": [0],
            "fee": [0],
            "target_temp": [0],
            "fee_rate": [0]
        }
        if rooms:
            for room in rooms:  # 从1号房开始
                self.dic["room_id"].append(room.room_id)
                self.dic["state"].append(state_ch[room.state])
                self.dic["fan_speed"].append(speed_ch[room.fan_speed])
                self.dic["current_temp"].append('%.2f' % room.current_temp)
                self.dic["fee"].append('%.2f' % room.fee)
                self.dic["target_temp"].append(room.target_temp)
                self.dic["fee_rate"].append(room.fee_rate)


class RoomBuffer:  # 房间数据缓存
    on_flag = [None, False, False, False, False, False]
    target_temp = [0, 25, 25, 25, 25, 25]  # 不要用数组。。。。
    init_temp = [0, 32, 28, 30, 29, 35]


# ============静态变量===========
room_b = RoomBuffer
speed_ch = ["", "高速", "中速", "低速"]
state_ch = ["", "服务中", "等待", "关机", "休眠"]

# ===========暂时直接执行，需要时通过管理员执行===========
scheduler = Scheduler()  # 创建一个调度器

high = 25
low = 18
default = 24
fee_h = 0.0016
fee_l = 0.0016
fee_m = 0.0016
scheduler.set_para(high, low, default, fee_h, fee_l, fee_m)
scheduler.power_on()
scheduler.start_up()


# ============客户===========
def register(request):
    if request.method == 'POST':
        room_id = request.POST.get('roomNumber')
        user_id = request.POST.get('username')
        password = request.POST.get('password')
        User.objects.create(user_id=user_id, room_id=room_id, password=password)
        return render(request, 'login.html')


def login_room(request):
    if request.method == 'POST':
        room_id = request.POST.get('roomNumber')
        user_id = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(room_id=room_id, user_id=user_id, password=password)
            context = {'room_id': room_id, 'user_id': user_id, 'cost': 0, 'sum_cost': 0, 'cur_tem': "not set",
                       'cur_wind': "not set"}
            # 如果用户名和密码匹配，登录成功，返回包含JavaScript的页面
            return render(request, 'tem_c2.html', context)

        except User.DoesNotExist:
            # 如果用户不存在或密码不匹配，返回登录页面或其他提示页面
            return JsonResponse('登陆失败')

    return render(request, 'login.html')


def login(request):
    return render(request, 'login.html')


# 用户点击开机
def open_ac(request):  # 在点击开启空调后执行： 加入调度队列-->判断调度状态-->如果进入服务队列，开启空调
    # -->如果需要等待资源，显示等候中
    """获取request中的用户信息和空调数据"""

    room_id = request.POST.get('room_id')
    user_id = request.POST.get('user_id')
    room = scheduler.request_on(room_id, user_id, default)  # 加入调度队列，返回一个房间对象，包含状态（1：服务，2：等待）
    if room.state == 1:
        # 打开空调
        room_state = '开启'
    else:
        # 等待资源中
        room_state = '等待'

    context = {'room_state': room_state}
    return JsonResponse(context)


# 如果空调为等待状态，需要一个函数，监控空调状态，当状态变为服务时，将其加入服务队列，同时将前端状态相应改变
def change_ac_state(request):
    # room_id = request.POST.get('room_id')
    json_data = json.loads(request.body)
    # 从 JSON 数据中获取 room_id
    room_id = json_data.get('room_id')

    # room = Room.objects.get(room_id=room_id)
    # room = Room.objects.filter(room_id=room_id).order_by('-request_time')[0]  # 因为是从数据库找的room，所以费用不更新

    # 从rooms中找
    rooms = scheduler.rooms
    for r in rooms:
        print('rooms中得到的room_id:', r.room_id, '，数据类型：', type(r.room_id))  # str类型
        print('从前端获得的room_id:', room_id, '，数据类型：', type(room_id))  # int类型
        if int(r.room_id) == room_id:
            print('找到room啦')
            room = r

    if room.state == 1:
        new_state = '开启'
    elif room.state == 2:
        new_state = '等待'
    elif room.state == 3:
        new_state = '关机'
    else:
        new_state = '休眠'
    if room.fan_speed == 1:
        wind = '低风'
    elif room.fan_speed == 2:
        wind = '中风'
    else:
        wind = '高风'
    temp = room.current_temp
    cost = room.fee  # !只有一个费用

    return JsonResponse({'cur_tem': temp, 'cur_wind': wind, 'cost': cost, 'sum_cost': cost, 'ac_status': new_state})


# 用户点击关机
def close_ac(request):
    """把room对象从room_list中移除"""
    room_id = request.POST.get('room_id')
    room = scheduler.request_off(room_id)
    room_state = '关机'
    context = {'room_state': room_state}
    return JsonResponse(context)


# 用户设定好温度和风速后点击确定
def change_temp_wind(request):
    room_id = request.POST.get('room_id')
    temp = int(request.POST.get('temperature'))  # 前端传来时为str，需要转化为int
    wind_speed = int(request.POST.get('fan_speed'))
    # 更新参数
    scheduler.change_target_temp(room_id, temp)  # 改变room的target_temp属性，写入数据库
    scheduler.change_fan_speed(room_id, wind_speed)  # 改变room的fan_speed属性，写入数据库
    return JsonResponse({'status': 'success'})


# ============管理员===========
def init(request):
    return render(request, 'init.html')


def init_submit(request):
    request.encoding = 'utf-8'
    high = int(request.GET['high'])
    low = int(request.GET['low'])
    default = int(request.GET['default'])
    fee_h = float(request.GET['fee_h'])
    fee_m = float(request.GET['fee_m'])
    fee_l = float(request.GET['fee_l'])
    for i in range(1, 6):
        room_b.init_temp[i] = int(request.GET['r' + str(i)])

    print(room_b.init_temp)
    scheduler.set_para(high, low, default, fee_h, fee_l, fee_m)
    scheduler.power_on()
    scheduler.start_up()
    return HttpResponseRedirect('/monitor')


def monitor(request):
    rooms = scheduler.check_room_state()
    print(rooms)
    return render(request, 'monitor.html', RoomsInfo(rooms).dic)


class Bills:
    @staticmethod
    def get_time(user_id, room_id):
        # 防止一个用户一次性订多个房间，需要房间号信息
        user_entry_exit = User.objects.filter(user_id=user_id, room_id=room_id).first()
        if user_entry_exit:
            return user_entry_exit.begin_date, user_entry_exit.out_date
        else:
            return None, None

    @staticmethod
    def cal_fee(start_time, end_time, room_id):
        '''
        找到当前费用和累计费用
        当前费用的理解是：从每次更新详单记录的时刻开始到现在，计算当前费用
        而非每次开关机
        '''
        # -表示降序排列，找到最新的房间记录
        # 这里有点问题，我们的数据库应该是只有一个fee，会累加更新，所以最新一条即为空调累计费用，不存在段费用 ？？？？？？
        records = Room.objects.filter(room_id=room_id).order_by('-request_time')
        if records:
            current_fee = records.first().fee
            history_fee = \
                Room.objects.filter(room_id=room_id, request_time__range=(start_time, end_time)).aggregate(Sum('fee'))[
                    'fee__sum']
            return current_fee, history_fee
        else:
            # 防止Attribute Error
            return 0, 0

    @staticmethod
    # 这个界面前面实现了在change_ac_state里，应该不用再实现了
    def current_status_return(request, user_id, room_id):
        '''
        交互————用户登录后的页面
        '''
        current_record = Room.objects.filter(room_id=room_id).order_by('-request_time').first()
        if current_record:
            status = {}
            status['current_temp'] = current_record.current_temp
            status['current_speed'] = current_record.fan_speed
            status['target_temp'] = current_record.target_temp
            start_time, end_time = Bills.get_time(user_id, room_id)
            status['current_fee'], status['history_fee'] = Bills.cal_fee(start_time, end_time, room_id)
        else:
            # 不知道有没有必要写
            status = {}
            status['current_temp'] = 26
            status['current_speed'] = 0
            status['target_temp'] = 26
            status['current_fee'] = 0
            status['history_fee'] = 0
        return render(request, 'tem_c2.html', {'current_status': status})

    @staticmethod
    def get_bill(user_id, room_id):
        start_time, end_time = Bills.get_time(user_id, room_id)
        _, total_fee = Bills.cal_fee(start_time, end_time, room_id)
        return total_fee

    @staticmethod
    def get_details(user_id, room_id):
        detail = {}
        start_time, end_time = Bills.get_time(user_id, room_id)
        records = Room.objects.filter(room_id=room_id, request_time__range=(start_time, end_time)).order_by(
            '-request_time')
        detail = []
        for r in records:
            dic = {}
            dic.update(
                request_id=r.request_id,
                request_time=r.request_time,
                room_id=r.room_id,
                operation=r.get_operation_display(),
                current_temp=r.current_temp,
                target_temp=r.target_temp,
                fan_speed=r.get_fan_speed_display(),
                fee=r.fee)
            detail.appned(dic)

        for d in detail:
            print(d)
        return detail

    @staticmethod
    def print_details(user_id, room_id):
        """
        打印详单
        :param room_id: 房间号
        :param begin_date: 起始日期
        :param end_date: endDay
        :return:    返回详单字典列表
        """
        rdr = Bills.get_details(user_id, room_id)
        import csv
        # 文件头，一般就是数据名
        file_header = ["request_id",
                       "request_time",
                       "room_id",
                       "operation",
                       "current_temp",
                       "target_temp",
                       "fan_speed",
                       "fee"]

        # 写入数据，如果没有文件夹就创建一个
        directory = "./details/"
        os.makedirs(directory, exist_ok=True)
        with open("./details/{}.csv".format(room_id), "w") as csvFile:
            writer = csv.DictWriter(csvFile, file_header)
            writer.writeheader()
            # 写入的内容都是以列表的形式传入函数
            for d in rdr:
                writer.writerow(d)
            csvFile.close()
        return


class Reports:
    @staticmethod
    def get_daily_report(request):
        '''
        交互————日报
        '''
        room_statistics = {}
        current_time = timezone.now()
        # 获取昨天的日期
        yesterday = current_time - timezone.timedelta(days=1)
        yesterday_start = timezone.datetime(yesterday.year, yesterday.month, yesterday.day, 0, 0, 0,
                                            tzinfo=timezone.utc)
        yesterday_end = timezone.datetime(yesterday.year, yesterday.month, yesterday.day, 23, 59, 59, 999999,
                                          tzinfo=timezone.utc)
        return render(request, 'xx.html', {room_statistics: Reports.get_report_list(yesterday_start, yesterday_end)})

    @staticmethod
    def get_weekly_report(request):
        '''
        交互————周报
        '''
        room_statistics = {}
        current_time = timezone.now()
        # 计算上一周周一零点
        last_monday = current_time - relativedelta(weekday=0, days=7, hour=0, minute=0, second=0, microsecond=0)
        # 计算本周末十二点
        this_weekend = current_time + relativedelta(weekday=6, hour=23, minute=59, second=59, microsecond=999999)
        return render(request, '', {room_statistics: Reports.get_report_list(last_monday, this_weekend)})

    @staticmethod
    def get_report_list(start_time, end_time):
        room_statistics = {}
        # 获取一天内的记录
        records = Room.objects.filter(request_time__range=(start_time, end_time))
        # 对每个房间的记录进行统计
        for record in records:
            room_id = record.room_id
            if room_id not in room_statistics:
                room_statistics[room_id] = {
                    'scheduling_count': 0,
                    'temperature_adjustment_count': 0,
                    'fan_speed_adjustment_count': 0,
                    'total_runtime': 0,
                    'total_waiting_time': 0,
                    'total_fee': 0.0,
                }
            # 统计调度次数、调温次数、调风速的次数
            room_statistics[room_id]['scheduling_count'] += 1
            if record.operation == 1:
                room_statistics[room_id]['temperature_adjustment_count'] += 1
            elif record.operation == 2:
                room_statistics[room_id]['fan_speed_adjustment_count'] += 1
            if record.state == 1:
                room_statistics[room_id]['total_runtime'] += record.serve_time
            room_statistics[room_id]['total_waiting_time'] += record.wait_time
            room_statistics[room_id]['total_fee'] += record.fee
            # 把服务时间和等待时间从秒（int）改成str
            for room, info in enumerate(room_statistics):
                info['total_run_time'] = str(timedelta(seconds=info['total_run_time']))
                info['total_waiting_time'] = str(timedelta(seconds=info['total_waiting_time']))
        print(room_statistics)
        return room_statistics

    @staticmethod
    def current_status(room_id):
        current_record = Room.objects.filter(room_id=room_id).order_by('-request_time').first()
        if current_record:
            status = {}
            status['cur_tem'] = current_record.current_temp
            status['air_condition']=current_record.state
            status['cur_wind'] = current_record.fan_speed
            status['target_tem'] = current_record.target_temp

        else:
            # 不知道有没有必要写
            status = {}
            status['cur_tem'] = 26
            status['air_condition'] = 0
            status['cur_wind']= 'not set'
            status['target_tem'] = 0
        return current_record

    @staticmethod
    def get_current_report(request):
        '''
        交互————管理员或前台监控
        缺少消费总金额计算
        消费总金额需要根据user_id->request time range->history fee
        但是可以显示当前消费金额
        '''
        all_room_ids = Room.objects.values_list('room_id', flat=True).distinct()
        home_status = {}
        # 打印所有房间号
        for room_id in all_room_ids:
            home_status[room_id] = Reports.current_status(room_id)
        return render(request, '', {'status': home_status})
