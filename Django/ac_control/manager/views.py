from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from manager import models
from threading import Timer
import datetime, time

from django.utils import timezone
from django.views import View
from threading import Timer
from user.models import Room

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
    def insert(self, room, queue_type):
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

    def insert(self, room, queue_type):
        super().insert(room, queue_type=queue_type)
        self.waiting_num += 1
        return True

    def delete(self, room):
        super().delete(room)
        self.waiting_num -= 1
        return True

    def update_waiting_time(self):
        super().update_time(queue_type=2)

# class ServingQueue(View):
#     room_list = []
#     serving_num = 0
#
#     def insert(self, room):
#         room.state = 1
#         room.scheduling_num += 1
#         self.room_list.append(room)
#         self.room_list.sort(key=lambda x: x.fan_speed)  # 按照风速排列
#         self.serving_num += 1
#         return True
#
#     def set_target_temp(self, room_id, target_temp):
#         for room in self.room_list:
#             if room.room_id == room_id:
#                 room.target_temp = target_temp
#                 break
#         return True
#
#     def set_fan_speed(self, room_id, fan_speed):
#         for room in self.room_list:
#             if room.room_id == room_id:
#                 room.fan_speed = fan_speed
#                 self.room_list.sort(key=lambda x: x.fan_speed)  # 按照风速排序，服务队列中风速优先
#                 break
#         return True
#
#     def delete(self, room):
#         self.room_list.remove(room)
#         self.serving_num -= 1
#         return True
#
#     def update_serve_time(self):
#         if self.serving_num != 0:
#             for room in self.room_list:
#                 room.serve_time += 1
#         timer = Timer(60, self.update_serve_time)  # 每1min执行一次函数
#         timer.start()
#
# class WaitingQueue(View):
#     room_list = []
#
#     waiting_num = 0
#
#     def Insert(self, room):
#         room.state = 2
#         room.scheduling_num += 1
#         self.room_list.append(room)
#         self.waiting_num += 1
#         return True
#
#     def set_target_temp(self, room_id, target_temp):
#         for room in self.room_list:
#             if room.room_id == room_id:
#                 room.target_temp = target_temp
#                 break
#         return True
#
#     def set_fan_speed(self, room_id, fan_speed, fee_rate):
#         for room in self.room_list:
#             if room.room_id == room_id:
#                 room.fan_speed = fan_speed
#                 room.fee_rate = fee_rate
#                 break
#         return True
#
#     def Delete(self, room):
#         self.room_list.remove(room)
#         self.waiting_num -= 1
#         return True
#
#     def update_waiting_time(self):
#         if self.waiting_num != 0:
#             for room in self.room_list:
#                 room.wait_time += 1
#         timer = Timer(60, self.update_waiting_time)  # 每1min执行一次函数
#         timer.start()

class Scheduler(View):  # 在views里直接创建
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 在这里进行初始化操作
        self.high_temp = None
        self.low_temp = None
        self.h_rate_fee = None
        self.m_rate_fee = None
        self.l_rate_fee = None
        self.request_id = 0
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

        return_room.request_time = timezone.now()  # 数据库room表没有request_time项
        return_room.request_id = self.request_id
        self.request_id += 1
        return_room.operation = 3
        return_room.save(force_insert=True)

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
    def request_off(self, room_id):
        for room in self.SQ.room_list:
            if room.room_id == room_id:
                # 房间回到初始温度
                room.current_temp = room.init_temp
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

    def scheduling(self):
        # 资源足够的情况
        if len(self.WQ.room_list) != 0 and len(self.SQ.room_list) < 3:
            severing_num = len(self.SQ.room_list)
            i = 1
            for room in self.WQ.room_list:
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
        request_room.wait_time = 120  # 分配等待服务时长
        request_room.update_wait_time()  # 可能要再实现一个更新，是等待时长递减

        #  奇奇怪怪 是要每一个房间都分配一个服务时间好像

        while True:
            if self.check_condition():
                min_wait_serve_time_room = min(self.WQ.room_list, key=lambda x: x.wait_serve_time)
                self.WQ.delete(min_wait_serve_time_room)
                self.SQ.insert(min_wait_serve_time_room)
                min_wait_serve_time_room.wait_time = 0
                break

            elif request_room.wait_time <= 0:
                # 没有服务状态变化，释放服务队列中服务时长最大的服务对象
                max_serve_time_room = max(self.SQ.room_list, key=lambda x: x.serve_time)
                self.SQ.delete(max_serve_time_room)
                self.WQ.insert(max_serve_time_room)
                self.SQ.insert(request_room)
                request_room.serve_time = 0
                max_serve_time_room.wait_time = 0  # 分配等待服务时长
                break
            time.sleep(1)

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

class Sever(View):
    1



def login(request):
    return render(request, 'manager_login.html')
