from django.http import HttpResponse
from django.shortcuts import render, redirect
from user import models
import datetime
from manager.views import Scheduler
from django.http import JsonResponse

# Create your views here.

scheduler = Scheduler()  # 创建一个调度器


def register(request):
    if request.method == 'POST':
        room_id = request.POST.get('roomNumber')
        user_id = request.POST.get('username')
        password = request.POST.get('password')
        models.User.objects.create(user_id=user_id, room_id=room_id, password=password)
        return render(request, 'login.html')


def login_room(request):
    if request.method == 'POST':
        room_id = request.POST.get('roomNumber')
        user_id = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = models.User.objects.get(room_id=room_id, user_id=user_id, password=password)
            context = {'room_id': room_id, 'user_id': user_id, 'cost': 0, 'sum_cost': 0, 'cur_tem': "not set",
                       'cur_wind': "not set"}
            # 如果用户名和密码匹配，登录成功，返回包含JavaScript的页面
            return render(request, 'tem_c2.html', context)

        except models.User.DoesNotExist:
            # 如果用户不存在或密码不匹配，返回登录页面或其他提示页面
            return render(request, 'login.html', '登陆失败')

    return render(request, 'login.html')


def login(request):
    return render(request, 'login.html')


# 用户点击开机
def open_ac(request):  # 在点击开启空调后执行： 加入调度队列-->判断调度状态-->如果进入服务队列，开启空调
    # -->如果需要等待资源，显示等候中
    """获取request中的用户信息和空调数据"""

    room_id = request.POST.get('room_id')
    room = scheduler.request_on(room_id, 26)  # 加入调度队列，返回一个房间对象，包含状态（1：服务，2：等待）

    if room.state == 1:
        # 打开空调
        room_state = '开启'
    else:
        # 等待资源中
        room_state = '等待'

    context = {'room_state': room_state}
    return render(request, 'tem_c2.html', context)


# 如果空调为等待状态，需要一个函数，监控空调状态，当状态变为服务时，将其加入服务队列，同时将前端状态相应改变
def change_ac_state(request):
    room_id = request.POST.get('room_id')
    room = models.Room.objects.get(room_id=room_id)
    new_state = room.state  # 获取当前房间状态
    return JsonResponse({'room_id': room_id, 'new_state': new_state})


# 用户点击关机
def close_ac(request):
    """把room对象从room_list中移除"""
    room_id = request.POST.get('room_id')
    room = scheduler.request_off(room_id)
    room_state = '关机'
    context = {'room_state': room_state}
    return render(request, 'tem_c2.html', context)


# 用户设定好温度和风速后点击确定
def change_temp_wind(request):
    room_id = request.POST.get('room_id')
    temp = request.POST.get('temp')
    wind_speed = request.POST.get('wind_speed')
    # 更改AirCondition中空调的参数
    ac = models.AirCondition.objects.get(room_id=room_id)
    ac.temp = temp
    ac.wind_speed = wind_speed
    ac.save()  # 更新room表中的信息
    return render(request, 'tem_c2.html')
