from rest_framework import serializers
from apps.account.models import User


from rest_framework import serializers
from apps.profiles.models import (
    RadiologistProfile,
    RadiographerProfile,
    AdminProfile,
    Certificate,
)


class CertificateSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    class Meta:
        model = Certificate
        fields = "__all__"

    def get_file(self, obj):
        request = self.context.get("request")
        if hasattr(obj, "file") and obj.file:
            return request.build_absolute_uri(obj.file.url)
        return None


class AdminRoleChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["role", "fee", "status"]


class AdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminProfile
        fields = "__all__"


class RadiologistProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = RadiologistProfile
        fields = "__all__"


class RadiographerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = RadiographerProfile
        fields = "__all__"
