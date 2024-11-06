from restapi.views.crud import CrudAPIView
from apps.account.models import Department
from .serializers import DepartmentSerializer
from apps.account.permissions import AdminPermission

from restapi.response import DictResponse


class department(CrudAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    lookup_field = "id"
