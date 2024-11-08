from restapi.views.crud import CrudAPIView
from restapi.views import ApiView
from apps.account.models import Radiologist, Department
from .serializers import RadiologistSerializer
from apps.account.permissions import AdminPermission
from django.db.models import Prefetch
from restapi.response import DictResponse


class radiologist(CrudAPIView):
    queryset = Radiologist.objects.all()
    serializer_class = RadiologistSerializer
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        keyword = self.request.GET.get("keyword")
        if keyword:
            self.queryset = self.queryset.filter(email__contains=keyword)

        else:
            self.queryset = (
                Radiologist.objects.all()
                .prefetch_related(
                    Prefetch("department", queryset=Department.objects.all())
                )
                .order_by("id")
            )

        serializer = self.get_serializer(self.queryset, many=True)
        self.queryset = serializer.data

        return DictResponse(
            data=self.queryset, status=200, message="successful", safe=False
        )

    def put(self, request, *args, **kwargs):

        data = self.request.data
        if data.get("department"):
            department = data.get("department")
            department = Department.objects.get(id=department.get("id"))
            update = Department.objects.filter(id=department.id).update(
                name=department.name
            )
            if update:
                return super().put(request, *args, **kwargs)
        else:
            return super().put(request, *args, **kwargs)
