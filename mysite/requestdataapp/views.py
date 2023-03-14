import os

from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def process_get_view(request: HttpRequest) -> HttpResponse:
    a = request.GET.get('a', '')
    b = request.GET.get('b', '')
    result = a + b
    context = {
        'a': a,
        'b': b,
        'result': result,
    }
    return render(request, 'requestdataapp/request-query-params.html', context=context)


def user_form(request: HttpRequest) -> HttpResponse:
    return render(request, 'requestdataapp/user-bio-form.html')


def handle_file_upload(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST' and request.FILES.get('myfile'):
        myfile = request.FILES['myfile']
        # print(f'\nFile size is - {myfile.size/1048576:.2} Mb\n')
        if myfile.size > 1048576:
            print(f'\nFile size is - {myfile.size / 1048576:.2} Mb\n')
            return HttpResponse('your file is too big!')
        print(f'\nFile size is - {myfile.size} byte\n')
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        print('saved file', filename)

    return render(request, 'requestdataapp/file-upload.html')
