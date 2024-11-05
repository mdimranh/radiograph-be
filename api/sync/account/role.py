from restapi.views.crud import CrudAPIView
from apps.account.models import Role
from .serializers import RoleSerializer
from apps.account.permissions import AdminPermission


class role(CrudAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    lookup_field = "id"
    permission_classes = [AdminPermission]
