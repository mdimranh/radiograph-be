from restapi.views.crud import CrudAPIView
from apps.settings.models import siteConfig
from .serializers import siteConfigSerializer

from restapi.response import DictResponse


class configuration(CrudAPIView):
    queryset = siteConfig.objects.all()
    serializer_class = siteConfigSerializer
    lookup_field = "id"

    def put(self, request):
        config = siteConfig.get_instance()
        serializer = siteConfigSerializer(config, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return DictResponse(
                message="Configuration updated successfully",
                data=serializer.data,
                status=200
            )
        return DictResponse(
            validation_error=serializer.errors,
            status=422
)