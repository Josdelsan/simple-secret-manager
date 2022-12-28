from django.contrib import admin

from .models import Secret, Service, SecretSalt


admin.site.register(Service)
admin.site.register(SecretSalt)
admin.site.register(Secret)


