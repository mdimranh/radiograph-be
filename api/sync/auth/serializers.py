from rest_framework import serializers
from apps.session.models import Session


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField()
    remember = serializers.BooleanField(default=False)

    def validate(self, data):
        phone = data.get("phone")
        if not phone.isnumeric():
            raise serializers.ValidationError({"phone": "Phone number must be numeric"})
        if len(phone) != 11:
            raise serializers.ValidationError(
                {"phone": "Phone number must be 11 digits"}
            )
        return data


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = "__all__"
