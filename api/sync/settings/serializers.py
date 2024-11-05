from rest_framework.serializers import ModelSerializer
from apps.account.models import Role


class RoleSerializer(ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"
