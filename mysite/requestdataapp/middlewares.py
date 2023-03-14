from datetime import datetime

from django.http import HttpRequest, HttpResponse


def set_useragent_on_request_middleware(get_response):

    print('initial call')

    def middleware(request: HttpRequest):
        print('before get response')
        request.user_agent = request.META['HTTP_USER_AGENT']
        response = get_response(request)
        print('after get response')
        return response

    return middleware


class CountRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests_count = 0
        self.requests_dict = {}
        self.responses_count = 0
        self.exceptions_count = 0

    def __call__(self, request: HttpRequest):
        self.requests_count += 1
        print('requests count', self.requests_count)
        if request.META['REMOTE_ADDR'] in self.requests_dict:
            delta = int(((datetime.now() - self.requests_dict[request.META['REMOTE_ADDR']]).total_seconds() % 3600)//60)
            print(f'\nThe previous request was made {delta} min. ago.\n')
            if delta < 1:
                return HttpResponse('Too many requests per hour!')
        self.requests_dict[request.META['REMOTE_ADDR']] = datetime.now()
        # print(self.requests_dict)
        response = self.get_response(request)
        self.responses_count += 1
        print('response count', self.responses_count)
        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        self.exceptions_count += 1
        print('got', self.exceptions_count, 'exceptions so far')
