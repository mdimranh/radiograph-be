from restapi.views.crud import CrudAPIView
from apps.account.models import User
from .serializers import UserSerializer


class radiologist(CrudAPIView):
    queryset = User.objects.filter(isRadiologist=True)
    serializer_class = UserSerializer
    lookup_field = "id"


class admin(CrudAPIView):
    queryset = User.objects.filter(isAdmin=True)
    serializer_class = UserSerializer
    lookup_field = "id"


class radiographer(CrudAPIView):
    queryset = User.objects.filter(isRadiographer=True)
    serializer_class = UserSerializer
    lookup_field = "id"
