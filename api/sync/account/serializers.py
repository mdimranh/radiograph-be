from rest_framework.serializers import ModelSerializer
from apps.account.models import User, Role


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ["password"]


class RoleSerializer(ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"
