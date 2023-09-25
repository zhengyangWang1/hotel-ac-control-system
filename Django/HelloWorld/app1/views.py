from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def something(request):
    # 获取请求方式
    print(request.method)

    # 在URL上传递值
    print(request.GET)

    # 在请求体中提交数据
    print(request.POST)

    return HttpResponse("返回内容")