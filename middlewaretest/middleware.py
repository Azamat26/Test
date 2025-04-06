from django.utils.deprecation import MiddlewareMixin
import logging
from django.http import HttpResponseForbidden, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
import time

RATE_LIMIT = 2
TIME_WINDOW = 1
USERS = {}

logger = logging.getLogger(__name__)

blocked_ip = ['127.0.0.1', '198.16.4.1']

class Test(MiddlewareMixin):
    def process_request(self, request):
        user_ip = request.META.get('REMOTE_ADDR')
        now = time.time()
        # print(f"текущее время: {now}")
        # print("request tttt")
        if user_ip not in USERS:
            USERS[user_ip] = []

        
        valid_timestamps = []
        for timestamp in USERS[user_ip]:
            if now - timestamp <= TIME_WINDOW:
                valid_timestamps.append(timestamp)

        USERS[user_ip] = valid_timestamps
        
        if len(USERS[user_ip]) >= RATE_LIMIT:
            return HttpResponse("Слишком много запросов. Попробуйте позже.", status=429)
        
        USERS[user_ip].append(now)
        
        print(USERS)
        #logger.info(10)
        # print(f"запрос: {request.method}, {request.path} ip: {request.META.get('REMOTE_ADDR')}")

    def process_response(self, request, response):
        # print("request rrrrr")
        # print(f"ответ: {response.status_code}")
        return response
    
    
class LoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        logger.info(f"Запрос:")

    def process_response(self, request, response):
        logger.info(f"Ответ")
        return response
    
# class Checker(MiddlewareMixin):
#     def process_request(self, request):
#         ip_address = request.META.get('REMOTE_ADDR')
#         path = request.path
#         print(f'ответ чекер: {ip_address}')
#         print(f'ответ чекер: {path}')
#         if ip_address in blocked_ip and path != "/contact/":
#             print(f"проверка {ip_address}")
#             return HttpResponseForbidden("Доступ закрыт")
#         else:
#             pass

# class Checker(MiddlewareMixin):
#     def process_request(self, request):
#         ip_address = request.META.get('REMOTE_ADDR')
#         path = request.path
#         print(f'ответ чекер: {ip_address}')
#         print(f'ответ чекер: {path}')
#         if ip_address in blocked_ip and path != "/contact/":
#             print(f"проверка {ip_address}")
#             return HttpResponseRedirect("https://google.com")
#         else:
#             pass

class Checker(MiddlewareMixin):
    def process_request(self, request):
        pass
        # ip_address = request.META.get('REMOTE_ADDR')
        # path = request.path
        # print(f'ответ чекер: {ip_address}')
        # print(f'ответ чекер: {path}')
        # if ip_address in blocked_ip and path != "/contact/":
        #     print(f"проверка {ip_address}")
        #     return HttpResponseRedirect("https://google.com")
        # else:
        #     pass

 
    

    
