from rest_framework.serializers import ModelSerializer
from apps.account.models import Role, Department, Radiologist
from rest_framework import serializers


class RoleSerializer(ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"


class DepartmentSerializer(ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class RadiologistSerializer(ModelSerializer):
    department = serializers.SerializerMethodField()

    class Meta:
        model = Radiologist
        fields = "__all__"

    def get_department(self, obj):

        # here i want name, and id
        if obj.department:
            return {"name": obj.department.name, "id": obj.department.id}
        return None

    def get_avatar(self, obj):
        request = self.context.get("request")
        if obj.avatar:
            return request.build_absolute_uri(obj.avatar.url)
        return None
