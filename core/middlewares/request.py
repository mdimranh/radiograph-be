from restapi.response import DictResponse
from restapi.views.request import Request
from django.db import connection
import time, json

# from copy import copy

# from apps.logs.models import ApiRequest


# class RequestLogMiddleware(object):
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def data(self, request):
#         return Request(request).data

#     def __call__(self, request):
#         start_time = time.time()
#         request_header = request.headers
#         request.META["HTTP_X_FORWARDED_FOR"] = request.META.get(
#             "HTTP_X_FORWARDED_FOR", ""
#         ).split(",")[0]
#         # payload = self.data(request)
#         self.response = self.get_response(request)
#         try:
#             payload = payload = request.data
#         except AttributeError:
#             payload = self.data(request)
#         qtime, queries = self.query_time(False)
#         if isinstance(self.response, DictResponse):
#             self.add_to_body("execution-time", round(time.time() - start_time, 2))
#             self.add_to_body("query-time", qtime)
#         response_header = self.response.headers

#         if (
#             not request.path.startswith("/admin")
#             and not request.path.startswith("/logs")
#             and not request.path.startswith("/favicon.ico")
#         ):
#             _response = copy(self.response)
#             try:
#                 response_body = self.response.data_dict
#             except:
#                 response_body = _response.content.decode("utf-8")
#             ApiRequest.objects.create(
#                 path=request.path,
#                 method=request.method,
#                 requestHeaders=dict(request_header),
#                 queryParams=dict(request.GET),
#                 payload=payload,
#                 statusCode=self.response.status_code,
#                 responseHeaders=dict(response_header),
#                 response=response_body,
#                 queryList=queries,
#                 executionTime=round(time.time() - start_time, 2),
#             )
#         return self.response

#     def query_time(self, add_to_body=False):
#         time = 0.0
#         for q in connection.queries:
#             time += float(q["time"])
#         if add_to_body:
#             self.add_to_body("total-query", len(connection.queries))
#             self.add_to_body("query-time", round(time, 2))
#         return round(time, 2), connection.queries

#     def add_to_body(self, key, value):
#         self.response.set_value(key, value)

#     def add_to_header(self, key, value):
#         self.response.headers["key"] = value


class ApiRequestMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        visitor_id = request.COOKIES.get("visitorId") or request.headers.get(
            "visitorId"
        )
        if not visitor_id:
            response = DictResponse("Bad request", status=400)
            return response
        response = self.get_response(request)
        return response
