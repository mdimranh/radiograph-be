from channels.db import database_sync_to_async
from apps.account.models import User
from apps.session.models import Session
from django.contrib.auth.models import AnonymousUser


class JwtAuthMiddleware:
    """
    Custom middleware (insecure) that takes user IDs from the query string.
    """

    def __init__(self, app):
        self.app = app

    def get_cookies(self, headers):
        """
        Extract cookies from the Cookie header and return them as a dictionary.
        """
        cookies_header = headers.get("cookie")
        cookies = {}

        if cookies_header:
            # Cookies are sent as a single string, e.g., "cookie1=value1; cookie2=value2"
            cookie_pairs = cookies_header.split(";")
            for pair in cookie_pairs:
                key, value = pair.strip().split("=", 1)
                cookies[key] = value

        return cookies

    @database_sync_to_async
    def get_user(self, scope):
        headers = {key.decode(): value.decode() for key, value in scope["headers"]}
        cookies = self.get_cookies(headers)
        access_token = cookies.get("access-token")
        refresh_token = cookies.get("refresh-token")
        visitor_id = cookies.get("visitorId")

        user = AnonymousUser()

        if access_token:
            session = Session.objects.filter(access_token=access_token).first()
            if not session:
                if refresh_token:
                    session = Session.objects.filter(
                        refresh_token=refresh_token
                    ).first()
                    if not session:
                        return user
                    return session.user
                else:
                    return user
            return session.user

        elif refresh_token:
            session = Session.objects.filter(
                refresh_token=refresh_token, visitor_id=visitor_id
            ).first()
            if not session:
                return user
            return session.user
        else:
            return user

    async def __call__(self, scope, receive, send):
        scope["user"] = await self.get_user(scope)
        return await self.app(scope, receive, send)
