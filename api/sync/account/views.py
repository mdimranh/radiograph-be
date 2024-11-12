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

    def get_queryset(self):
        keyword = self.request.GET.get("keyword")
        if keyword:
            self.queryset = self.queryset.filter(
                Q(email__icontains=keyword)
                | Q(first_name__icontains=keyword)
                | Q(phone__icontains=keyword)
            )

        return super().get_queryset()


class radiologist(BaseUserhView):
    queryset = User.objects.filter(isRadiologist=True)


class radiographer(BaseUserhView):
    queryset = User.objects.filter(isRadiographer=True)


class admin(BaseUserhView):
    queryset = User.objects.filter(isAdmin=True)


class user(CrudAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "id"
