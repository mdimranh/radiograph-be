from rest_framework.serializers import ModelSerializer
from apps.account.models import Role, Department
from apps.settings.models import siteConfig

class RoleSerializer(ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"


class DepartmentSerializer(ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"

class siteConfigSerializer(ModelSerializer):
    class Meta:
        model = siteConfig
        fields = "__all__"

    def get_avatar(self, obj):
        request = self.context.get("request")
        if obj.avatar:
            return request.build_absolute_uri(obj.avatar.url)
        return None
