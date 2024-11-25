from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from apps.account.models import User
from apps.session.models import Session

from ..auth.serializers import SessionSerializer

from api.sync.settings.serializers import DepartmentSerializer
from api.sync.profile.serializers import CertificateSerializer
from rest_framework import serializers
from apps.profiles.models import (
    RadiologistProfile,
    RadiographerProfile,
    AdminProfile,
)


class ProfileSerializer(ModelSerializer):
    department = serializers.SerializerMethodField()
    certificate = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        self.role = kwargs.pop("role", None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = None  # Set dynamically
        fields = [
            "about",
            "avatar",
            "gender",
            "marital_status",
            "blood_group",
            "department",
            "certificate",
        ]
        read_only_fields = ["avatar"]

    def get_department(self, obj):
        # Check if the object has the 'department' attribute
        if hasattr(obj, "department"):
            if hasattr(obj.department, "all"):
                departments = obj.department.all()
                if departments.exists():
                    serializer = DepartmentSerializer(departments, many=True)
                    return serializer.data
            elif obj.department:
                serializer = DepartmentSerializer(obj.department)
                return serializer.data
        return None

    def get_certificate(self, obj):
        # Check if the object has the 'certificate' attribute
        request = self.context.get("request")
        if hasattr(obj, "certificate") and request:
            certificates = obj.certificate.all()
            if certificates.exists():
                serializer = CertificateSerializer(
                    certificates, context=self.context, many=True
                )
                return serializer.data

        return None

    def to_representation(self, instance):
        # Dynamically set the model based on the role
        if self.role == "radiologist":
            self.Meta.model = RadiologistProfile
        elif self.role == "radiographer":
            self.Meta.model = RadiographerProfile
        elif self.role == "admin":
            self.Meta.model = AdminProfile

        return super().to_representation(instance)


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    profile = serializers.SerializerMethodField()
    session = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ["password"]
        depth = 1

    def get_full_name(self, obj):
        full_name = (
            f"{obj.first_name} {obj.last_name}" if obj.last_name else obj.first_name
        )
        return full_name.strip()

    def get_profile(self, obj):
        if hasattr(obj, "isRadiologist") and obj.isRadiologist:
            data = RadiologistProfile.objects.filter(user=obj).first()
            if data:
                serializer = ProfileSerializer(
                    data, context=self.context, role="radiologist"
                )
                return serializer.data
        elif hasattr(obj, "isRadiographer") and obj.isRadiographer:
            data = RadiographerProfile.objects.filter(user=obj).first()
            if data:
                serializer = ProfileSerializer(
                    data, context=self.context, role="radiographer"
                )
                return serializer.data
        elif hasattr(obj, "isAdmin") and obj.isAdmin:
            data = AdminProfile.objects.filter(user=obj).first()
            if data:
                serializer = ProfileSerializer(data, context=self.context, role="admin")
                print(serializer.data)
                return serializer.data
        return None

    def get_session(self, obj):
        session = Session.objects.filter(user=obj).order_by("-updated").first()
        return SessionSerializer(session).data
