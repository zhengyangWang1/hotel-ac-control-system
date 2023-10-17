from django.http import HttpResponse
from django.shortcuts import render, redirect
from app1.models import User, Room

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
