from django.http import HttpResponse
from xssdemo.models import Users
from json import dumps
def regist(request):
    nickname = request.POST.get('nickname')
    username = request.POST.get('username')
    password = request.POST.get('password')
    Users.objects.create(nickname=nickname,username=username,password=password)
    return HttpResponse(dumps({'state':'ok'}))

def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    res = list(Users.objects.filter(username=username,password=password).values())
    return HttpResponse(dumps(res))