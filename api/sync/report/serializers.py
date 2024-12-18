from apps.report.models import Report
from rest_framework import serializers


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = "__all__"
