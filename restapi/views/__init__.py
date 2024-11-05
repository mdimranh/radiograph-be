from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.db.models import QuerySet
from rest_framework import serializers
from ..response import DictResponse
from ..exceptions import ValidationError
from .request import Request
from enum import Enum
from django.core.paginator import InvalidPage
from ..exceptions import ExceptionHandlerMixin, RestException

from dotenv import load_dotenv
import os

load_dotenv(override=True)


class ApiView(ExceptionHandlerMixin, View):

    http_method_names = [
        "get",
        "post",
        "put",
        "patch",
        "delete",
        "head",
        "options",
        "trace",
        "details",
    ]

    permission_classes = []
    authentication_classes = []
    api_key_required = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = None

    def perform_authenticate(self):
        if self.authentication_classes:
            for auth_class in self.authentication_classes:
                user, session = auth_class().authenticate(self.request)
            if user and session:
                self.request.user = user
                self.request.session = session
                return

    def _check_apikey(self):
        self.request.internal = None
        api_key_required = getattr(
            self, f"api_key_required_for_{self.request.method.lower()}", None
        )
        if api_key_required is None:
            api_key_required = self.api_key_required

        if api_key_required:
            api_key = self.request.META.get("HTTP_API_KEY")
            if api_key is None:
                raise RestException()
            if api_key == os.environ.get("API_KEY"):
                self.request.internal = True
            else:
                self.request.external = False

    def has_permission(self):
        permission_classes = getattr(
            self, f"permission_classes_for_{self.request.method.lower()}", None
        )
        if permission_classes is None:
            permission_classes = self.permission_classes
        if not permission_classes:
            return True
        for permission in permission_classes:
            if permission().has_permission(self.request, self):
                return True
        return False

    def http_has_not_permission(self, *args, **kwargs):
        response = DictResponse(
            message="You have not enough permission to access this api.", status=401
        )

        if self.view_is_async:

            async def func():
                return response

            return func()
        else:
            return response

    def method_is_allowed(self, method):
        if method.lower() not in self.http_method_names:
            return False
        return True

    def http_method_not_allowed(self, *args, **kwargs):
        response = DictResponse(
            message=f"{self.request.method} method is not allowed.", status=403
        )

        if self.view_is_async:

            async def func():
                return response

            return func()
        else:
            return response

    def get_parser_context(self, http_request):
        """
        Returns a dict that is passed through to Parser.parse(),
        as the `parser_context` keyword argument.
        """
        # Note: Additionally `request` and `encoding` will also be added
        #       to the context by the Request object.
        return {
            "view": self,
            "args": getattr(self, "args", ()),
            "kwargs": getattr(self, "kwargs", {}),
        }

    def get_query_params(self, key=None):
        params = self.request.GET.dict()
        if key:
            return params.get(key)
        return params

    def dispatch(self, request, *args, **kwargs):
        try:
            self.request = request
            self._check_apikey()
            self.request.data = Request(self.request).data
            if not self.method_is_allowed(request.method):
                return self.http_method_not_allowed()
            # self.perform_authenticate()
            if not self.has_permission():
                return self.http_has_not_permission()
            return super().dispatch(self.request, *args, **kwargs)
        except Exception as e:
            return self.handle_exception(e)

    @classmethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        view.cls = cls
        view.initkwargs = initkwargs

        # Note: session based authentication is explicitly CSRF validated,
        # all other authentication is CSRF exempt.
        return csrf_exempt(view)
