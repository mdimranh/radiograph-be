from restapi.views.crud import CrudAPIView
from apps.account.models import User
from ..serializers import (
    UserSerializer,
)
from django.db.models import Q
from restapi.response import DictResponse


class details(CrudAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        category = self.kwargs.get("category")
        match category:
            case "radiologist":
                queryset = self.queryset.filter(isRadiologist=True)
            case "radiographer":
                queryset = self.queryset.filter(isRadiographer=True)
            case "admin":
                queryset = self.queryset.filter(isAdmin=True)
        return queryset
