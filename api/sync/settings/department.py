from restapi.views.crud import CrudAPIView
from apps.account.models import Department
from .serializers import DepartmentSerializer
from apps.account.permissions import AdminPermission

from restapi.response import DictResponse


class department(CrudAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        keyword = self.request.GET.get("keyword")
        if keyword:
            self.queryset = self.queryset.filter(name__contains=keyword)
        return super().get(request, *args, **kwargs)
