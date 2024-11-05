from rest_framework.permissions import IsAuthenticated
from restapi.views import ApiView
from restapi.response import DictResponse

from django.utils import timezone

from apps.account.models import User
from apps.session.models import Session

from .serializers import LoginSerializer


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
            response = DictResponse("Login successful")
            response.set_cookie(
                "access-token",
                session.access_token,
                path="/",
                expires=session.access_token_expires,
                httponly=False,
                samesite="None",
                secure=True,
            )
            response.set_cookie(
                "refresh-token",
                session.refresh_token,
                path="/",
                expires=session.refresh_token_expires,
                httponly=False,
                samesite="None",
                secure=True,
            )
            return response
        return DictResponse(validation_error=serializer.errors, status=400)


class verify(ApiView):
    def get(self, request):
        if request.user.is_authenticated:
            return DictResponse("Token verified")
        access_token = request.COOKIES.get("access-token")
        refresh_token = request.COOKIES.get("refresh-token")
        visitor_id = request.COOKIES.get("visitorId") or request.headers.get(
            "visitorId"
        )
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
                    return DictResponse("Invalid token", status=401)
                session.update_access_token()
                response = DictResponse({"message": "Token verified"})
                response.set_cookie(
                    "access-token",
                    session.access_token,
                    path="/",
                    expires=session.access_token_expires,
                    httponly=False,
                    samesite="None",
                    secure=True,
                )
            if (
                session.access_token_expires < timezone.now()
                and session.refresh_token_expires > timezone.now()
            ):
                session.update_access_token()
                response = DictResponse("Token verified")
                response.set_cookie(
                    "access-token",
                    session.access_token,
                    path="/",
                    expires=session.access_token_expires,
                    httponly=False,
                    samesite="None",
                    secure=True,
                )
        if refresh_token:
            session = Session.objects.filter(
                refresh_token=refresh_token,
                visitor_id=visitor_id,
                refresh_token_expires__gt=timezone.now(),
            ).first()
            if not session:
                response = DictResponse("Invalid token", status=401)
                response.remove_cookie("refresh-token")
                return response
            session.update_access_token()
            response = DictResponse("Token verified")
            response.set_cookie(
                "access-token",
                session.access_token,
                path="/",
                expires=session.access_token_expires,
                httponly=False,
                samesite="None",
                secure=True,
            )
            return response
        return DictResponse("Invalid token", status=401)


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
