from django.shortcuts import render

msg = []
def comment(request):
    if request.method == "GET":
        return render(request, 'comment.html')
    else:
        v = request.POST.get('content')
        if "script" in v:
            return render(request, 'comment.html', {'error': 'error'})
        else:
            msg.append(v)
            return render(request, 'index.html', {'msg': msg})

def index(request):
    return render(request, 'index.html', {'msg': msg})
