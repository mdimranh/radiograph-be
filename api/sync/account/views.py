from restapi.views.crud import CrudAPIView
from apps.account.models import User
from .serializers import (
    UserSerializer,
)
from django.db.models import Q
from restapi.response import DictResponse
from utils.temp_password import generate_temp_password
from utils.brevo import email_service
class BaseUserhView(CrudAPIView):
    serializer_class = UserSerializer
    lookup_field = "id"

    def get_queryset(self):
        keyword = self.request.GET.get("keyword")
        if keyword:
            self.queryset = self.queryset.filter(
                Q(email__icontains=keyword)
                | Q(first_name__icontains=keyword)
                | Q(phone__icontains=keyword)
            )

        return super().get_queryset()

    def post(self, request, *args, **kwargs):

        identity = request.GET.get("identity")

        data = request.data
        current_user = request.user
        role_name = current_user.role.name
        match identity:
            case "radiologist":
                data["isRadiologist"] = True
            case "radiographer":
                data["isRadiographer"] = True
            case "admin":
                data["isAdmin"] = True

        if role_name and  role_name in ["division-officer", "super-admin"]:
            if current_user.role.name in ["division-officer"]:
                data['username'] = f"{data.get('first_name', '').replace(' ', '-').lower()}-{data.get('last_name', '').replace(' ', '-').lower()}"
                data['addBy'] = current_user.id
                data['status'] = "active"
                data['password'] = generate_temp_password()
                validation = UserSerializer(data=data)
            if validation.is_valid():
                insert = validation.save()
                data['id'] = insert.id
                
                # Basic email sending
                # email_service.send_template_email(
                #     template_name='login',
                #     subject=' Login to Your Account',
                #     recipients=validation.validated_data['email'],
                #     template_context={
                #         'first_name': validation.validated_data['first_name'],
                #         'last_name': validation.validated_data['last_name'],
                #         'phone': validation.validated_data['phone'],
                #         'password': validation.validated_data['password'],
                #     }
                # )
            else:
                return DictResponse(
                    validation_error=validation.errors, status=422
                )
            return DictResponse(message="User created successfully", data=data, status=201)
        else:
            return DictResponse(message="You are not authorized to perform this action", status=403)
        
    def put(self, request, *args, **kwargs):

        user_id = request.GET.get("id")
        data = request.data
        current_user = request.user
        role_name = current_user.role.name

        if role_name and  role_name in ["division-officer", "super-admin"]:
            user = User.objects.filter(id=user_id).first()
            if not user:
                return DictResponse(message="User not found", status=404)

            # Initialize variables for update
            status = user.status
            approved_by = None
            rejected_by = None

            # Determine the status and approver/rejecter
            if data.get("approved", False):
                status = "active"
                approved_by = current_user.id
            else:
                status = "rejected"
                rejected_by = current_user.id

            # Update the user
            update = User.objects.filter(id=user_id).update(
                status=status,
                approvedBy=approved_by,
                rejectedBy=rejected_by
            )

            data = {
                "id": user_id,
                "status": status
            }

            if update:
                return DictResponse(message="User updated successfully", data = data, status=200)

        return DictResponse(message="You are not authorized to perform this action", status=403)


class radiologist(BaseUserhView):
    queryset = User.objects.filter(isRadiologist=True)


class radiographer(BaseUserhView):
    queryset = User.objects.filter(isRadiographer=True)


class admin(BaseUserhView):
    queryset = User.objects.filter(isAdmin=True)


class user(CrudAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "id"
