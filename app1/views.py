from django.http import HttpResponse
from django.shortcuts import render, redirect
from app1.models import User, Room, calculate_electricity_cost
from django.utils import timezone
import datetime
from django.db.models import Sum, F, ExpressionWrapper, DurationField
import django.db.models
from django.db.models.functions import Cast


# Create your views here.
def something(request):
    # 获取请求方式
    print(request.method)

    # 在URL上传递值
    print(request.GET)

    # 在请求体中提交数据
    print(request.POST)

    # return HttpResponse("返回内容")
    return render(request, 'something.html')


def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    else:
        # 如果是post请求，获取用户提交的数据
        print(request.POST)
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")
        if user == 'wang' and pwd == "123":
            return redirect("https://zhengyangwang1.github.io/")
        else:
            return render(request, "login.html", {'error_msg': '账号或密码有误，请重新登录！'})


def add_user(request):
    # User.objects.create(user_id='3314', user_name='wzy', user_age=20)
    User.objects.create(user_id='1111', user_name='222', user_age=20)

    return HttpResponse('导入成功')


def create_form(request, user_id, room_id):
    room_records = Room.objects.filter(user_id=user_id, room_id=room_id).order_by('open_time')
    context = {'records': room_records}
    cost = calculate_electricity_cost(room_records)
    context['cost'] = cost
    context['record'] = room_records[0].open_time
    return render(request, 'ac_usage_detail.html', context)


end = timezone.now()
start = end - datetime.timedelta(days=10)


def registration(request, start_date=start, end_date=end):
    bill_details = Room.objects.values("room_id").annotate(total_time=Sum(F("close_time") - F("open_time")))
    for detail in bill_details:
        room_id = detail["room_id"]
        room_records = Room.objects.filter(room_id=room_id)
        total_cost = calculate_electricity_cost(room_records)
        detail["total_cost"] = total_cost
    return render(request, 'registration.html', {'bill_details': bill_details})

# 需要添加的模块：
# 在用户更改温度时以及关闭空调时写数据进数据库
# 前端需要写生成表格的代码
