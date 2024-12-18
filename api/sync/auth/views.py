from rest_framework.permissions import IsAuthenticated
from restapi.views import ApiView
from restapi.response import DictResponse
from core.exceptions import Unauthorized

from django.utils import timezone

from apps.account.models import User
from apps.session.models import Session

from .serializers import LoginSerializer
from ..account.serializers import UserSerializer


class login(ApiView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.filter(phone=serializer.data["phone"]).first()
            if not user:
                return DictResponse("User not found", status=404)
            if not user.check_password(serializer.data["password"]):
                return DictResponse("Invalid credentials", status=401)
            visitor_id = request.COOKIES.get("visitorId") or request.headers.get(
                "visitorId"
            )
            session = Session.objects.create(
                user=user,
                remember=serializer.data["remember"],
                user_agent=request.META.get("HTTP_USER_AGENT"),
                ip=request.META.get("REMOTE_ADDR"),
                visitor_id=visitor_id,
            )
            response = DictResponse(
                "Login successful",
                data=UserSerializer(session.user, context={"request": request}).data,
            )
            response.set_cookie(
                "access-token",
                session.access_token,
                path="/",
                max_age=5 * 60,
                httponly=False,
                samesite="None",
                secure=True,
            )
            response.set_cookie(
                "refresh-token",
                session.refresh_token,
                path="/",
                max_age=60 * 68 * 24,
                httponly=False,
                samesite="None",
                secure=True,
            )
            return response
        return DictResponse(validation_error=serializer.errors, status=422)


class verify(ApiView):
    def get(self, request):
        access_token = request.COOKIES.get("access-token") or request.headers.get(
            "access-token"
        )
        refresh_token = request.COOKIES.get("refresh-token") or request.headers.get(
            "refresh-token"
        )
        visitor_id = request.COOKIES.get("visitorId") or request.headers.get(
            "visitorId"
        )
        if not refresh_token:
            response = DictResponse("Credentials not provided", status=401)
            response.delete_cookie("access-token")
            response.delete_cookie("refresh-token")
            return response

        if access_token:
            session = Session.objects.filter(
                access_token=access_token, visitor_id=visitor_id
            ).first()
            if not session:
                session = Session.objects.filter(
                    refresh_token=refresh_token,
                    visitor_id=visitor_id,
                    refresh_token_expires__gt=timezone.now(),
                ).first()
                if not session:
                    response = DictResponse("Invalid token", status=401)
                    response.delete_cookie("access-token")
                    response.delete_cookie("refresh-token")
                    return response
                session.update_access_token()
                getUser = User.objects.get(id=session.user.id)
                response = DictResponse(
                    "Token verified",
                    data=UserSerializer(getUser, context={"request": request}).data,
                )
                response.set_cookie(
                    "access-token",
                    session.access_token,
                    path="/",
                    max_age=5 * 60,
                    httponly=False,
                    samesite="None",
                    secure=True,
                )
                return response
            if (
                session.access_token_expires < timezone.now()
                and session.refresh_token_expires > timezone.now()
            ):
                session.update_access_token()
                getUser = User.objects.get(id=session.user.id)
                response = DictResponse(
                    "Token verified",
                    data=UserSerializer(getUser, context={"request": request}).data,
                )
                response.set_cookie(
                    "access-token",
                    session.access_token,
                    path="/",
                    max_age=5 * 60,
                    httponly=False,
                    samesite="None",
                    secure=True,
                )
                return response

        session = Session.objects.filter(
            refresh_token=refresh_token,
            visitor_id=visitor_id,
            refresh_token_expires__gt=timezone.now(),
        ).first()
        if not session:
            response = DictResponse("Invalid token", status=401)
            response.delete_cookie("refresh-token")
            return response
        session.update_access_token()
        getUser = User.objects.get(id=session.user.id)
        response = DictResponse(
            "Token verified",
            data=UserSerializer(getUser, context={"request": request}).data,
        )
        response.set_cookie(
            "access-token",
            session.access_token,
            path="/",
            max_age=5 * 60,
            httponly=False,
            samesite="None",
            secure=True,
        )
        return response


class logout(ApiView):
    def get(self, request):
        if not request.user.is_authenticated:
            return DictResponse("User is not authenticated", status=401)
        session = request.session
        session.refresh_token_expires = timezone.now()
        session.access_token_expires = timezone.now()
        session.save()
        response = DictResponse("Logout successful")
        response.delete_cookie("access-token")
        response.delete_cookie("refresh-token")
        return response
