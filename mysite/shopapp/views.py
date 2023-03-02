from timeit import default_timer

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render


def shop_index(request: HttpRequest):
    # print(request.path)
    # print(request.method)
    # print(request.headers)
    # return HttpResponse('Hello World')
    context = {
        'time_running': default_timer(),
    }
    return render(request, 'shopapp/shop-index.html', context=context)