from django.contrib import admin

# Register your models here.
from .models import AdminProfile, RadiographerProfile, RadiologistProfile, Certificate

admin.site.register(AdminProfile)
admin.site.register(RadiographerProfile)
admin.site.register(RadiologistProfile)
admin.site.register(Certificate)
