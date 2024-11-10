from rest_framework import serializers
from apps.account.models import User


from rest_framework import serializers
from apps.profiles.models import (
    RadiologistProfile,
    RadiographerProfile,
    AdminProfile,
)


class AdminRoleChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["role"]


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
