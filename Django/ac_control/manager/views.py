from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from manager import models
from threading import Timer
import datetime, time

from django.utils import timezone
from django.views import View
from threading import Timer
from user.models import Room

# import numpy as np

# Create your views here.
class Queue(View):
    room_list = []

    def insert(self, room, queue_type):
        room.state = queue_type
        room.scheduling_num += 1
        self.room_list.append(room)
        self.room_list.sort(key=lambda x: x.fan_speed)  # 按照风速排列
        return True

    def set_target_temp(self, room_id, target_temp):
        for room in self.room_list:
            if room.room_id == room_id:
                room.target_temp = target_temp
                break
        return True

    def set_fan_speed(self, room_id, fan_speed):
        for room in self.room_list:
            if room.room_id == room_id:
                room.fan_speed = fan_speed
                self.room_list.sort(key=lambda x: x.fan_speed)  # 按照风速排序，服务队列中风速优先
                break
        return True

    def delete(self, room):
        self.room_list.remove(room)
        return True

    def update_time(self, queue_type):
        for room in self.room_list:
            if room.state == queue_type:
                room.time += 1

        timer = Timer(60, lambda: self.update_time(queue_type))  # 每1min执行一次函数
        timer.start()

class ServingQueue(Queue):
    serving_num = 0
    queue_type = 1  # 1为服务状态
    def insert(self, room, queue_type=1):
        super().insert(room, queue_type=queue_type)
        self.serving_num += 1
        return True

    def delete(self, room):
        super().delete(room)
        self.serving_num -= 1
        return True

    def update_serve_time(self):
        super().update_time(queue_type=1)

class WaitingQueue(Queue):
    waiting_num = 0
    queue_type = 2  # 2为等待状态

    def insert(self, room, queue_type=2):
        super().insert(room, queue_type=queue_type)
        self.waiting_num += 1
        return True

    def delete(self, room):
        super().delete(room)
        self.waiting_num -= 1
        return True

    def update_waiting_time(self):
        super().update_time(queue_type=2)


class Scheduler(View):  # 在views里直接创建
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 在这里进行初始化操作
        self.high_temp = None
        self.low_temp = None
        self.h_rate_fee = None
        self.m_rate_fee = None
        self.l_rate_fee = None
        self.request_id = 1
        self.request_num = 0
        self.rooms = []  # 储存房间队列，最多有5个房间

        # 等待队列与服务队列
        self.SQ = ServingQueue()
        self.WQ = WaitingQueue()
    def get(self, request):
        '''
        获取前台传参
        主要有：温度范围，不同风速的费率
        各已在后面传参的时候给
        '''

    def set_para(self, high_temp, low_temp, h_rate_fee, m_rate_fee, l_rate_fee):
        self.high_temp = high_temp
        self.low_temp = low_temp
        self.h_rate_fee = h_rate_fee
        self.m_rate_fee = m_rate_fee
        self.l_rate_fee = l_rate_fee
        return True

    # 用户申请资源
    def request_on(self, room_id, current_temp):  # 用户开机时调用
        '''
        一个请求到来，第一次开机分配房间对象然后处理，否则直接处理
        调用调度算法
        问题：房间ID如何分配的
        开始计费和计温
        '''
        return_room = self.get_or_create_room(room_id, current_temp)

        if self.SQ.serving_num < 3:
            self.SQ.insert(return_room)  # 进入服务队列 state = 1
        else:
            self.WQ.insert(return_room)  # 进入等待队列 state = 2


        return_room.request_id = self.request_id
        self.request_id += 1
        return_room.operation = 3
        return_room.save(force_insert=True)  # 存入数据库

        return return_room

    # 判断请求如何实现
    def get_or_create_room(self, room_id, current_temp):
        for room in self.rooms:
            if room.room_id == room_id:
                room.current_temp = current_temp
                return room

        # 如果房间不存在，创建一个新的房间对象
        if len(self.rooms) < 5:  # 控制只能有五个房间开机
            new_room = Room(request_id=self.request_id, room_id=room_id, current_temp=current_temp)
            self.rooms.append(new_room)
            self.request_num += 1  # 发出第一次开机请求的房间数加一
            return new_room

        # 如果请求数超过了限制，返回 None 或者其他适当的值
        return None

    # 用户关机
    def request_off(self, room_id):  # 将指定房间状态设为3：关闭
        for room in self.SQ.room_list:
            if room.room_id == room_id:
                # 房间回到初始温度
                room.current_temp = room.init_temp  # 为什么房间直接回到初始温度？
                # 修改房间状态
                if room.state == 1:  # 服务队列中
                    room.state = 3
                    self.SQ.delete(room)
                if room.state == 2:  # 等待队列中
                    room.state = 3
                    self.WQ.delete(room)
                else:
                    room.state = 3
                # 写入数据库
                room.request_id = self.request_id
                self.request_id += 1
                room.operation = 4
                room.request_time = timezone.now()
                room.save(force_insert=True)

                # 开启资源充足的调度
                severing_num = len(self.SQ.room_list)
                i = 1
                for temp in self.WQ.room_list:
                    if i <= 3 - severing_num:
                        self.WQ.delete(temp)
                        self.SQ.insert(temp)
                    i += 1
                return room

   # 用户调温
    def change_target_temp(self, room_id, target_temp):
        if target_temp < 18:
            target_temp = 18
        if target_temp > 25:
            target_temp = 25
            for room in self.rooms:
                if room.room_id == room_id:
                    if room.state == 1:  # 在调度队列中
                        self.SQ.set_target_temp(room_id, target_temp)
                    elif room.state == 2:  # 在等待队列中
                        self.WQ.set_target_temp(room_id, target_temp)
                    else:
                        room.target_temp = target_temp

                        # 写入数据库
                        room.request_id = self.request_id
                        self.request_id += 1
                        room.operation = 1
                        room.request_time = timezone.now()
                        room.save(force_insert=True)

                        return room

  # 用户调整风速
    def change_fan_speed(self, room_id, fan_speed):
        """
        处理调风请求
        :param room_id:
        :param fan_speed:
        :return:
        """
        if fan_speed == 1:
            fee_rate = self.l_rate_fee # 低风速时的费率
        elif fan_speed == 2:
            fee_rate = self.m_rate_fee  # 中风速时的费率
        elif fan_speed == 1:
            fee_rate = self.h_rate_fee
        for room in self.rooms:
            if room.room_id == room_id:
                if room.state == 1:  # 在调度队列中
                    self.SQ.set_fan_speed(room_id, fan_speed)
                elif room.state == 2:  # 在等待队列中
                    self.WQ.set_fan_speed(room_id, fan_speed)
                else:
                    room.fan_speed = fan_speed
                # 写入数据库
                room.request_id = self.request_id
                self.request_id += 1
                room.operation = 2
                room.request_time = timezone.now()
                room.save(force_insert=True)

                return room

  # 用户开关机更新房间状态
    def update_room_state(self, room_id):
        '''
        1
        '''
    def check_room_state(self):
        '''
        用于管理员检测房间状态
        '''

    def scheduling(self):
        # 资源足够的情况
        if len(self.WQ.room_list) != 0 and len(self.SQ.room_list) < 3:
            severing_num = len(self.SQ.room_list)
            i = 1
            for room in self.WQ.room_list:  # 遍历等待队列，将等待中的房间插入服务队列
                if i <= 3 - severing_num:
                    self.WQ.delete(room)
                    self.SQ.insert(room)
                i += 1

        # 资源不足的情况
        elif len(self.WQ.room_list) != 0 and len(self.SQ.room_list) == 3:
            request_room = self.WQ.room_list[0]

            # 优先级调度启动
            available_room1 = [room for room in self.SQ.room_list if room.fan_speed < request_room.fan_speed]
            # 时间片调度启动
            available_room2 = [room for room in self.SQ.room_list if room.fan_speed == request_room.fan_speed]
            if available_room1:
                self.priority_scheduling(available_room1, request_room)  # 优先级调度
            elif available_room2:
                self.time_slice_scheduling(request_room)  # 时间片轮询调度
            else:
                if len(self.SQ.room_list) >= 3:
                    self.WQ.insert(request_room)
                else:
                    self.SQ.insert(request_room)
                    request_room.wait_time = 0  # 分配等待服务时长

    # 优先级调度
    def priority_scheduling(self, rooms, request_room):
        '''
        优先级调度
        '''
        # 找出风速最小的房间
        min_fan_speed = min(rooms, key=lambda x: x.fan_speed).fan_speed
        min_fan_speed_rooms = list(filter(lambda x: x.fan_speed == min_fan_speed, rooms))
        # 按服务时间对房间进行排序
        sorted_rooms = sorted(min_fan_speed_rooms, key=lambda x: x.serve_time, reverse=True)
        self.SQ.delete(sorted_rooms[0])
        self.WQ.insert(sorted_rooms[0])
        sorted_rooms[0].wait_time = 0     # 等待与服务时间的分配与用处  ？？？？？?
        self.SQ.insert(request_room)
        request_room.sever_time = 0

    # 时间片调度
    def time_slice_scheduling(self, request_room):
        clock = 120

        #  奇奇怪怪 是要每一个房间都分配一个服务时间好像
        # 不太对

        while clock != 0:
            if self.check_condition():
                min_wait_serve_time_room = min(self.WQ.room_list, key=lambda x: x.wait_serve_time)
                self.WQ.delete(min_wait_serve_time_room)
                self.SQ.insert(min_wait_serve_time_room)
                min_wait_serve_time_room.wait_time = 0
                break

            else:
                clock -= 1
            time.sleep(1)

        # 判断是如何跳出循环的
        if clock <= 0:
            # 没有服务状态变化，释放服务队列中服务时长最大的服务对象
            max_serve_time_room = max(self.SQ.room_list, key=lambda x: x.serve_time)
            self.SQ.delete(max_serve_time_room)
            self.WQ.insert(max_serve_time_room)
            self.SQ.insert(request_room)
            request_room.serve_time = 0
            max_serve_time_room.wait_time = 0  # 分配等待服务时长


    def check_condition(self):  # 时间片轮转跳出条件
        if any(self.check_target_arrive or room.state == 3 for room in self.SQ.room_list):  # 还没实现达到温度与关机函数
            return True

    def check_target_arrive(self):  # 检查达到目标温度与否
        if len(self.SQ.room_list) != 0:
            for room in self.SQ.room_list:
                if abs(room.current_temp - room.target_temp) < 0.1 or room.current_temp < room.target_temp:
                    room.state = 4
                    self.SQ.delete(room)
                    # 后面要启动回温 未实现
                    return True

def login(request):
    return render(request, 'manager_login.html')



# ===============类================
class RoomCounter:  # 分配房间号
    num = 0
    dic = {}


class RoomInfo:  # Room->字典
    dic = {
        "target_temp": "--",
        "init_temp": "--",
        "current_temp": "--",
        "fan_speed": "--",
        "fee": 0,
        "room_id": 0
    }

    def __init__(self, room):
        self.dic["target_temp"] = room.target_temp
        self.dic["init_temp"] = room.init_temp
        self.dic["current_temp"] = int(room.current_temp)
        self.dic["fan_speed"] = speed_ch[room.fan_speed]
        self.dic["fee"] = int(room.fee)
        self.dic["room_id"] = room.room_id


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


class ChartData:
    open_time = []  # 五个房间的开机时长
    record_num = 0  # 详单数
    schedule_num = 0  # 调度次数
    open_num = []  # 五个房间的*开机次数*
    change_temp_num = []  # 五个房间的调温次数
    change_fan_num = []  # 五个房间的调风速次数
    # ---numpy---
    # fee = np.zeros([6, 30])  # 五个房间，30分钟内费用 + 30分钟内总费用


# ============静态变量===========
room_c = RoomCounter  # 静态
room_info = RoomInfo
scheduler = Scheduler()  # 属于model模块
room_b = RoomBuffer
speed_ch = ["", "高速", "中速", "低速"]
state_ch = ["", "服务中", "等待", "关机", "休眠"]


# ===============================


# ================函数 <顾客界面>  ==============
def get_room_id(request):
    s_id = request.session.session_key
    if s_id is None:
        request.session.create()
        s_id = request.session.session_key

    if s_id not in room_c.dic:
        room_c.num = room_c.num + 1
        room_c.dic[s_id] = room_c.num
        return room_c.num
    else:
        return room_c.dic[s_id]


def client_off(request):  # 第一次访问客户端界面、开机
    room_id = get_room_id(request)
    room = scheduler.update_room_state(room_id)
    if room:  # -----------之所以要判断，是因为第一次访问页面，room有未创建的风险
        return render(request, 'client-off.html', RoomInfo(room).dic)
    else:  # 妹有room实例
        return render(request, 'client-off.html', room_info.dic)


def client_on(request):
    room_id = get_room_id(request)
    room = scheduler.update_room_state(room_id)
    return render(request, 'client-on.html', RoomInfo(room).dic)


def power(request):  # 客户端-电源键
    room_id = get_room_id(request)
    if not room_b.on_flag[room_id]:
        room_b.on_flag[room_id] = True  # 开机
        scheduler.request_on(room_id, room_b.init_temp[room_id])  # 创建room对象
        scheduler.set_init_temp(room_id, room_b.init_temp[room_id])  # 这里初始温度，和requeston的温度一样，如何简化？
        return HttpResponseRedirect('/on/')
    else:
        room_b.on_flag[room_id] = False  # 关机
        scheduler.request_off(room_id)
        return HttpResponseRedirect('/')


def change_high(request):  # 高速
    room_id = get_room_id(request)
    if room_b.on_flag[room_id]:
        scheduler.change_fan_speed(room_id, 1)
        return HttpResponseRedirect('/on/')
    else:
        return HttpResponseRedirect('/')


def change_mid(request):  # 中速
    room_id = get_room_id(request)
    if room_b.on_flag[room_id]:
        scheduler.change_fan_speed(room_id, 2)
        return HttpResponseRedirect('/on/')
    else:
        return HttpResponseRedirect('/')


def change_low(request):  # 低速
    room_id = get_room_id(request)
    if room_b.on_flag[room_id]:
        scheduler.change_fan_speed(room_id, 3)
        return HttpResponseRedirect('/on/')
    else:
        return HttpResponseRedirect('/')


def change_up(request):  # 升温
    room_id = get_room_id(request)
    if room_b.on_flag[room_id]:  # 这里target_temp如何保证和内核同步？
        temperature = room_b.target_temp[room_id] + 1
        room_b.target_temp[room_id] = temperature
        scheduler.change_target_temp(room_id, temperature)
        return HttpResponseRedirect('/on/')
    else:
        return HttpResponseRedirect('/')


def change_down(request):  # 降温
    room_id = get_room_id(request)
    if room_b.on_flag[room_id]:
        temperature = room_b.target_temp[room_id] - 1
        room_b.target_temp[room_id] = temperature
        scheduler.change_target_temp(room_id, temperature)
        return HttpResponseRedirect('/on/')
    else:
        return HttpResponseRedirect('/')


