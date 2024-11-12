import math
from api.sync.account.views import user
from restapi.views.crud import CrudAPIView
from apps.account.models import User, Department
from apps.profiles.models import RadiologistProfile, RadiographerProfile, AdminProfile
from .serializers import (
    AdminRoleChangeSerializer,
    RadiographerProfileSerializer,
    RadiologistProfileSerializer,
    AdminProfileSerializer,
)
from api.sync.account.serializers import UserSerializer
from restapi.response import DictResponse
from restapi.views import ApiView

import time


class AdminRoleChange(CrudAPIView):
    queryset = User.objects.all()
    serializer_class = AdminRoleChangeSerializer
    lookup_field = "id"


class ProfileChange(ApiView):
    def put(self, request, *args, **kwargs):
        """
        User profile update:
            - First find the profile of the user using user_id and identity, then update the profile.
        """

        data = self.request.data
        user_id = self.request.GET.get("id")
        identity = self.request.GET.get("identity")

        if not identity:
            return DictResponse(
                message="Identity not found",
                status=404,
                data=None,
            )

        # Create a mapping from identity to model
        match identity:
            case "radiologist":
                model_class = RadiologistProfile
            case "radiographer":
                model_class = RadiographerProfile
            case "admin":
                model_class = AdminProfile

        queryset = model_class.objects.all()

        # Check if the profile exists
        profile = queryset.filter(user=user_id).first()

        if not profile:
            return DictResponse(
                message="Profile not found",
                status=404,
                data=None,
            )

        # Create the appropriate serializer dynamicall
        match identity:
            case "radiologist":
                serializer = RadiologistProfileSerializer(
                    profile, data=data, partial=True
                )
            case "radiographer":
                serializer = RadiographerProfileSerializer(
                    profile, data=data, partial=True
                )
            case "admin":
                serializer = AdminProfileSerializer(profile, data=data, partial=True)

        # Validate and save the serializer
        if not serializer.is_valid():
            return DictResponse(
                message="Invalid data",
                status=400,
                data=serializer.errors,
            )

        update = serializer.save()
        if update:
            return DictResponse(
                message="Profile updated",
                status=200,
                data=serializer.data,
            )

        return DictResponse(
            message="Profile not updated",
            status=400,
            data=None,
        )


class RadiologistProfiles(CrudAPIView):
    queryset = RadiologistProfile.objects.all()
    serializer_class = RadiologistProfileSerializer
    lookup_field = "id"


class RadiographerProfiles(CrudAPIView):
    queryset = RadiographerProfile.objects.all()
    serializer_class = RadiographerProfileSerializer
    lookup_field = "id"


class AdminProfiles(CrudAPIView):
    queryset = AdminProfile.objects.all()
    serializer_class = RadiographerProfileSerializer
    lookup_field = "id"
