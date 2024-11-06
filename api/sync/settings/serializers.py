from rest_framework.serializers import ModelSerializer
from apps.account.models import Role, Department


class RoleSerializer(ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"

class DepartmentSerializer(ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"
