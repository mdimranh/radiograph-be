from django.db import models
from utils.models import BaseModel
from apps.account.models import Department, User


class Report(BaseModel):
    parient_id = models.CharField(max_length=100)
    patient_name = models.CharField(max_length=100)
    patient_age = models.CharField(max_length=100)
    patient_gender = models.CharField(max_length=100)
    referral_doctor = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reports")
