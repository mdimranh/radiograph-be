from restapi.views.crud import CrudAPIView
from apps.account.models import User
from .serializers import (
    UserSerializer,
)
from django.db.models import Q
from restapi.response import DictResponse


class BaseUserhView(CrudAPIView):
    serializer_class = UserSerializer
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        keyword = self.request.GET.get("keyword")
        if keyword:
            self.queryset = self.queryset.filter(
                Q(email__icontains=keyword)
                | Q(first_name__icontains=keyword)
                | Q(phone__icontains=keyword)
            )

        serializer = self.get_serializer(self.queryset, many=True)
        data = serializer.data

        return DictResponse(data=data, status=200, message="successful", safe=False)


class radiologist(BaseUserhView):
    queryset = User.objects.filter(isRadiologist=True)


class radiographer(BaseUserhView):
    queryset = User.objects.filter(isRadiographer=True)
    serializer_class = UserSerializer
    lookup_field = "id"


class user(CrudAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "id"


class admin(BaseUserhView):
    queryset = User.objects.prefetch_related("role").filter(isAdmin=True)
