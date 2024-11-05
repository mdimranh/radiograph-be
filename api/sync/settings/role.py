from restapi.views.crud import CrudAPIView
from restapi.views import ApiView
from apps.account.models import Role
from .serializers import RoleSerializer
from apps.account.permissions import AdminPermission

from restapi.response import DictResponse


class role(CrudAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        keyword = self.request.GET.get("keyword")
        if keyword:
            self.queryset = self.queryset.filter(name__contains=keyword)
        return super().get(request, *args, **kwargs)
