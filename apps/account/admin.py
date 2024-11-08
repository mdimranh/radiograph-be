from django.contrib import admin
from .models import User, Role, Department, Rediologist

admin.site.register(User)
admin.site.register(Role)
admin.site.register(Department)
admin.site.register(Rediologist)
