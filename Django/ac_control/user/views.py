from django.http import HttpResponse
from django.shortcuts import render, redirect
from user import models
import datetime


# Create your views here.

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
            context = {'room_id': room_id,'user_id':user_id,'cost': 0,'sum_cost': 0,'cur_tem':"not set",'cur_wind':"not set"}
            # 如果用户名和密码匹配，登录成功，返回包含JavaScript的页面
            return render(request, 'tem_c2.html', context)

        except models.User.DoesNotExist:
            # 如果用户不存在或密码不匹配，返回登录页面或其他提示页面
            return render(request, 'login.html')

    return render(request, 'login.html')


def login(request):
    return render(request, 'login.html')


# 用户点击开机
def open_ac(request):  # 把该房间信息添加到数据库
    """获取request中的用户信息和空调数据"""
    user_id = request.POST.get('user_id')
    room_id = request.POST.get('room_id')
    # temp = request.POST.get('temp')
    # wind_speed = request.POST.get('wind_speed')
    # 在AirCondition中添加一条空调信息，用户id和房间号由前端request传入，空调温度和风速为默认值
    models.AirCondition.objects.create(user_id=user_id, room_id=room_id, temp=26, wind_speed=5)  # 待添加
    # 在Room中添加一条操作信息，表明空调已经开启
    models.Room.objects.create(room_id=room_id, user_id=user_id, temp=26, wind_speed=5,
                               open_time=datetime.datetime.now())
    return render(request, 'ac.html')


# 用户点击关机
def close_ac(request):
    """把room对象从room_list中移除"""
    user_id = request.POST.get('user_id')
    room_id = request.POST.get('room_id')
    temp = request.POST.get('temp')
    wind_speed = request.POST.get('wind_speed')
    # 将AirCondition中将该房间空调的信息删去
    models.AirCondition.objects.filter(room_id=room_id).delete()
    # 在Room中添加一条操作信息，表明空调已经关闭
    models.Room.objects.create(room_id=room_id, user_id=user_id, temp=temp, wind_speed=wind_speed,
                               close_time=datetime.datetime.now())
    return render(request, '关机后显示已关机')


# 用户设定好温度和风速后点击确定
def change_temp_wind(request):
    user_id = request.POST.get('user_id')
    room_id = request.POST.get('room_id')
    temp = request.POST.get('temp')
    wind_speed = request.POST.get('wind_speed')
    # 更改AirCondition中空调的参数
    ac = models.AirCondition.objects.get(room_id=room_id)
    ac.temp = temp
    ac.wind_speed = wind_speed
    ac.save()
    # 在Room中添加一条操作，表明更改后的空调参数
    models.Room.objects.create(room_id=room_id, user_id=user_id, temp=temp, wind_speed=wind_speed,
                               change_time=datetime.datetime.now())
    return render(request, '显示更改成功')


   