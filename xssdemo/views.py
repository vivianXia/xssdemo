from django.http import JsonResponse
from django.shortcuts import render

from xss.decorators import skip_xss_check

msg = []


# @skip_xss_check
def comment(request):
    if request.method == "GET":
        return render(request, 'comment.html')
    else:
        v = request.POST.get('content')
        msg.append(v)
        return JsonResponse({'msg': msg})
        #return render(request, 'index.html', {'msg': msg})


def index(request):
    return render(request, 'index.html', {'msg': msg})

