from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.utils import timezone
from manager import models
from threading import Timer
import datetime
import threading
import time
import django
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
            if queue_type == 1:
                room.serve_time += 1
            if queue_type == 2:
                room.wait_time += 1
        timer = Timer(10, lambda: self.update_time(queue_type))  # 每1min执行一次函数
        timer.start()


class ServingQueue(Queue):
    serving_num = 0
    queue_type = 1  # 1为服务状态
    room_list = []

    def insert(self, room, queue_type=1):
        super().insert(room, queue_type=queue_type)
        self.serving_num += 1
        room.sever_begin_time = django.utils.timezone.now()
        return True

    def delete(self, room):
        super().delete(room)
        self.serving_num -= 1
        room.sever_over_time = django.utils.timezone.now()
        return True

    def update_serve_time(self):
        super().update_time(queue_type=1)

    def auto_update_fee(self, mode):
        '''
        自动计费功能
        每秒
        '''
        if mode == 1:
            for room in self.room_list:
                if room.fan_speed == 3:
                    room.current_temp += 0.05
                    room.fee += 0.1
                elif room.fan_speed == 2:
                    room.current_temp += 0.05
                    room.fee += 0.05
                else:
                    room.current_temp += 0.05
                    room.fee = room.fee + 1/30
                # print(room.current_temp)
            timer = Timer(1, self.auto_update_fee, [1])
            timer.start()
        else:
            for room in self.room_list:
                if room.fan_speed == 3:
                    room.current_temp -= 0.016
                    room.fee += 0.016
                elif room.fan_speed == 2:
                    room.current_temp -= 0.016
                    room.fee += 0.008
                else:
                    room.current_temp -= 0.016
                    room.fee += 0.005
            timer = Timer(1, self.auto_update_fee, [2])
            timer.start()


class WaitingQueue(Queue):
    waiting_num = 0
    queue_type = 2  # 2为等待状态
    room_list = []

    def insert(self, room, queue_type=2):
        super().insert(room, queue_type=queue_type)
        self.waiting_num += 1
        return True

    def delete(self, room):
        super().delete(room)
        self.waiting_num -= 1
        return True

    def update_wait_time(self):
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
        self.default_target_temp = 0
        self.rooms = []  # 储存房间队列，最多有5个房间

        # 等待队列与服务队列
        self.SQ = ServingQueue()
        self.WQ = WaitingQueue()

        STATE_CHOICE = [
            (1, 'WORKING'),
            (2, 'SHUTDOWN'),
            (3, 'SETMODE'),
            (4, 'READY')
        ]

        self.state = 2

    def set_para(self, high_temp, low_temp, default, h_rate_fee, m_rate_fee, l_rate_fee):
        self.high_temp = high_temp
        self.low_temp = low_temp
        self.default_target_temp = default
        self.h_rate_fee = h_rate_fee
        self.m_rate_fee = m_rate_fee
        self.l_rate_fee = l_rate_fee
        return True

    # 用户申请资源
    def request_on(self, room_id, user_id, init_temp):  # 用户开机时调用
        '''
        一个请求到来，第一次开机分配房间对象然后处理，否则直接处理
        调用调度算法
        问题：房间ID如何分配的
        开始计费和计温
        '''
        return_room = Room(request_id=self.request_id)
        flag = 1
        for room in self.rooms:
            if room.room_id == room_id:  # 不是第一次开机，直接处理
                room.user_id = user_id
                room.target_temp = 22
                room.fan_speed = 2
                flag = 0
                if len(self.SQ.room_list) < 3:  # 服务队列未满
                    self.SQ.insert(room)
                    room.sever_begin_time = timezone.now()
                else:  # 服务队列已满
                    self.WQ.insert(room)
                    room.wait_time = 20
                return_room = room
                #  写入数据库
                room.request_time = timezone.now()
                room.request_id = self.request_id
                self.request_id += 1
                room.operation = 3
                room.save(force_insert=True)
        if flag == 1:  # 是第一次开机，先分配房间对象再处理
            temp_room = return_room
            self.request_num += 1  # 发出第一次开机请求的房间数加一
            if self.request_num > 5:  # 控制只能有五个房间开机
                return False  # 返回

            temp_room.room_id = room_id
            temp_room.init_temp = init_temp  # 11
            temp_room.current_temp = init_temp  # 11
            temp_room.user_id = user_id
            temp_room.target_temp = 22
            temp_room.fan_speed = 2
            self.rooms.append(temp_room)
            if len(self.SQ.room_list) < 3:  # 服务队列未满
                self.SQ.insert(temp_room)
                temp_room.sever_begin_time = timezone.now()
            else:  # 服务队列已满
                self.WQ.insert(temp_room)
                temp_room.wait_time = 20

            return_room = temp_room
            #  写入数据库
            temp_room.request_time = timezone.now()
            self.request_id += 1
            temp_room.operation = 3
            temp_room.save(force_insert=True)
        return return_room  # 返回房间的状态，目标温度，风速，费率以及费用

    # 用户关机
    def request_off(self, room_id):  # 将指定房间状态设为3：关闭
        for room in self.SQ.room_list:
            if room.room_id == room_id:

                # 修改房间状态
                if room.state == 1:  # 服务队列中
                    room.state = 3
                    self.SQ.delete(room)
                    room.sever_over_time = timezone.now()
                if room.state == 2:  # 等待队列中
                    room.state = 3
                    self.WQ.delete(room)
                else:
                    room.state = 3

                self.back_temp(room, 1)

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
            fee_rate = self.l_rate_fee  # 低风速时的费率
        elif fan_speed == 2:
            fee_rate = self.m_rate_fee  # 中风速时的费率
        elif fan_speed == 3:
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
                room.fan_speed = fan_speed
                room.request_id = self.request_id
                self.request_id += 1
                room.operation = 2
                room.request_time = timezone.now()
                room.save(force_insert=True)

                return room

    # 用户开关机更新房间状态
    def update_room_state(self, room_id):
        '''
        检查房间是否开机
        '''
        for room in self.rooms:
            # print(room.room_id)
            if room.room_id == room_id:
                return room

    def check_room_state(self):
        '''
        更新self.rooms
        '''
        timer = threading.Timer(5, self.check_room_state)  # 每五秒执行一次check函数,list_room为参数
        timer.start()
        return self.rooms

    def power_on(self):
        """
        开启中控机，中控机状态修改为”SETMODE“
        初始化房间队列
        :return:
        """
        Room.objects.all().delete()
        self.state = 3
        #  只要服务队列有房间就计费和计温,制热mode=1,制冷mode=2,
        # if self.default_target_temp == 22:
        self.SQ.auto_update_fee(1)  # 制热
        # else:
        #     self.SQ.auto_update_fee(2)  # 制冷

        # 开启调度函数
        self.scheduling()
        self.sup_print()
        #  只要有服务就检查是否有房间达到目标温度
        self.check_target_arrive()
        # 开启调度队列和等待队列的计时功能
        self.SQ.update_serve_time()
        # self.WQ.update_wait_time()

        return self.state

    def start_up(self):
        '''
        参数设置完毕，进入READY状态
        '''
        self.state = 4
        return self.state

    def back_temp(self, room, mode):
        '''
        回温
        '''
        # if room.state == 4:
        #     if mode == 1:
        #         if room.current_temp > room.init_temp:
        #             room.current_temp -= 0.008
        #             if room.target_temp_has_changed():
        #                 print(room.target_temp_has_changed())
        #                 if self.SQ.serving_num < 3:  # 服务队列没满
        #                     self.SQ.insert(room)
        #                 else:
        #                     self.WQ.insert(room)
        #             timer = threading.Timer(1, self.back_temp, [room, 1])  # 每1秒执行一次函数
        #             timer.start()
        if room.state == 3:
            if mode == 1:
                if room.current_temp > room.init_temp:
                    # print(room.current_temp)
                    # print(room.init_temp)
                    room.current_temp -= 0.05
                timer = threading.Timer(1, self.back_temp, [room, 1])  # 每1秒执行一次函数
                timer.start()

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
            self.priority_scheduling()
            self.time_slice_scheduling()

        # print("服务队列:")
        # for room in self.SQ.room_list:
        #     print(room.room_id)
        # print("等待队列:")
        # for room in self.WQ.room_list:
        #     print(room.room_id)
        #     request_room = self.WQ.room_list[0]
        #
        #     # 优先级调度启动
        #     available_room1 = [room for room in self.SQ.room_list if room.fan_speed < request_room.fan_speed]
        #     # 时间片调度启动
        #     available_room2 = [room for room in self.SQ.room_list if room.fan_speed == request_room.fan_speed]
        #     if available_room1:
        #         self.priority_scheduling(available_room1, request_room)  # 优先级调度
        #     elif available_room2:
        #         self.time_slice_scheduling(request_room)  # 时间片轮询调度
        #     else:
        #         if len(self.SQ.room_list) >= 3:
        #             self.WQ.insert(request_room)
        #         else:
        #             self.SQ.insert(request_room)
        #             request_room.wait_time = 0  # 分配等待服务时长
        #
        timer = threading.Timer(1, self.scheduling)  # 每2min执行一次调度函数
        timer.start()

    def sup_print(self):
        print("服务队列:")
        for room in self.SQ.room_list:
            print(room.room_id)
        print("等待队列:")
        for room in self.WQ.room_list:
            print(room.room_id)
        timer = threading.Timer(5, self.sup_print)
        timer.start()


    # 优先级调度
    def priority_scheduling(self):
        '''
        优先级调度
        '''
        for r in self.WQ.room_list:
            available_room1 = [room for room in self.SQ.room_list if room.fan_speed < r.fan_speed]
            if available_room1:
                # 找出风速最小那一档的所有房间
                min_fan_speed = min(available_room1, key=lambda x: x.fan_speed).fan_speed
                min_fan_speed_rooms = list(filter(lambda x: x.fan_speed == min_fan_speed, available_room1))
                # 按服务时间对房间进行排序
                sorted_rooms = sorted(min_fan_speed_rooms, key=lambda x: x.serve_time, reverse=True)
                self.SQ.delete(sorted_rooms[0])
                self.WQ.delete(r)
                self.SQ.insert(r)
                r.serve_time = 0
                self.WQ.insert(sorted_rooms[0])
                sorted_rooms[0].wait_time = 20

    # 时间片调度
    def time_slice_scheduling(self):
        for r in self.WQ.room_list:
            if r.wait_time > 0:
                r.wait_time -= 1
            else:
                available_room2 = [room for room in self.SQ.room_list if room.fan_speed == r.fan_speed]
                if available_room2:
                    # 没有服务状态变化，释放服务队列中服务时长最大的服务对象
                    max_serve_time_room = max(available_room2, key=lambda x: x.serve_time)
                    self.SQ.delete(max_serve_time_room)
                    self.WQ.delete(r)
                    self.SQ.insert(r)
                    r.serve_time = 0
                    self.WQ.insert(max_serve_time_room)
                    max_serve_time_room.wait_time = 20

    def check_target_arrive(self):  # 检查达到目标温度与否
        if len(self.SQ.room_list) != 0:
            for room in self.SQ.room_list:
                if abs(room.current_temp - room.target_temp) < 0.0001 or room.current_temp > room.target_temp:
                    # print(room.current_temp)
                    # print(room.target_temp)
                    self.request_off(room.room_id)

                    # self.SQ.delete(room)
                    # if self.default_target_temp == 22:
                    #     self.back_temp(room, 1)
                    # else:
                    #     self.back_temp(room, 2)

        # 不懂下面这段什么意义
        # if self.WQ.waiting_num != 0:
        #     for room in self.WQ.room_list:
        #         if abs(room.current_temp - room.target_temp) < 0.1 or room.current_temp < room.target_temp:
        #             room.state = 4
        #             self.WQ.delete_room(room)
        #             if self.default_target_temp == 22:
        #                 self.back_temp(room, 1)
        #             else:
        #                 self.back_temp(room, 2)
        timer = threading.Timer(0.05, self.check_target_arrive)  # 每5秒执行一次check函数
        timer.start()


def login(request):
    return render(request, 'manager_login.html')
