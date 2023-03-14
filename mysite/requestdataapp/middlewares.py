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

        self.requests_dict[request.META['REMOTE_ADDR']] = self.requests_dict.get(request.META['REMOTE_ADDR'], [])

        # print('\n1', self.requests_dict[request.META['REMOTE_ADDR']])
        self.requests_dict[request.META['REMOTE_ADDR']].append(datetime.now())

        first_request_time = self.requests_dict[request.META['REMOTE_ADDR']][0]
        time_delta = ((datetime.now() - first_request_time).total_seconds() % 3600) // 60
        print(time_delta)
        if time_delta > 10:
            self.requests_dict[request.META['REMOTE_ADDR']] = self.requests_dict[request.META['REMOTE_ADDR']][1:]

        requests_per_time = len(self.requests_dict[request.META['REMOTE_ADDR']])
        print('number of requests is', requests_per_time)
        # print('\n2', self.requests_dict[request.META['REMOTE_ADDR']])

        if requests_per_time > 20:
            return HttpResponse('Too many requests in 10 minutes!')
            # return HttpResponse('Too many requests per hour!')

        response = self.get_response(request)
        self.responses_count += 1
        print('response count', self.responses_count)
        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        self.exceptions_count += 1
        print('got', self.exceptions_count, 'exceptions so far')
