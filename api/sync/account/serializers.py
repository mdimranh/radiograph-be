from rest_framework.serializers import ModelSerializer
from apps.account.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ["password"]
