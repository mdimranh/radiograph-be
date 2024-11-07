from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from apps.account.models import Role, Department, User


from rest_framework import serializers
from apps.profiles.models import (
    RadiologistProfile,
    RadiographerProfile,
    AdminProfile,
)


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class RadiologistProfileSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()

    class Meta:
        model = RadiologistProfile
        fields = [
            "about",
            "avatar_url",
            "gender",
            "marital_status",
            "blood_group",
            "certificate",
            "department",
        ]

    def get_avatar_url(self, obj):
        request = self.context.get("request")
        if obj.avatar and request:
            return request.build_absolute_uri(obj.avatar.url)
        return None

    def get_department(self, obj):
        data = Department.objects.filter(id=obj.department.id).first()
        if data:
            serializer = DepartmentSerializer(data)
            return serializer.data
        return None


class RadiographerProfileSerializer(serializers.ModelSerializer):
    department = serializers.SerializerMethodField()

    class Meta:
        model = RadiographerProfile
        fields = [
            "about",
            "avatar",
            "gender",
            "marital_status",
            "blood_group",
            "certificate",
            "department",
        ]

    def get_department(self, obj):
        # Check if the object has a ManyToMany relationship and is not empty
        if obj.department.exists():
            departments = obj.department.all()  # Get all related departments
            serializer = DepartmentSerializer(departments, many=True)
            return serializer.data
        return None


class AdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminProfile
        fields = [
            "about",
            "avatar",
            "gender",
            "marital_status",
            "blood_group",
            "certificate",
        ]


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    radiologist_profile = serializers.SerializerMethodField()
    radiographer_profile = serializers.SerializerMethodField()
    admin_profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ["password"]
        depth = 3

    def get_full_name(self, obj):
        full_name = f"{obj.first_name} {obj.last_name}"
        return full_name.strip()

    def get_radiologist_profile(self, obj):
        if hasattr(obj, "isRadiologist") and obj.isRadiologist:
            data = RadiologistProfile.objects.filter(user=obj).first()
            if data:
                serializer = RadiologistProfileSerializer(data, context=self.context)
                return serializer.data
        return None

    def get_radiographer_profile(self, obj):
        if hasattr(obj, "isRadiographer") and obj.isRadiographer:
            data = RadiographerProfile.objects.filter(user=obj).first()
            if data:
                serializer = RadiographerProfileSerializer(data, context=self.context)
                return serializer.data
        return None

    def get_admin_profile(self, obj):
        if hasattr(obj, "isAdmin") and obj.isAdmin:
            data = AdminProfile.objects.filter(user=obj).first()
            if data:
                serializer = AdminProfileSerializer(data, context=self.context)
                return serializer.data
        return None
