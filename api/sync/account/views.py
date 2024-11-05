from restapi.views.crud import CrudAPIView
from apps.account.models import User
from .serializers import UserSerializer
from rest_framework.permissions import IsAdminUser


class user(CrudAPIView):
    permission_classes_for_get = [IsAdminUser]

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "id"
